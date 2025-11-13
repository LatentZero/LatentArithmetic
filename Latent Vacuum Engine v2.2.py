#!/usr/bin/env python3
"""
LATENT VACUUM ENGINE v2.2 — FIXED FOR WINDOWS (UTF-8)
"""

import numpy as np
import csv

# ============================
# PARAMETERS
# ============================
M_initial = 1.0
N_MAX = 6
CYCLES = 100000
LOG_FILE = "lve_log_v2.2_100k.csv"
ANOMALY_FILE = "anomaly_report_v2.2_100k.txt"
T_HOM = 0.8
DCE_DRIVE_BASE = 1e-6
DCE_FACTOR = 1.0 / (8 * np.pi)
dt = 1.0
M_PLANCK_CORE = 0.05
WHITE_HOLE_BURST_FREQ = 1.0

# ============================
# CORE FUNCTIONS
# ============================
def measure_hom_visibility(T):
    return T

def apply_dce_drive(V, M):
    if M <= 0:
        return 0.0
    return DCE_DRIVE_BASE * V / (M ** 3)

def compute_dNdt(f_dot):
    return f_dot ** 2 * DCE_FACTOR

def update_mass(M, dNdt, dt):
    if M <= M_PLANCK_CORE:
        return M
    dMdt = -1.0 / (15360 * np.pi * M**2)
    return M + dMdt * dt

# ============================
# INITIALIZE LOG (UTF-8 SAFE)
# ============================
with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'cycle', 'n', 'area_sim', 'area_expected', 'V_hom', 'f_dot',
        'dNdt', 'dMdt', 'M', 'anomaly'
    ])

anomalies = []
np.random.seed(42)
M = M_initial
white_hole_count = 0

print("LATENT VACUUM ENGINE v2.2 — Running 100,000 cycles...")

# ============================
# MAIN LOOP
# ============================
for cycle in range(CYCLES):
    n = np.random.randint(0, N_MAX + 1)
    area_sim = area_expected = max(n, 1) * 2 * np.pi
    V = measure_hom_visibility(T_HOM)
    f_dot = apply_dce_drive(V, M)
    dNdt = compute_dNdt(f_dot)
    M_new = update_mass(M, dNdt, dt)
    dMdt = (M_new - M) / dt
    M = M_new

    anomaly = ""
    if abs(area_sim - area_expected) > 1e-10:
        anomaly += "AREA_DRIFT "
    if dNdt > 1e-6:
        anomaly += "DCE_ANOMALY "
    if M <= M_PLANCK_CORE:
        anomaly += "WHITE_HOLE_BURST "
        # Use plain text instead of ν
        anomalies.append(f"Cycle {cycle}: WHITE HOLE #{white_hole_count + 1} at freq={WHITE_HOLE_BURST_FREQ:.1e} Hz")
        white_hole_count += 1
        M = M_initial

    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            cycle, n, f"{area_sim:.6f}", f"{area_expected:.6f}",
            f"{V:.3f}", f"{f_dot:.2e}", f"{dNdt:.2e}",
            f"{dMdt:.2e}", f"{M:.6f}", anomaly
        ])

    if cycle % 10000 == 0:
        print(f"Cycle {cycle:5d} | n={n} | Area={area_sim:.2f} | M={M:.6f} | dN/dt={dNdt:.2e} | Bursts={white_hole_count}")

# ============================
# FINAL REPORT (UTF-8 + NO GREEK LETTERS)
# ============================
with open(ANOMALY_FILE, 'w', encoding='utf-8') as f:
    if anomalies:
        f.write("WHITE HOLE BURSTS DETECTED:\n")
        f.write("\n".join(anomalies))
    else:
        f.write("NO ANOMALIES — CLEAN EVAPORATION\n")

print(f"\nSimulation complete!")
print(f"  → White hole bursts: {white_hole_count}")
print(f"  → Log: {LOG_FILE}")
print(f"  → Report: {ANOMALY_FILE}")