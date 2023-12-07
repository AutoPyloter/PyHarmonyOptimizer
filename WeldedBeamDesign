from PyHarmonyOptimizer import *

class WeldedBeamDesign:
    E = 30 * 10**6  # Young Modülü
    G = 12 * 10**6  # Kayma Modülü
    P = 6000        # Yük
    L = 14          # Kiriş uzunluğu
    Tomax = 13600   # Maksimum kesme gerilmesi
    Sigmamax = 30000 # Maksimum normal gerilme
    Deltamax = 0.25  # Maksimum yer değiştirme
    NG = 7         # Kısıtlama sayısı

    def __init__(self, x1, x2, x3, x4):
        self.x1 = x1  # Kiriş genişliği
        self.x2 = x2  # Kiriş yüksekliği
        self.x3 = x3  # Kiriş kalınlığı
        self.x4 = x4  # Kaynak genişliği

    def compute_penalty(self):
        delta_x = (4 * self.P * self.L**3) / (self.E * self.x3**3 * self.x4)
        sigma_x = (6 * self.P * self.L) / (self.x4 * self.x3**2)
        Pc = (4.013 * self.E * ((self.x3**2 * self.x4**6) / 36)**0.5) / (self.L**2) * (1 - self.x3 / (2 * self.L) * (self.E / (4 * self.G))**0.5)
        M = self.P * (self.L + self.x2 / 2)
        R = ((self.x2)**2 / 4 + ((self.x1 + self.x3) / 2)**2)**0.5
        J = 2 * self.x1 * self.x2 * ((self.x2**2) / 12 + ((self.x1 + self.x3) / 2)**2)
        To1 = self.P / (self.x1 * self.x2 * 2**0.5)
        To2 = M * R / J
        Tox = ((To1)**2 + (To2)**2 + 2 * self.x2 * To1 * To2 / (2 * R))**0.5

        constraints = [
            Tox - self.Tomax,
            sigma_x - self.Sigmamax,
            self.x1 - self.x4,
            0.10471 * self.x1**2 + 0.04811 * self.x3 * self.x4 * (14 + self.x2) - 5,
            0.125 - self.x1,
            delta_x - self.Deltamax,
            self.P - Pc
        ]

        penalties = 0
        for constraint in constraints[:self.NG]:
            if constraint > 0:
                penalties += constraint

        return penalties

    def fitness(self):
        penalty = self.compute_penalty()
        The_fitness=1.10471 * self.x1**2 * self.x2 + 0.04811 * self.x3 * self.x4 * (14 + self.x2)
        if penalty > 0:
            The_Reference=penalty+10
        else:
            The_Reference=The_fitness
        return The_Reference, The_fitness,penalty

def optimize_beam_design():
    design = {
        'x1': Continuous(0.1, 2),
        'x2': Continuous(0.1, 10),
        'x3': Continuous(0.1, 10),
        'x4': Continuous(0.1, 2)
    }

    def objective_function(harmony):
        beam = WeldedBeamDesign(harmony['x1'], harmony['x2'], harmony['x3'], harmony['x4'])
        return beam.fitness()

    optimizer = Minimization(design, objective_function)
    best_solution = optimizer.optimize(max_iter=2000,memory_size=500,PAR=0.4,HMCR=0.7,log=False)
    return best_solution

def print_solution(solution):
    harmony, fitness = solution
    print("En iyi çözümün detayları:")
    for key, value in harmony.items():
        print(f"  {key}: {value}")
        pass
    print(f"Fitness değeri: {fitness}")
    return fitness[0]

try:
   for a in range(10000):
        print(a,". run:")
        best_solution = optimize_beam_design()
        thePrint=print_solution(best_solution)
        if thePrint < 1.9229156516342583:
            quit()
except Exception as e:
    print(f"Bir hata oluştu: {e}")
