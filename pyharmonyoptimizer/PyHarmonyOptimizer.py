#PyHarmonyOptimizer.py
import random
import types
from abc import ABC, abstractmethod


class Sampler(ABC):

    @abstractmethod
    def sample(self):
        pass


class Continuous(Sampler):

    def __init__(self, *args):
        min_val, max_val = args
        self.min_val = min_val
        self.max_val = max_val
    def sample(self):
        return random.uniform(self.min_val, self.max_val)


class Discrete(Sampler):

    def __init__(self, values):
        self.values = values

    def sample(self):
        return random.choice(self.values)


class Constant(Sampler):

    def __init__(self, *args):
        self.value = args[0]

    def sample(self):
        return self.value

class Categorical(Sampler):

    def __init__(self, categories): 
        self.categories = categories

    def sample(self):
        return random.choice(self.categories)




class Optimization(ABC):

    def __init__(self, design, objective):

        self.design = design
        self.objective = objective
        self.harmony_memory = []
        self.fitness_memory = []
        self.penalty_memory = []
        self.best_fit = None
        self.best_index = None
        self.worst_fit = None
        self.worst_index = None
        

    def initialize_harmony_memory(self, size):

        for _ in range(size):
            harmony = {var: self.design[var].sample() for var in self.design}
            fitness, penalty = self.objective(harmony)

            self.harmony_memory.append(harmony)
            self.fitness_memory.append(fitness)
            self.penalty_memory.append(penalty)
        self.find_best_worst(size)



    def find_best_worst(self, HMS):

        valid_inds = [i for i, p in enumerate(self.penalty_memory) if p <= 0]
        number_of_valid = len(valid_inds)

        if number_of_valid == 0:  # Hepsi geçersiz çözüm ise
            self.best_index = self.penalty_memory.index(min(self.penalty_memory))
            self.best_fit = self.fitness_memory[self.best_index]
            self.worst_index = max((idx for idx, val in enumerate(self.penalty_memory) if idx != self.best_index), key=lambda idx: self.penalty_memory[idx])
            self.worst_fit = self.fitness_memory[self.worst_index]
        elif number_of_valid == HMS:  # Hepsi geçerli çözüm ise
            self.best_fit, self.best_index = min((fit, idx) for (idx, fit) in enumerate(self.fitness_memory))
            self.worst_fit, self.worst_index = max((fit, idx) for (idx, fit) in enumerate(self.fitness_memory) if idx != self.best_index)
        else:  # Kimi geçerli kimi geçersiz ise
            self.worst_index = self.penalty_memory.index(max(self.penalty_memory))
            self.worst_fit = self.fitness_memory[self.worst_index]
            valid_fitness = [self.fitness_memory[i] for i in valid_inds]
            self.best_fit, temp_index = min((fit, idx) for (idx, fit) in enumerate(valid_fitness))
            self.best_index = valid_inds[temp_index]

    def generate_new_harmony(self, hmcr, par):

        new_harmony = {}
        for var in self.design:

            if random.random() < hmcr:
                new_harmony[var] = random.choice([h[var] for h in self.harmony_memory])
            else:
                new_harmony[var] = self.design[var].sample()

            if random.random() < par:
                new_harmony[var] = self.design[var].sample()
        return new_harmony
    
    def update_harmony_memory(self, new_harmony):
        new_fitness, new_penalty = self.objective(new_harmony)

        if new_penalty > 0 and self.penalty_memory[self.worst_index] > 0:
            if new_penalty < self.penalty_memory[self.worst_index]:
                self.harmony_memory[self.worst_index] = new_harmony
                self.fitness_memory[self.worst_index] = new_fitness
                self.penalty_memory[self.worst_index] = new_penalty

        elif new_penalty <= 0 and self.penalty_memory[self.worst_index] <= 0:
            if new_fitness < self.worst_fit:
                self.harmony_memory[self.worst_index] = new_harmony
                self.fitness_memory[self.worst_index] = new_fitness
                self.penalty_memory[self.worst_index] = new_penalty

        elif new_penalty <= 0 and self.penalty_memory[self.worst_index] > 0:
            self.harmony_memory[self.worst_index] = new_harmony
            self.fitness_memory[self.worst_index] = new_fitness
            self.penalty_memory[self.worst_index] = new_penalty
        self.find_best_worst(len(self.harmony_memory))
        
    

class Minimization(Optimization):

    def optimize(self, hmcr=0.8, par=0.3, memory_size=20, max_iter=1000, log=False):
        self.initialize_harmony_memory(memory_size)
        out=""
        for index in range(max_iter):
            new_harmony = self.generate_new_harmony(hmcr, par)
            self.update_harmony_memory(new_harmony)

            if log:
                best_harmony = self.harmony_memory[self.best_index]
                best_penalty = self.penalty_memory[self.best_index]
                
                out=(f"Iteration {index+1}, Harmony: {best_harmony}, Fitness: {self.best_fit}, Penalty: {best_penalty}")
                if log:
                    print(out)
        return out,self.best_fit
        
