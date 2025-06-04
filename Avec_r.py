import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# === Étape 1 : Lecture du fichier CSV (sans en-tête, séparateur ;, virgules décimales) ===
df = pd.read_csv("data.csv", sep=";", header=None)
df.columns = ["r", "uncertainty"]

# Conversion des virgules en points et en float
df["r"] = df["r"].str.replace(",", ".").astype(float)
df["uncertainty"] = df["uncertainty"].str.replace(",", ".").astype(float)

# Extraction des données
r_values = df["r"].values
sigma_values = df["uncertainty"].values

# === Étape 2 : Définir la fonction χ² ===
def chi2(r):
    return np.sum(((r_values - r) / sigma_values) ** 2)

# === Étape 3 : Minimisation de χ² pour trouver r_opt ===
res = minimize_scalar(chi2, bounds=(min(r_values), max(r_values)), method="bounded")
r_opt = res.x
chi2_min = res.fun

print(f"\n✅ Valeur optimale de r : {r_opt:.8f}")
print(f"✅ χ² minimum : {chi2_min:.4f}")

# === Étape 4 : Tracé de la courbe χ²(r) ===
r_grid = np.linspace(r_opt - r_opt * 0.5, r_opt + r_opt * 0.5, 1000)
chi2_grid = np.array([chi2(r) for r in r_grid])

plt.plot(r_grid, chi2_grid, label="χ²(r)")
plt.axvline(r_opt, color='green', linestyle='--', label='r optimal')
plt.axhline(chi2_min + 1, color='red', linestyle='--', label='χ²_min + 1')
plt.xlabel("r")
plt.ylabel("χ²(r)")
plt.title("Minimisation du χ² pour estimer r")
plt.legend()
plt.grid(True)
plt.show()

# === Étape 5 : Détermination de l'incertitude sur r ===
threshold = chi2_min + 1
above = chi2_grid > threshold
crossings = np.where(np.diff(above.astype(int)) != 0)[0]

if len(crossings) >= 2:
    r_low = np.interp(threshold,
                      [chi2_grid[crossings[0]], chi2_grid[crossings[0] + 1]],
                      [r_grid[crossings[0]], r_grid[crossings[0] + 1]])
    r_high = np.interp(threshold,
                       [chi2_grid[crossings[1]], chi2_grid[crossings[1] + 1]],
                       [r_grid[crossings[1]], r_grid[crossings[1] + 1]])
    uncertainty = (r_high - r_low) / 2
    uncertaintyElarg: = uncertainty * 2
    print(f"✅ Incertitude sur r : ±{uncertaintyElarg:.8f}")

    # === Étape 6 : Calcul de χ²(r₀ ± ε) ===
    r_plus = r_opt + uncertainty
    r_minus = r_opt - uncertainty
    chi2_plus = chi2(r_plus)
    chi2_minus = chi2(r_minus)

    print(f"r₀ + ε = {r_plus:.12f} → χ²(r₀ + ε) = {chi2_plus:.12f}")
    print(f"r₀ - ε = {r_minus:.12f} → χ²(r₀ - ε) = {chi2_minus:.12f}")


else:
    print("❌ Impossible de déterminer une incertitude : pas d'intersection avec χ²_min + 1.")
