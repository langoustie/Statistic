import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

# === Constantes connues ===
T_env = 20.68
sigma_T = 1 / 2 * np.sqrt(3)  # incertitude constante

# === Lecture du fichier CSV ===
df = pd.read_csv("data3.csv", sep=";", header=None)
df.columns = ["t", "T"]

# Conversion virgule -> point et en float
for col in df.columns:
    df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

df = df.dropna()  # sécurité

t_values = df["t"].values
T_values = df["T"].values
T0 = T_values[0]  # température initiale

# === Modèle de Newton ===
def T_model(t, r):
    return T_env + (T0 - T_env) * np.exp(-r * t)

# === Fonction χ² ===
def chi2(r):
    model = T_model(t_values, r)
    if np.any(np.isnan(model)) or np.any(np.isinf(model)):
        return np.inf
    residuals = (T_values - model) / sigma_T
    return np.sum(residuals**2)

# === Minimisation de χ² ===
res = minimize_scalar(chi2, bounds=(1e-6, 0.01), method="bounded")
r_opt = res.x
chi2_min = res.fun

print(f"\n✅ Valeur optimale de r : {r_opt:.8f}")
print(f"✅ χ² minimum : {chi2_min:.4f}")

# === Tracé de χ²(r) ===
r_grid = np.linspace(r_opt - r_opt * 0.5, r_opt + r_opt * 0.5, 1000)
chi2_grid = np.array([chi2(r) for r in r_grid])

plt.plot(r_grid, chi2_grid, label="χ²(r)")
plt.axvline(r_opt, color='green', linestyle='--', label='r optimal')
plt.axhline(chi2_min + 1, color='red', linestyle='--', label='χ²_min + 1')
plt.xlabel("r")
plt.ylabel("χ²(r)")
plt.title("Ajustement du modèle de Newton (χ²)")
plt.legend()
plt.grid(True)
plt.show()

# === Détermination de l'incertitude (χ² = χ²_min + 1) ===
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

    r_plus = r_opt + uncertainty
    r_minus = r_opt - uncertainty
    chi2_plus = chi2(r_plus)
    chi2_minus = chi2(r_minus)

    print(f"✅ Incertitude sur r : ±{uncertainty:.8f}")
    print(f"r₀ + ε = {r_plus:.12f} → χ²(r₀ + ε) = {chi2_plus:.12f}")
    print(f"r₀ - ε = {r_minus:.12f} → χ²(r₀ - ε) = {chi2_minus:.12f}")
else:
    print("❌ Impossible de déterminer une incertitude : pas d'intersection avec χ²_min + 1.")
