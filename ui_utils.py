import streamlit as st
import pandas as pd
import io
import zipfile
from datetime import datetime
from gcp_utils import extract_keywords_from_description

def display_results(results):
    """
    Exibe os resultados dos currículos processados.

    Args:
    results (list): Lista de resultados processados.
    """
    st.header("Resultados Executados")
    if results:
        for idx, result in enumerate(results):
            with st.expander(f"Resultados para: {result['filename']}"):
                st.write(result["text"])
                st.download_button(
                    label="Baixar texto extraído",
                    data=result["text"],
                    file_name=f"{result['filename']}.txt",
                    key=f"download_text_{idx}"
                )
                with open(result["path"], "rb") as file:
                    st.download_button(
                        label="Baixar PDF original",
                        data=file,
                        file_name=result["filename"],
                        key=f"download_pdf_{idx}"
                    )

def display_search_results(results):
    """
    Exibe os resultados da busca por palavras-chave.

    Args:
    results (list): Lista de resultados processados.
    """
    st.header("Busca por Palavras-Chave")
    keywords = st.text_input("Adicione palavras-chave separadas por vírgulas", key="search_keywords")

    if keywords:
        keywords = [keyword.strip().lower() for keyword in keywords.split(",")]
        keywords_no_space = [keyword.replace(" ", "") for keyword in keywords]
        
        filtered_results = []
        for result in results:
            text = result["text"].lower()
            matched_keywords = set()
            for keyword in keywords + keywords_no_space:
                if keyword in text:
                    matched_keywords.add(keyword)
            keyword_count = len(matched_keywords)
            if keyword_count > 0:
                filtered_results.append((keyword_count, result))
        
        if filtered_results:
            st.write("Currículos encontrados com as palavras-chave fornecidas:")
            filtered_results.sort(reverse=True, key=lambda x: x[0])  # Ordenar por contagem de palavras-chave
            grouped_results = {}
            for count, result in filtered_results:
                if count not in grouped_results:
                    grouped_results[count] = []
                grouped_results[count].append(result)
            
            for count in sorted(grouped_results.keys(), reverse=True):
                st.write(f"Currículos com {count} palavras-chave correspondentes:")
                for idx, result in enumerate(grouped_results[count]):
                    with st.expander(f"Resultados para: {result['filename']}"):
                        st.write(result["text"])
                        st.download_button(
                            label="Baixar texto extraído",
                            data=result["text"],
                            file_name=f"{result['filename']}.txt",
                            key=f"filtered_download_text_{count}_{idx}"
                        )
                        with open(result["path"], "rb") as file:
                            st.download_button(
                                label="Baixar PDF original",
                                data=file,
                                file_name=result["filename"],
                                key=f"filtered_download_pdf_{count}_{idx}"
                            )
            
            # Botão para baixar todos os resultados filtrados como ZIP
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for count, results in grouped_results.items():
                        for result in results:
                            pdf_path = result["path"]
                            pdf_name = result["filename"]
                            zip_file.write(pdf_path, f"{count}_palavras_chave/{pdf_name}")
                    keywords_str = ", ".join(keywords)
                    zip_file.writestr("palavras_chave.txt", keywords_str)
                zip_buffer.seek(0)
                st.download_button(
                    label="Baixar todos os currículos filtrados",
                    data=zip_buffer,
                    file_name="curriculos_filtrados.zip",
                    mime="application/zip"
                )
        else:
            st.write("Nenhum currículo encontrado com as palavras-chave fornecidas.")

def display_job_analysis(results):
    """
    Exibe a análise de compatibilidade de currículos com a descrição da vaga.

    Args:
    results (list): Lista de resultados processados.
    """
    st.header("Análise de Palavras-Chave e Comparação com Descrições de Vagas")
    
    job_description_text = st.text_area("Insira a descrição da vaga", key="job_description")
    
    if job_description_text:
        job_keywords = extract_keywords_from_description(job_description_text)
        job_keywords_no_space = [keyword.replace(" ", "") for keyword in job_keywords]
    
        st.write("Palavras-chave técnicas extraídas da descrição da vaga:")
        st.write(", ".join(job_keywords))
        
        if results:
            st.write("Análise de compatibilidade dos currículos com a descrição da vaga:")
            compatibility_results = []
            
            for result in results:
                text = result["text"].lower()
                matched_keywords = set()
                for keyword in job_keywords + job_keywords_no_space:
                    if keyword in text:
                        matched_keywords.add(keyword)
                keyword_count = len(matched_keywords)
                compatibility_results.append((keyword_count, result))
            
            compatibility_results.sort(reverse=True, key=lambda x: x[0])  # Ordenar por contagem de palavras-chave
            for count, result in compatibility_results:
                with st.expander(f"Resultados para: {result['filename']} (Compatibilidade: {count} palavras-chave)"):
                    st.write(result["text"])
                    st.download_button(
                        label="Baixar texto extraído",
                        data=result["text"],
                        file_name=f"{result['filename']}.txt",
                        key=f"compatibility_download_text_{result['filename']}"
                    )
                    with open(result["path"], "rb") as file:
                        st.download_button(
                            label="Baixar PDF original",
                            data=file,
                            file_name=result["filename"],
                            key=f"compatibility_download_pdf_{result['filename']}"
                        )

def display_resume_bank(df):
    """
    Exibe o banco de currículos com opção de download.

    Args:
    df (pd.DataFrame): DataFrame contendo os currículos processados.
    """
    st.header("Banco de Currículos")
    df['LinkedIn'] = df['LinkedIn'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if x else '')
    df['PDF Download'] = df.apply(lambda row: f'<a href="{row["PDF Path"]}" download="{row["Nome do Arquivo"]}">Baixar PDF</a>', axis=1)
    st.write(df.to_html(escape=False), unsafe_allow_html=True)
    
    # Botão para baixar todos os currículos como ZIP
    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for _, row in df.iterrows():
                pdf_path = row["PDF Path"]
                with open(pdf_path, "rb") as f:
                    pdf_data = f.read()
                zip_file.writestr(f'{row["Nome do Arquivo"]}', pdf_data)
        zip_buffer.seek(0)
        st.download_button(
            label="Baixar todo o banco de currículos",
            data=zip_buffer,
            file_name="banco_de_curriculos.zip",
            mime="application/zip"
        )

def display_resume_triage(results):
    """
    Exibe a triagem automática de currículos com base em palavras-chave ou descrição da vaga.

    Args:
    results (list): Lista de resultados processados.
    """
    st.header("Triagem Automática de Currículos")

    job_name = st.text_input("Nome da Vaga", key="triage_job_name")

    if not job_name:
        st.warning("Por favor, insira o nome da vaga para prosseguir.")
    else:
        triage_option = st.radio("Escolha a forma de triagem", ("Palavras-Chave", "Descrição da Vaga"), key="triage_option")

        if triage_option == "Palavras-Chave":
            keywords = st.text_input("Adicione palavras-chave separadas por vírgulas", key="triage_keywords")
            if keywords:
                keywords = [keyword.strip().lower() for keyword in keywords.split(",")]
                keywords_no_space = [keyword.replace(" ", "") for keyword in keywords]
                filtered_results = []
                for result in results:
                    text = result["text"].lower()
                    matched_keywords = set()
                    for keyword in keywords + keywords_no_space:
                        if keyword in text:
                            matched_keywords.add(keyword)
                    keyword_count = len(matched_keywords)
                    if keyword_count > 0:
                        filtered_results.append((keyword_count, result))
                
                if filtered_results:
                    st.write("Currículos encontrados com as palavras-chave fornecidas:")
                    filtered_results.sort(reverse=True, key=lambda x: x[0])  # Ordenar por contagem de palavras-chave
                    grouped_results = {}
                    for count, result in filtered_results:
                        if count not in grouped_results:
                            grouped_results[count] = []
                        grouped_results[count].append(result)
                    
                    triage_dataframes = []
                    for count in sorted(grouped_results.keys(), reverse=True):
                        group_df = pd.DataFrame([
                            {
                                "Nome do Arquivo": res["filename"],
                                "Nome Completo": res["name"],
                                "Telefone": ", ".join(res["phones"]),
                                "Email": ", ".join(res["emails"]),
                                "LinkedIn": ", ".join(res["linkedin_links"]),
                                "Palavras-Chave Técnica": ", ".join(res["keywords"]),
                                "Tempo Experiência": res["experience"],
                                "PDF Download": res["path"]
                            }
                            for res in grouped_results[count]
                        ])
                        group_df['LinkedIn'] = group_df['LinkedIn'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if x else '')
                        triage_dataframes.append((count, group_df))
                        st.write(f"Currículos com {count} palavras-chave correspondentes:")
                        st.write(group_df.to_html(escape=False), unsafe_allow_html=True)

                    # Botão para baixar todos os resultados filtrados como ZIP
                    current_date = datetime.now().strftime("%Y-%m-%d")
                    zip_filename = f"triagem_inteligente_{job_name}_{current_date}.zip"
                    with io.BytesIO() as zip_buffer:
                        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                            for count, group_df in triage_dataframes:
                                for _, row in group_df.iterrows():
                                    pdf_path = row["PDF Download"]
                                    with open(pdf_path, "rb") as f:
                                        pdf_data = f.read()
                                    zip_file.writestr(f"{count}_palavras_chave/{row['Nome do Arquivo']}", pdf_data)
                            keywords_str = ", ".join(keywords)
                            zip_file.writestr("palavras_chave.txt", keywords_str)
                        zip_buffer.seek(0)
                        st.download_button(
                            label="Baixar todos os currículos triados",
                            data=zip_buffer,
                            file_name=zip_filename,
                            mime="application/zip"
                        )
                else:
                    st.write("Nenhum currículo encontrado com as palavras-chave fornecidas.")

        elif triage_option == "Descrição da Vaga":
            job_description_text = st.text_area("Insira a descrição da vaga", key="triage_job_description")
            if job_description_text:
                job_keywords = extract_keywords_from_description(job_description_text)
                job_keywords_no_space = [keyword.replace(" ", "") for keyword in job_keywords]
            
                st.write("Palavras-chave técnicas extraídas da descrição da vaga:")
                st.write(", ".join(job_keywords))
                
                if results:
                    st.write("Análise de compatibilidade dos currículos com a descrição da vaga:")
                    compatibility_results = []
                    
                    for result in results:
                        text = result["text"].lower()
                        matched_keywords = set()
                        for keyword in job_keywords + job_keywords_no_space:
                            if keyword in text:
                                matched_keywords.add(keyword)
                        keyword_count = len(matched_keywords)
                        compatibility_results.append((keyword_count, result))
                    
                    if compatibility_results:
                        compatibility_results.sort(reverse=True, key=lambda x: x[0])  # Ordenar por contagem de palavras-chave
                        grouped_results = {}
                        for count, result in compatibility_results:
                            if count not in grouped_results:
                                grouped_results[count] = []
                            grouped_results[count].append(result)
                        
                        triage_dataframes = []
                        for count in sorted(grouped_results.keys(), reverse=True):
                            group_df = pd.DataFrame([
                                {
                                    "Nome do Arquivo": res["filename"],
                                    "Nome Completo": res["name"],
                                    "Telefone": ", ".join(res["phones"]),
                                    "Email": ", ".join(res["emails"]),
                                    "LinkedIn": ", ".join(res["linkedin_links"]),
                                    "Palavras-Chave Técnica": ", ".join(res["keywords"]),
                                    "Tempo Experiência": res["experience"],
                                    "PDF Download": res["path"]
                                }
                                for res in grouped_results[count]
                            ])
                            group_df['LinkedIn'] = group_df['LinkedIn'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>' if x else '')
                            triage_dataframes.append((count, group_df))
                            st.write(f"Currículos com {count} palavras-chave correspondentes:")
                            st.write(group_df.to_html(escape=False), unsafe_allow_html=True)

                        # Botão para baixar todos os resultados filtrados como ZIP
                        current_date = datetime.now().strftime("%Y-%m-%d")
                        zip_filename = f"triagem_inteligente_{job_name}_{current_date}.zip"
                        with io.BytesIO() as zip_buffer:
                            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                                for count, group_df in triage_dataframes:
                                    for _, row in group_df.iterrows():
                                        pdf_path = row["PDF Download"]
                                        with open(pdf_path, "rb") as f:
                                            pdf_data = f.read()
                                        zip_file.writestr(f"{count}_palavras_chave/{row['Nome do Arquivo']}", pdf_data)
                                keywords_str = ", ".join(job_keywords)
                                zip_file.writestr("palavras_chave.txt", keywords_str)
                            zip_buffer.seek(0)
                            st.download_button(
                                label="Baixar todos os currículos triados",
                                data=zip_buffer,
                                file_name=zip_filename,
                                mime="application/zip"
                            )
                    else:
                        st.write("Nenhum currículo encontrado com a descrição da vaga fornecida.")
