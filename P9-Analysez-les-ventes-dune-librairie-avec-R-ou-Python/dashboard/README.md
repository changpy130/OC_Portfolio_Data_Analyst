# 📚 Lapage Dashboard<a name="version-english"></a>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

> 🇫🇷 [Lire la version française](#version-française)

---

## 🎯 Project Context

Lapage is a French bookstore chain that launched its e-commerce platform 2 years ago. This interactive dashboard analyses 2 years of online sales data to support strategic decisions on pricing, product offering, and customer targeting.

**Business questions addressed:**
- How is revenue evolving over time, and what seasonal patterns exist?
- Which products and categories drive the most value?
- Are there significant differences in purchasing behaviour by gender and age?
- How concentrated is revenue across the customer base?

---

## 🛠️ Tech Stack

| Component | Technology | Role |
|---|---|---|
| Dashboard | Streamlit | Interactive multi-page web app |
| Visualisation | Plotly | Interactive charts |
| API | FastAPI + SQLite | REST API exposing KPIs |
| Testing | pytest | Automated data validation |
| CI/CD | GitHub Actions | Runs tests on every push |

---

## 📊 Dashboard Pages

| Page | Content |
|---|---|
| **🏠 Home** | Overview metrics — transactions, clients, products |
| **🌟 KPIs** | Year-over-year KPI comparison, product positioning scatter plot, Lorenz curve |
| **🌏 Évolution du CA** | Revenue time series with moving averages by granularity and period |
| **🔗 Corrélations** | Statistical correlation analysis between client and product variables |

---

## 📁 Project Structure

```
dashboard/
├── Home.py                  # Entry point
├── pages/
│   ├── 1_KPIs.py
│   ├── 2_Evolution du CA.py
│   └── 3_Corrélations.py
├── components/
│   ├── state.py             # Session state management
│   ├── data_loader.py       # Data loading & filtering + API calls
│   ├── calculation.py       # KPI & statistical calculations
│   ├── graph_plotly.py      # Plotly chart functions
│   └── ui.py                # Sidebar & shared UI components
└── tests/
    └── test_app.py          # pytest test suite
```

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the dashboard

```bash
cd dashboard
streamlit run Home.py
```

### 3. Run the API (optional — needed for live KPIs)

Open a second terminal:

```bash
cd api
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive documentation at `http://localhost:8000/docs`.

### 4. Run the tests

```bash
pytest tests/ -v
```

---

---

## Version Française<a name="version-française"></a>

# 📚 Lapage Dashboard

> 🇬🇧 [Read the English version](#version-english)

---

## 🎯 Contexte du projet

Lapage est une librairie française ayant lancé son site e-commerce il y a 2 ans. Ce tableau de bord interactif analyse 2 ans de données de ventes en ligne pour soutenir les décisions stratégiques sur la tarification, l'offre produit et le ciblage client.

**Questions métier traitées :**
- Comment évolue le chiffre d'affaires dans le temps, et quels patterns saisonniers existent ?
- Quels produits et catégories génèrent le plus de valeur ?
- Existe-t-il des différences significatives de comportement d'achat selon le genre et l'âge ?
- Quelle est la concentration des revenus sur la base clients ?

---

## 🛠️ Stack technique

| Composant | Technologie | Rôle |
|---|---|---|
| Dashboard | Streamlit | Application web multi-pages interactive |
| Visualisation | Plotly | Graphiques interactifs |
| API | FastAPI + SQLite | API REST exposant les KPIs |
| Tests | pytest | Validation automatisée des données |
| CI/CD | GitHub Actions | Exécution des tests à chaque push |

---

## 📊 Pages du dashboard

| Page | Contenu |
|---|---|
| **🏠 Accueil** | Métriques globales — transactions, clients, produits |
| **🌟 KPIs** | Comparaison annuelle des KPIs, scatter plot de positionnement produit, courbe de Lorenz |
| **🌏 Évolution du CA** | Série temporelle du CA avec moyennes mobiles par granularité et période |
| **🔗 Corrélations** | Analyse des corrélations statistiques entre variables clients et produits |

---

## 📁 Structure du projet

```
dashboard/
├── Home.py                  # Point d'entrée
├── pages/
│   ├── 1_KPIs.py
│   ├── 2_Evolution du CA.py
│   └── 3_Corrélations.py
├── components/
│   ├── state.py             # Gestion du session state
│   ├── data_loader.py       # Chargement & filtrage des données + appels API
│   ├── calculation.py       # Calculs KPI & statistiques
│   ├── graph_plotly.py      # Fonctions de graphiques Plotly
│   └── ui.py                # Sidebar & composants UI partagés
└── tests/
    └── test_app.py          # Suite de tests pytest
```

---

## 🚀 Lancer le projet

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Lancer le dashboard

```bash
cd dashboard
streamlit run Home.py
```

### 3. Lancer l'API (optionnel — nécessaire pour les KPIs en temps réel)

Ouvrir un second terminal :

```bash
cd api
uvicorn main:app --reload
```

L'API sera disponible sur `http://localhost:8000`.  
Documentation interactive sur `http://localhost:8000/docs`.

### 4. Lancer les tests

```bash
pytest tests/ -v
```
