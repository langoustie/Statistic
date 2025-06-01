# 🔬 Estimation expérimentale du coefficient de refroidissement – méthode du χ²

Ce projet propose deux approches numériques pour estimer le **coefficient de refroidissement thermique \( r \)** à partir de données expérimentales, en utilisant la **méthode du χ²** (chi carré).

---

## ℹ️ Contexte scientifique

Dans de nombreuses expériences de physique, on cherche à ajuster un modèle théorique aux données mesurées.  
La méthode du **χ²** est une technique d’estimation des paramètres qui permet :

- de trouver la **valeur optimale** d’un paramètre (ici, \( r \)) qui **minimise l’écart pondéré** entre les données et le modèle,
- d’estimer **l’incertitude** sur ce paramètre à partir du critère \( \chi^2 = \chi^2_{\text{min}} + 1 \).

---

## 📐 La méthode du χ²

Pour un modèle \( f(t, r) \) et des données expérimentales \( (t_i, T_i) \) avec incertitudes \( \sigma_i \), la statistique χ² est définie par :

\[
\chi^2(r) = \sum_i \left( \frac{T_i - f(t_i, r)}{\sigma_i} \right)^2
\]

La valeur de \( r \) qui **minimise** \( \chi^2 \) est considérée comme la **meilleure estimation**.  
L’**incertitude** sur \( r \) est déterminée comme l’intervalle où \( \chi^2(r) = \chi^2_{\min} + 1 \).

---

## 📁 Contenu du projet

| Fichier                  | Description |
|-------------------------|-------------|
| `Avec_r_direct.py`      | Utilise une série de valeurs de \( r_i \) et leurs incertitudes pour estimer une moyenne pondérée par minimisation de χ² |
| `Avec_Ti_modele.py`     | Ajuste le paramètre \( r \) dans le modèle de Newton à partir des données \( T_i \) mesurées dans le temps |
| `data.csv`              | Fichier de données au format attendu (à fournir) |

---

## 🔎 Description des deux approches

### 1. `Avec_r_direct.py` – Moyenne pondérée des valeurs de r

- Données : plusieurs valeurs expérimentales de \( r_i \), chacune avec une incertitude \( \sigma_i \)
- Objectif : déterminer une valeur optimale de \( r \) en minimisant :

  \[
  \chi^2(r) = \sum_i \left( \frac{r_i - r}{\sigma_i} \right)^2
  \]

- Permet de comparer avec une méthode analytique (dérivées partielles)

**Format du fichier attendu** :
0,000134;0,000012
0,000145;0,000013


---

### 2. `Avec_Ti_modele.py` – Ajustement d’un modèle exponentiel à T(t)

- Données : températures \( T_i \) mesurées à différents temps \( t_i \)
- Objectif : ajuster \( r \) dans le modèle de Newton :

  \[
  T(t) = T_{\text{env}} + (T_0 - T_{\text{env}}) \cdot e^{-r t}
  \]

- Méthode : minimisation de \( \chi^2(r) \) avec incertitude constante sur chaque \( T_i \)

**Format du fichier attendu** :

---

## 📦 Installation

Dépendances :

```bash
pip install numpy pandas matplotlib scipy
python Avec_r_direct.py      # si vous avez des r_i + incertitudes
python Avec_Ti_modele.py     # si vous avez des T_i mesurés dans le temps
