import random
from abc import ABC, abstractmethod

class Sampler(ABC):
    @abstractmethod
    def sample(self):
        pass

class Continuous(Sampler):
    def __init__(self, min_val, max_val):
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
    def __init__(self, value):
        self.value = value

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

    def initialize_harmony_memory(self, size):
        for _ in range(size):
            harmony = {var: self.design[var].sample() for var in self.design}
            self.harmony_memory.append((harmony, self.objective(harmony)))

    def generate_new_harmony(self, HMCR, PAR):
        new_harmony = {}
        for var in self.design:
            if random.random() < HMCR:
                new_harmony[var] = random.choice([h[0][var] for h in self.harmony_memory])
            else:
                new_harmony[var] = self.design[var].sample()
            if random.random() < PAR:
                new_harmony[var] = self.design[var].sample()
        return new_harmony

    @abstractmethod
    def optimize(self, HMCR, PAR, memory_size, max_iter):
        pass

class Minimization(Optimization):
    def optimize(self, HMCR, PAR, memory_size, max_iter):
        self.initialize_harmony_memory(memory_size)
        for _ in range(max_iter):
            new_harmony = self.generate_new_harmony(HMCR, PAR)
            new_fitness = self.objective(new_harmony)
            worst_harmony = max(self.harmony_memory, key=lambda x: x[1])
            if worst_harmony[1] > new_fitness:
                self.harmony_memory.remove(worst_harmony)
                self.harmony_memory.append((new_harmony, new_fitness))
        return min(self.harmony_memory, key=lambda x: x[1])

class Maximization(Optimization):
    def optimize(self, HMCR, PAR, memory_size, max_iter):
        self.initialize_harmony_memory(memory_size)
        for _ in range(max_iter):
            new_harmony = self.generate_new_harmony(HMCR, PAR)
            new_fitness = self.objective(new_harmony)
            worst_harmony = min(self.harmony_memory, key=lambda x: x[1])
            if worst_harmony[1] < new_fitness:
                self.harmony_memory.remove(worst_harmony)
                self.harmony_memory.append((new_harmony, new_fitness))
        return max(self.harmony_memory, key=lambda x: x[1])