import streamlit as st
import pandas as pd
import zipfile
import io
from datetime import datetime

from gcp_utils import process_document, extract_keywords_from_description
from processing_utils import extract_contact_info
from ui_utils import display_results, display_search_results, display_job_analysis, display_resume_bank, display_resume_triage

# Adicione a imagem no cabeçalho
st.image("img/prototipo-globalhitss.png", use_column_width=True)

st.title("Análise de Currículos")

# Upload de arquivos PDF
uploaded_files = st.file_uploader("Selecione os currículos", type=["pdf"], accept_multiple_files=True)

# Inicializar os estados da sessão
if 'results' not in st.session_state:
    st.session_state.results = []
if 'curriculos_df' not in st.session_state:
    st.session_state.curriculos_df = pd.DataFrame(columns=["Nome do Arquivo", "Nome Completo", "Telefone", "Email", "LinkedIn",
                                                           "Palavras-Chave Técnica", "Tempo Experiência", "PDF Path"])

# Processamento dos arquivos carregados
if uploaded_files:
    results = []
    progress_bar = st.progress(0)
    num_files = len(uploaded_files)

    for i, uploaded_file in enumerate(uploaded_files):
        if not any(result['filename'] == uploaded_file.name for result in st.session_state.results):
            with st.spinner(f"Processando {uploaded_file.name}..."):
                file_path = f"docs/{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                extracted_text = process_document(file_path)
                name, phones, emails, linkedin_links = extract_contact_info(extracted_text)
                keywords = extract_keywords_from_description(description=extracted_text)
                experience = extract_keywords_from_description(description=extracted_text, pergunta="Qual o tempo de experiência desse candidato? Me diga apenas o número em anos.", key_word=False)
                
                result = {
                    "filename": uploaded_file.name,
                    "text": extracted_text,
                    "path": file_path,
                    "name": name,
                    "phones": phones,
                    "emails": emails,
                    "linkedin_links": linkedin_links,
                    "keywords": keywords,
                    "experience": experience
                }
                results.append(result)
                
                new_row = {
                    "Nome do Arquivo": uploaded_file.name, 
                    "Nome Completo": name, 
                    "Telefone": ", ".join(phones), 
                    "Email": ", ".join(emails),
                    "LinkedIn": ", ".join(linkedin_links),
                    "Palavras-Chave Técnica": keywords,
                    "Tempo Experiência": experience,
                    "PDF Path": file_path
                }
                st.session_state.curriculos_df = pd.concat([st.session_state.curriculos_df, pd.DataFrame([new_row])], ignore_index=True)
        
        progress_bar.progress((i + 1) / num_files)
    
    st.session_state.results.extend(results)
    st.success("Processamento concluído!")

# Criar abas para diferentes funcionalidades
tabs = st.tabs(["Resultados Executados", "Busca por Palavra-Chave", "Análise de Palavras-Chave", "Banco de Currículos", "Triagem Automática de Currículos"])

with tabs[0]:
    display_results(st.session_state.results)

with tabs[1]:
    display_search_results(st.session_state.results)

with tabs[2]:
    display_job_analysis(st.session_state.results)

with tabs[3]:
    display_resume_bank(st.session_state.curriculos_df)

with tabs[4]:
    display_resume_triage(st.session_state.results)