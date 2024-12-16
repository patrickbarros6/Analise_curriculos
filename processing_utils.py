import re
from gcp_utils import extract_keywords_from_description

def extract_contact_info(text):
    """
    Extrai nome completo, telefone, email e LinkedIn do texto.

    Args:
    text (str): Texto extraído do documento.

    Returns:
    tuple: Nome, telefones, emails e links do LinkedIn.
    """
    # Regex para email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    
    # Regex para telefone (formatos comuns no Brasil)
    phone_pattern = r'\(?\d{2}\)?\s?\d{4,5}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    
    # Regex para LinkedIn
    linkedin_pattern = r'https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9-_/]+'
    linkedin_links = re.findall(linkedin_pattern, text)
    
    # Nome completo (heurística: primeira linha do currículo)
    name = extract_keywords_from_description(description=text, pergunta='Qual o nome completo do candidato? Me responda apenas o nome completo.', key_word=False)
    return name, phones, emails, linkedin_links
