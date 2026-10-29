# 🚨 Monitor de Segurança Pública - Ribeirão Preto

Painel interativo em Streamlit para monitoramento de ocorrências de segurança pública por região/bairro de Ribeirão Preto, com visualização em mapa, gráficos analíticos e tabela detalhada.

> **Observação:** os dados exibidos são simulados (gerados com `numpy`) apenas para fins de demonstração.

## Funcionalidades

- 📍 Mapa interativo (Folium) com marcadores por região, coloridos conforme o nível de alerta
- 📊 Gráfico de ocorrências por região
- 📈 Linha do tempo com ocorrências por hora
- 🔍 Distribuição por tipo de ocorrência
- 📋 Tabela detalhada por região
- Filtro por nível de alerta (Vermelho / Amarelo / Verde) na barra lateral

## Tecnologias

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [NumPy](https://numpy.org/)
- [Folium](https://python-visualization.github.io/folium/) + [streamlit-folium](https://github.com/randyzwitch/streamlit-folium)

## Como executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/<seu-usuario>/<seu-repositorio>.git
   cd <seu-repositorio>
   ```

2. (Recomendado) Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Rode a aplicação:

   ```bash
   streamlit run Seguranac.py
   ```

5. Acesse no navegador o endereço exibido no terminal (geralmente `http://localhost:8501`).
