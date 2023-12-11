from PyHarmonyOptimizer import *

# Amaç Fonksiyonu
def objective_function(harmony):
    A, B, C, D = harmony['A'], harmony['B'], harmony['C'], harmony['D']
    return A + B + C if D == "yukarı" else A - B - C

# Tasarım Değişkenleri
design = {
    'A': Discrete([0, 1, 3]),
    'B': Discrete([1, 1.5, 2, 2.5, 3, 3.5]),
    'C': Continuous(4, 5),
    'D': Categorical(["yukarı", "aşağı"])
}

# Optimizasyon
optimizer = Minimization(design, objective_function)
best_solution = optimizer.optimize(hmcr=0.8, par=0.3, memory_size=10, max_iter=100)
print("En iyi çözüm:", best_solution)
