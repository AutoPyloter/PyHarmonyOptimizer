from PyHarmonyOptimizer import *
import math
from functools import lru_cache

class WeldedBeamDesign:
    YOUNGS_MODULUS = 30e6
    SHEAR_MODULUS = 12e6
    MAX_ITERATIONS = 10000
    MEMORY_SIZE = 50
    PAR_PARAMETER = 0.1
    HMCR_PARAMETER = 0.9
    LOAD = 6000
    BEAM_LENGTH = 14
    MAX_SHEAR_STRESS = 13600
    MAX_NORMAL_STRESS = 30000
    MAX_DISPLACEMENT = 0.25
    NUMBER_OF_CONSTRAINTS = 7
    RUN = 1
    ISLOG=True
    SHOWMEMORY=True
    OUTPUT_FILE = "output.txt"

    def __init__(self, beam_width, beam_height, beam_thickness, weld_width):
        self.beam_width, self.beam_height, self.beam_thickness, self.weld_width = beam_width, beam_height, \
                                                                                  beam_thickness, weld_width

    def compute_penalty(self):
        p, l, ee, g, x1, x2, x3, x4 = [self.LOAD, self.BEAM_LENGTH, self.YOUNGS_MODULUS, self.SHEAR_MODULUS,
                                       self.beam_width, self.beam_height, self.beam_thickness, self.weld_width]

        delta_x = (4 * p * l ** 3) / (ee * x3 ** 3 * x4)
        sigma_x = (6 * p * l) / (x4 * x3 ** 2)
        pc = (4.013 * ee * ((x3 ** 2 * x4 ** 6) / 36) ** 0.5) / (l ** 2) * (1 - x3 / (2 * l) * (ee / (4 * g)) ** 0.5)
        m = p * (l + x2 / 2)
        r = (x2 ** 2 / 4 + ((x1 + x3) / 2) ** 2) ** 0.5
        j = 2 * (x1 * x2 * 2 ** 0.5 * ((x2 ** 2) / 12 + ((x1 + x3) / 2) ** 2))
        to1 = p / (x1 * x2 * 2 ** 0.5)
        to2 = m * r / j
        tox = (to1 ** 2 + to2 ** 2 + 2 * x2 * to1 * to2 / (2 * r)) ** 0.5

        constraints = [
            tox - self.MAX_SHEAR_STRESS,
            sigma_x - self.MAX_NORMAL_STRESS,
            self.beam_width - self.weld_width,
            0.10471 * self.beam_width ** 2 +
            0.04811 * self.beam_thickness * self.weld_width * (14 + self.beam_height) - 5,
            0.125 - self.beam_width,
            delta_x - self.MAX_DISPLACEMENT,
            self.LOAD - pc
        ]

        penalties = sum(max(0, constraint) for constraint in constraints[:self.NUMBER_OF_CONSTRAINTS])
        return penalties
    @lru_cache(maxsize=None)
    def fitness(self):
        penalty = self.compute_penalty()
        the_fitness = 1.10471 * self.beam_width ** 2 * self.beam_height + 0.04811 * self.beam_thickness * self. \
            weld_width * (14 + self.beam_height)
        the_reference = penalty*1000+3  if penalty > 0 else the_fitness
        return the_reference, the_fitness, penalty

    @staticmethod
    def optimize_beam_design():
        design = {'beam_width': Continuous(0.1, 2),
                  'beam_height': Continuous(0.1, 10),
                  'beam_thickness': Continuous(0.1, 10),
                  'weld_width': Continuous(0.1, 2)}

        def objective_function(harmony):
            beam = WeldedBeamDesign(harmony['beam_width'], harmony['beam_height'], harmony['beam_thickness'],
                                    harmony['weld_width'])
            return beam.fitness()

        optimizer = Minimization(design, objective_function)
        
        runing=optimizer.optimize(max_iter=WeldedBeamDesign.MAX_ITERATIONS,
                                  memory_size=WeldedBeamDesign.MEMORY_SIZE,
                                  par=WeldedBeamDesign.PAR_PARAMETER,
                                  hmcr=WeldedBeamDesign.HMCR_PARAMETER,
                                  log=WeldedBeamDesign.ISLOG)
        if WeldedBeamDesign.SHOWMEMORY:
            optimizer.print_harmony_memory()
        return runing
        

    @staticmethod
    def print_solution(solution, file=None):
        harmony, fitness = solution
        output = f"Details of the best solution:\n"
        output += '\n'.join([f"  {key}: {value}" for key, value in harmony.items()])
        output += f"\nFitness value: {fitness}\n\n"

        print(output)
        if file:
            with open(file, 'a') as f:
                # f.write(output)
                pass
        return fitness[0]


def get_fitness_for_specific_design(beam_width, beam_height, beam_thickness, weld_width):
    design = WeldedBeamDesign(beam_width, beam_height, beam_thickness, weld_width)
    reference, fitness, penalty = design.fitness()
    print(f"Design Parameters:\n"
          f"  Beam Width: {beam_width}\n"
          f"  Beam Height: {beam_height}\n"
          f"  Beam Thickness: {beam_thickness}\n"
          f"  Weld Width: {weld_width}\n"
          f"Fitness Value: {fitness}\n"
          f"Penalty: {penalty}\n"
          f"Reference Value: {reference}")


if __name__ == "__main__":
    try:
        for run_number in range(WeldedBeamDesign.RUN):
            print(f"{run_number + 1}. run:")
            current_solution = WeldedBeamDesign.optimize_beam_design()
            WeldedBeamDesign.print_solution(current_solution, WeldedBeamDesign.OUTPUT_FILE)
        #get_fitness_for_specific_design(0.206741, 3.65285, 8.54856, 0.231265)
    except Exception as e:
        print(f"An error occurred: {e}")
