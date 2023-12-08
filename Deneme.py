from PyHarmonyOptimizer import *

class OptimizasyonProblemi:
    # Constructor with the design variables limits
    def __init__(self, x1, x2, x3, x4):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4

    # Objective function definition
    def fitness(self):
        return 0.6224 * self.x1 * self.x3 * self.x4 + 1.7781 * self.x2**2 * self.x3 + 3.1661 * self.x1**2 * self.x4 + 19.8621 * self.x1 * self.x3**2

    # Constraints function definition
    def compute_penalty(self):
        penalties = 0
        g1 = -self.x1 + 0.0193 * self.x3
        g2 = -self.x2 + 0.00954 * self.x3
        g3 = -3.141592653589793 * self.x3**2 * self.x4 - (4/3) * 3.141592653589793 * self.x3**3 + 1_296_000
        g4 = self.x4 - 240

        # Check if constraints are violated and apply penalties if so
        for g in [g1, g2, g3, g4]:
            if g > 0:
                penalties += g

        return penalties

    # General fitness value calculation function definition
    def evaluate(self):
        try:
            penalty = self.compute_penalty()
            fitness = self.fitness()
            the_reference = fitness + penalty if penalty > 0 else fitness
            return the_reference
        except Exception as e:
            print(f"An error occurred during evaluation: {e}")
            return float('inf')  # Return a high value to represent a bad solution in case of an error

# Optimization function definition
def optimize_design():
    design = {
        'x1': Continuous(0.1, 2.0),  # Limits for x1
        'x2': Continuous(0.1, 2.0),  # Limits for x2
        'x3': Continuous(0.1, 2.0),  # Limits for x3
        'x4': Continuous(0.1, 2.0),  # Limits for x4
    }

    def objective_function(harmony):
        problem = OptimizasyonProblemi(harmony['x1'], harmony['x2'], harmony['x3'], harmony['x4'])
        return problem.evaluate()

    optimizer = Minimization(design, objective_function)
    best_solution = optimizer.optimize(max_iter=2000, memory_size=500, PAR=0.4, HMCR=0.7, log=False)
    return best_solution

# Function to print the best solution details
def print_solution(solution):
    harmony, fitness = solution
    print("En iyi çözümün detayları:")
    for key, value in harmony.items():
        print(f"  {key}: {value:.4f}")
    print(f"Fitness değeri: {fitness}")

# Run the optimization function and print results
if __name__ == "__main__":
    try:
        best_solution = optimize_design()
        print_solution(best_solution)
    except Exception as e:
        print(f"Optimization failed with error: {e}")
