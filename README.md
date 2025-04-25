# 🐍 Learn2Slither — Snake AI en Q-Learning

**Learn2Slither** est un projet d'intelligence artificielle où un agent (le serpent) apprend à jouer au jeu Snake en utilisant l'algorithme de **Q-learning**. Il s'agit d'une version optimisée avec un champ de vision réduit (sur les axes X et Y), un système de récompenses, des pommes vertes et rouges, un replay de parties, et de nombreuses visualisations de données pour suivre l'apprentissage.

---

## 🚀 Installation

Assurez-vous d'utiliser **Python 3.12+**.

1. Clonez le dépôt :

```bash
git clone https://github.com/ltuffery/Learn2Slither.git
cd Learn2Slither
```

2. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

---

## ⚙️ Lancer le jeu (manuellement)

```bash
python main.py
```

---

## 🏋️ Entraîner l'IA

L'entraînement utilise l'algorithme Q-Learning avec une table `Q[(state, action)]` :

```bash
python -m ai.train
```

Cela produit :

- `data/q_table.csv` : la Q-table sauvegardée
- `data/rewards.csv` : les récompenses par épisode
- `replay/replay.json` : l'historique d'une partie

---

## 🔁 Rejouer une partie

Le système de replay lit un fichier `.json` contenant les états, actions et résultats.

```bash
python -m ai.replay
```
