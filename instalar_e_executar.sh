#!/usr/bin/env bash
# ============================================================
#  Monitor de Seguranca Publica - Ribeirao Preto
#  Script de instalacao e execucao (Linux / macOS)
# ============================================================

set -e

echo ""
echo "==========================================================="
echo "  Monitor de Seguranca Publica - Instalacao e Execucao"
echo "==========================================================="
echo ""

# Garante que o script roda a partir da pasta onde ele esta
cd "$(dirname "$0")"

# 1. Verifica se o Python 3 esta instalado
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERRO] Python 3 nao encontrado."
    echo "Instale o Python 3.10+ (https://www.python.org/downloads/)."
    exit 1
fi

echo "[OK] Python encontrado: $(python3 --version)"
echo ""

# 2. Cria o ambiente virtual se ainda nao existir
if [ ! -d "venv" ]; then
    echo "[INFO] Criando ambiente virtual..."
    python3 -m venv venv
else
    echo "[INFO] Ambiente virtual ja existe."
fi

# 3. Ativa o ambiente virtual
# shellcheck disable=SC1091
source venv/bin/activate

# 4. Atualiza o pip e instala as dependencias
echo ""
echo "[INFO] Instalando dependencias (pode demorar alguns minutos)..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# 5. Executa a aplicacao
echo ""
echo "[OK] Tudo pronto! Iniciando a aplicacao..."
echo "O app abrira no navegador. Pressione Ctrl+C para encerrar."
echo ""
streamlit run Seguranac.py
