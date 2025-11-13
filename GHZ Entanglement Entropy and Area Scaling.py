import qutip as qt
import numpy as np

def ghz_state(n):
    """Generate n-mode GHZ state |n_L> = 1/sqrt(2) (|0>^n + |1>^n)"""
    if n == 0:
        return qt.fock(1, 0)  # Vacuum mode
    zero = qt.basis(2, 0)
    one = qt.basis(2, 1)
    state = (qt.tensor([zero] * n) + qt.tensor([one] * n)).unit()
    return state

results = []
for n in range(7):  # n=0 to 6
    psi = ghz_state(n)
    rho = psi * psi.dag()
    
    # Bipartite entropy (first n//2 modes)
    if n > 0:
        ptrace_idx = list(range(n // 2))
        rho_A = rho.ptrace(ptrace_idx)
        S = qt.entropy_vn(rho_A)
    else:
        S = 0.0
    
    # Analytic area (Area = max(n, 1) * 2π, ℏ=1)
    area = max(n, 1) * 2 * np.pi
    
    results.append((n, S, area))
    print(f"n={n:2d} | Entropy S={S:.6f} (nats) | Area={area:.2f}")

# Summary table
print("\n| n | Bipartite Entropy S (nats) | Area Estimate (≈ n × 2π) |")
print("|---|-----------------------------|---------------------------|")
for n, S, area in results:
    print(f"| {n} | {S:.3f} | {area:.2f} |")