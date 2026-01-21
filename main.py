import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Section print
def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

# === Load data ===
growth_data = pd.read_csv("growth_data.csv")
batch_data = pd.read_csv("batch_fluoride_data.csv")
rfb_data = pd.read_csv("rfb_breakthrough_data.csv")

# === Growth analysis ===
section("1. BACTERIAL GROWTH UNDER FLUORIDE STRESS")

print(growth_data)

plt.figure()
for col in growth_data.columns[1:]:
    plt.plot(
        growth_data.iloc[:, 0],
        growth_data[col],
        marker="o",
        label=col.replace("_mgL", "").replace("OD_", "") + " mg/L"
    )

plt.xlabel("Time (h)")
plt.ylabel("OD600")
plt.title("Growth Curve Under Fluoride Stress")
plt.legend(title="Fluoride")
plt.grid(True)
plt.show()

# === Batch kinetics ===
section("2. BATCH FLUORIDE REMOVAL KINETICS")

C0 = batch_data["Initial_Fluoride_mgL"].iloc[0]

batch_data["Removal_%"] = (C0 - batch_data["Final_Fluoride_mgL"]) / C0 * 100
batch_data["ln_Ct_C0"] = np.log(batch_data["Final_Fluoride_mgL"] / C0)

print(batch_data)

slope, intercept, r, _, _ = linregress(
    batch_data["Time_hours"],
    batch_data["ln_Ct_C0"]
)
k = -slope

print(f"\nRate constant k = {k:.4f} h⁻¹")
print(f"R² = {r**2:.4f}")

plt.figure()
plt.plot(batch_data["Time_hours"], batch_data["ln_Ct_C0"], "o", label="Data")
plt.plot(
    batch_data["Time_hours"],
    intercept + slope * batch_data["Time_hours"],
    label="Fit"
)
plt.xlabel("Time (h)")
plt.ylabel("ln(Ct / C0)")
plt.title("Fluoride Removal Kinetics")
plt.legend()
plt.grid(True)
plt.show()

# === RFB analysis ===
section("3. REVERSIBLE FLUIDISED BED PERFORMANCE")

rfb_data["Cout_Cin"] = rfb_data["Cout_mgL"] / rfb_data["Cin_mgL"]
print(rfb_data)

plt.figure()
plt.plot(rfb_data["Time_h"], rfb_data["Cout_Cin"], marker="s")
plt.axhline(0.1, linestyle="--", label="Breakthrough")
plt.axhline(0.9, linestyle="--", label="Exhaustion")

plt.xlabel("Time (h)")
plt.ylabel("Cout / Cin")
plt.title("Fluoride Breakthrough Curve (RFB)")
plt.legend()
plt.grid(True)
plt.show()

section("ANALYSIS COMPLETED")

print(" The analysis was succesfull, Report by Truptimayee ")
