# SUS-Data-Insights
Dashboard interativo para análise de internações hospitalares utilizando Python, Streamlit, Pandas e Altair.

<div align="center">

# 🏥 SUS Data Insights

**Análise inteligente de internações hospitalares**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Altair](https://img.shields.io/badge/Altair-Visualização-1F77B4)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

Dashboard interativo em Python para explorar custos, causas e distribuição de internações hospitalares.

![Prévia do dashboard](docs/preview.png)

</div>

---

## 📑 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Objetivos](#-objetivos)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Dados](#-dados)
- [Como executar](#-como-executar)
- [Melhorias futuras](#-melhorias-futuras)
- [Contexto acadêmico](#-contexto-acadêmico)
- [Autor](#-autor)

## 📊 Sobre o projeto

O **SUS Data Insights** transforma dados simulados de internações hospitalares em indicadores e visualizações, facilitando a análise de **custos**, **causas de internação** e **distribuição regional**. A ferramenta permite que o usuário explore os dados por meio de filtros e exporte os resultados.

## 🎯 Objetivos

- Analisar os custos das internações hospitalares.
- Identificar as causas mais frequentes de internação.
- Explorar a distribuição por faixa etária, sexo e região.
- Visualizar variações ao longo do tempo.
- Permitir consultas personalizadas por meio de filtros.

## 📈 Funcionalidades

| Recurso | Descrição |
|---|---|
| **Indicadores (KPIs)** | Custo total, quantidade de internações e média de dias de permanência |
| **Causa principal** | Identificação da causa de internação mais comum |
| **Gráficos** | Distribuição regional e evolução temporal |
| **Filtros** | Período, região, sexo e faixa etária |
| **Tabela interativa** | Visualização dos registros filtrados |
| **Exportação** | Download dos dados filtrados em CSV |

## 🛠️ Tecnologias

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/): interface web do dashboard
- [Pandas](https://pandas.pydata.org/): tratamento e análise dos dados
- [Altair](https://altair-viz.github.io/): visualizações interativas

## 📁 Estrutura do projeto

```
sus-data-insights/
├── app.py                                  # Código principal do dashboard
├── Analise_Internacoes_SUS_Simulacao.csv   # Base de dados simulada
├── requirements.txt                        # Dependências do projeto
├── docs/
│   └── preview.png                         # Captura de tela do dashboard
└── README.md
```

## 🗂️ Dados

A base `Analise_Internacoes_SUS_Simulacao.csv` contém registros **simulados**, criados exclusivamente para fins acadêmicos.

> ⚠️ **Aviso:** os dados **não representam informações oficiais do SUS** e não devem ser usados para conclusões reais sobre saúde pública.

**Principais colunas:** *(ajuste conforme o seu CSV)*

| Coluna | Descrição |
|---|---|
| `[data_internacao]` | Data da internação |
| `[regiao]` | Região do paciente |
| `[sexo]` | Sexo do paciente |
| `[faixa_etaria]` | Faixa etária |
| `[causa]` | Causa da internação |
| `[dias_permanencia]` | Dias de permanência hospitalar |
| `[custo]` | Custo da internação (R$) |

## 🚀 Como executar

**Pré-requisitos:** Python 3.9 ou superior e `pip`.

1. **Clone o repositório**
   ```bash
   git clone https://github.com/[seu-usuario]/sus-data-insights.git
   cd sus-data-insights
   ```

2. **(Opcional) Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o dashboard**
   ```bash
   streamlit run app.py
   ```

O app abrirá automaticamente em `http://localhost:8501`.

## 🔮 Melhorias futuras

- [ ] Comparativo entre períodos
- [ ] Mapa interativo por estado/região
- [ ] Análise de custo médio por causa de internação
- [ ] Exportação de relatórios em PDF
- [ ] Deploy no Streamlit Community Cloud

## 🎓 Contexto acadêmico

Projeto Integrador do curso de **Análise e Desenvolvimento de Sistemas (ADS)** do **Senac EAD**.

## 👤 Autor

**[Seu nome]**
[LinkedIn](https://linkedin.com/in/[seu-perfil]) · [GitHub](https://github.com/[seu-usuario])
