from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
import vertexai
from vertexai.language_models import TextGenerationModel

# Configurar as credenciais do GCP
credentials = service_account.Credentials.from_service_account_file('gcpKey/globalhitss-producao-3e1c6665deca.json')

# Inicializar o cliente do Document AI
documentai_client = documentai.DocumentProcessorServiceClient(credentials=credentials)
# teste 
# Inicializar o cliente do Vertex AI
vertexai.init(project='globalhitss-producao', location='us-central1')

def process_document(file_path):
    """
    Processa um documento PDF usando o Document AI do GCP.

    Args:
    file_path (str): Caminho para o arquivo PDF.

    Returns:
    str: Texto extraído do documento.
    """
    with open(file_path, 'rb') as file:
        content = file.read()
    
    project_id = 'globalhitss-producao'
    location = "us"
    processor_id = 'd3af668f314232de'

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    
    document = {"content": content, "mime_type": "application/pdf"}

    request = {
        "name": name,
        "raw_document": document
    }

    result = documentai_client.process_document(request=request)
    text = ""
    for page in result.document.pages:
        for paragraph in page.paragraphs:
            for segment in paragraph.layout.text_anchor.text_segments:
                start_index = segment.start_index if segment.start_index else 0
                end_index = segment.end_index
                text += result.document.text[start_index:end_index]
            text += "\n"
    return text

def extract_keywords_from_description(description, pergunta='Quais são todas as palavras chaves tecnicas desse texto? Me de uma resposta somente com as palavras separadas por vigula', key_word=True):
    """
    Extrai palavras-chave técnicas da descrição usando o modelo text-bison do Vertex AI.

    Args:
    description (str): Descrição do trabalho ou texto do currículo.
    pergunta (str): Pergunta a ser feita ao modelo de linguagem.
    key_word (bool): Se True, retorna as palavras-chave; caso contrário, retorna o texto completo.

    Returns:
    list or str: Lista de palavras-chave ou texto extraído.
    """
    temperature = 1
    parameters = {
        "temperature": temperature,
        "max_output_tokens": 2000,
        "top_p": 0,
        "top_k": 1,
    }
 
    texto_trat = description + '\n Q:' + pergunta + '\n A:'
 
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
      texto_trat,
        **parameters,
    )
    
    resposta = response.text
    if key_word:
        key_words = resposta.replace('(','').replace(')','').split(',')
    else:
        key_words = resposta.strip()
    return key_words
