@echo off
REM ============================================================
REM  Monitor de Seguranca Publica - Ribeirao Preto
REM  Script de instalacao e execucao (Windows)
REM ============================================================

setlocal

echo.
echo ===========================================================
echo   Monitor de Seguranca Publica - Instalacao e Execucao
echo ===========================================================
echo.

REM Garante que o script roda a partir da pasta onde ele esta
cd /d "%~dp0"

REM 1. Verifica se o Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado.
    echo Instale o Python 3.10+ em https://www.python.org/downloads/
    echo Marque a opcao "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado.
echo.

REM 2. Cria o ambiente virtual se ainda nao existir
if not exist "venv\" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o ambiente virtual.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Ambiente virtual ja existe.
)

REM 3. Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM 4. Atualiza o pip e instala as dependencias
echo.
echo [INFO] Instalando dependencias (pode demorar alguns minutos)...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar as dependencias.
    pause
    exit /b 1
)

REM 5. Executa a aplicacao
echo.
echo [OK] Tudo pronto! Iniciando a aplicacao...
echo O app abrira no navegador. Feche esta janela para encerrar.
echo.
streamlit run Seguranac.py

endlocal
pause
