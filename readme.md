# Análise de Currículos com Streamlit e GCP

## Visão Geral

Este projeto tem como objetivo analisar currículos PDF utilizando os serviços do Google Cloud Platform (GCP), como Document AI e Vertex AI. A aplicação permite fazer upload de múltiplos currículos, extrair informações importantes, buscar por palavras-chave, comparar currículos com descrições de vagas e realizar triagens automáticas.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

project/
│
├── main.py
├── gcp_utils.py
├── processing_utils.py
└── ui_utils.py


- `main.py`: Arquivo principal que inicializa a aplicação Streamlit e define as abas de navegação.
- `gcp_utils.py`: Contém funções para processar documentos com o Document AI e extrair palavras-chave com o Vertex AI.
- `processing_utils.py`: Contém funções para extrair informações de contato dos currículos.
- `ui_utils.py`: Contém funções para exibir resultados na interface Streamlit.

## Configuração

### Pré-requisitos

- Python 3.7 ou superior
- Conta no Google Cloud Platform (GCP) com acesso aos serviços Document AI e Vertex AI
- Arquivo de credenciais do GCP (`gcpKey/globalhitss-producao-3e1c6665deca.json`)

### Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```


2. Crie um ambiente virtual e ative-o:

   python -m venv env
   source env/bin/activate  # Linux/Mac
   .\env\Scripts\activate  # Windows
3. Instale as dependências:

   pip install -r requirements.txt


4. Coloque o arquivo de credenciais do GCP na pasta `gcpKey`.


### Execução

1. Execute a aplicação Streamlit:

   streamlit run main.py.
2. Acesse a aplicação no navegador através do endereço fornecido (`http://localhost:8501`).



## Funcionalidades

### Upload de Currículos

* Faça upload de múltiplos currículos em formato PDF.
* Os currículos serão processados usando o Document AI para extrair texto.

### Resultados Executados

* Visualize o texto extraído de cada currículo.
* Faça o download do texto extraído ou do PDF original.

### Busca por Palavra-Chave

* Adicione palavras-chave separadas por vírgulas para buscar nos currículos.
* Visualize e faça download dos currículos que contêm as palavras-chave fornecidas.

### Análise de Palavras-Chave

* Insira uma descrição de vaga para extrair palavras-chave técnicas usando o Vertex AI.
* Compare os currículos com as palavras-chave extraídas da descrição da vaga.

### Banco de Currículos

* Visualize um banco de currículos com informações extraídas como nome, telefone, email e LinkedIn.
* Faça o download de todos os currículos em um arquivo ZIP.

### Triagem Automática de Currículos

* Realize uma triagem automática dos currículos com base em palavras-chave ou descrição da vaga.
* Agrupe os currículos pela quantidade de correspondências com as palavras-chave.
* Faça o download de todos os currículos triados em um arquivo ZIP.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

### Executar a Aplicação Streamlit

Para executar a aplicação Streamlit, use o seguinte comando no terminal:

```bash
streamlit run main.py
```
