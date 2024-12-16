@echo off
setlocal

:: Define a versão do Python aqui
set PYTHON_VERSION=3.11

:: Obtém o diretório atual do script .bat
set "PROJECT_DIR=%~dp0"
:: Remove a última barra invertida do caminho
set "PROJECT_DIR=%PROJECT_DIR:~0,-1%"

:: Extrai o nome da pasta do projeto a partir do caminho completo
for %%i in ("%PROJECT_DIR%") do set "FOLDER_NAME=%%~nxi"

:: Define o nome do ambiente virtual
set "VENV_NAME=ambiente_%FOLDER_NAME%"


echo Criando ambiente virtual em: "%PROJECT_DIR%\%VENV_NAME%"
python.exe -m venv "%VENV_NAME%"

echo Ambiente virtual '%VENV_NAME%' criado.

:: Ativa o ambiente virtual
call "%PROJECT_DIR%\%VENV_NAME%\Scripts\activate.bat"

echo Ambiente virtual '%VENV_NAME%' ativado.

:End
endlocal
