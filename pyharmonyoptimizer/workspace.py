import random
from abc import ABC, abstractmethod

# Örnekleyici sınıflar
class Sampler(ABC):
    @abstractmethod
    def sample(self, dependency_values={}):
        pass

class Continuous(Sampler):
    def __init__(self, min_val, max_val, dependencies=None):
        self.min_val = min_val
        self.max_val = max_val
        self.dependencies = dependencies or {}

    def sample(self, dependency_values={}):
        # Bağımlı değişken değerlerini güncelle
        updated_dependencies = {key: (float(dependency_values[value]) if value in dependency_values else self.dependencies[value]) for key, value in self.dependencies.items()}
        
        # Güncellenmiş min ve max değerlerini kullan
        min_val = updated_dependencies.get('min_val', self.min_val)
        max_val = updated_dependencies.get('max_val', self.max_val)
        return random.uniform(min_val, max_val)
    def select_compatible_sample(self, samples, dependency_values):
        compatible_samples = []
        for sample in samples:
            if all(self.is_compatible(dependency_values, dep_var, sample) for dep_var in self.dependencies.keys()):
                compatible_samples.append(sample)
        return compatible_samples

    def is_compatible(self, dependency_values, dep_var, sample_value):
        # Bağımlı değişkenlere uygun olup olmadığını kontrol et
        min_val = dependency_values.get(f'min_{dep_var}')
        max_val = dependency_values.get(f'max_{dep_var}')

        if min_val is not None and sample_value < min_val:
            return False
        if max_val is not None and sample_value > max_val:
            return False

        return True
class Discrete(Sampler):
    def __init__(self, values, dependencies=None):
        self.values = values
        self.dependencies = dependencies or {}

    def sample(self, dependency_values={}):
        updated_dependencies = {key: (float(dependency_values[value]) if isinstance(dependency_values.get(value), (int, float)) else self.dependencies[value]) for key, value in self.dependencies.items()}
        min_val = updated_dependencies.get('min_val', min(self.values))
        max_val = updated_dependencies.get('max_val', max(self.values))

        valid_values = [val for val in self.values if min_val <= val <= max_val]
        return random.choice(valid_values) if valid_values else None

    def select_compatible_sample(self, samples, dependency_values):
        compatible_samples = []
        for sample in samples:
            if all(self.is_compatible(dependency_values, dep_var, sample) for dep_var in self.dependencies.keys()):
                compatible_samples.append(sample)
        return compatible_samples

    def is_compatible(self, dependency_values, dep_var, sample_value):
        # Bağımlı değişkenlere uygun olup olmadığını kontrol et
        min_val = dependency_values.get(f'min_{dep_var}')
        max_val = dependency_values.get(f'max_{dep_var}')

        if min_val is not None and sample_value < min_val:
            return False
        if max_val is not None and sample_value > max_val:
            return False

# Discrete, Constant, Categorical sınıflarınızı benzer şekilde güncelleyebilirsiniz

# Optimizasyon sınıfı
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
            harmony = {}
            dependency_values = {}
            for var in self.design:
                harmony[var] = self.design[var].sample(dependency_values)
                dependency_values[var] = harmony[var]
            print(harmony)
            fitness, penalty = self.objective(harmony)
            self.harmony_memory.append(harmony)
            self.fitness_memory.append(fitness)
            self.penalty_memory.append(penalty)

        self.find_best_worst(size)

    def generate_new_harmony(self, hmcr, par):
        new_harmony = {}
        dependency_values = {}
        for var in self.design:
            if random.random() < hmcr:
                # Uyum hafızasındaki örnekler
                samples = [h[var] for h in self.harmony_memory]

                # Bağımlı değişkenlere uygun örnekleri seç
                compatible_samples = self.design[var].select_compatible_sample(samples, dependency_values)
                #print(compatible_samples)

                if compatible_samples:
                    new_harmony[var] = random.choice(compatible_samples)
                else:
                    new_harmony[var] = self.design[var].sample(dependency_values)
            else:
                new_harmony[var] = self.design[var].sample(dependency_values)

            if random.random() < par:
                new_harmony[var] = self.design[var].sample(dependency_values)

            dependency_values[var] = new_harmony[var]

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


class Minimization(Optimization):
    def optimize(self, hmcr=0.8, par=0.3, memory_size=20, max_iter=1000, log=False):
        self.initialize_harmony_memory(memory_size)
        for index in range(max_iter):
            new_harmony = self.generate_new_harmony(hmcr, par)
            self.update_harmony_memory(new_harmony)

            if log:
                best_harmony = self.harmony_memory[self.best_index]
                best_penalty = self.penalty_memory[self.best_index]
                print(f"Iteration {index+1}, Harmony: {best_harmony}, Fitness: {self.best_fit}, Penalty: {best_penalty}")

# Tasarım alanı ve hedef fonksiyon
design_space = {
    'x1': Continuous(0.1, 2),
    'x2': Continuous(2, 100),
    'x3': Discrete([1, 2, 3, 4, 5,9]),
    'x4': Discrete([1, 2, 3, 4, 5,9], dependencies={'min_val': 'x3'})
}

def obj_func(harmony):
    x1, x2, x3, x4= harmony['x1'], harmony['x2'], harmony['x3'], harmony['x4']


    tomax, sigmamax, deltamax, p, l, ee, g , ng= [13600, 30000, 0.25, 6000, 14, 30e6, 12e6, 7]
    dx = (4 * p * l ** 3) / (ee * x3 ** 3 * x4)
    sx = (6 * p * l) / (x4 * x3 ** 2)
    pc = (4.013 * ee * ((x3 ** 2 * x4 ** 6) / 36) ** 0.5) / (l ** 2) * (1 - x3 / (2 * l) * (ee / (4 * g)) ** 0.5)
    m = p * (l + x2 / 2)
    r = (x2 ** 2 / 4 + ((x1 + x3) / 2) ** 2) ** 0.5
    j = 2 * (x1 * x2 * 2 ** 0.5 * ((x2 ** 2) / 12 + ((x1 + x3) / 2) ** 2))
    t1 = p / (x1 * x2 * 2 ** 0.5)
    t2 = m * r / j
    tox = (t1 ** 2 + t2 ** 2 + 2 * x2 * t1 * t2 / (2 * r)) ** 0.5

    constraints = [
        tox - tomax,
        sx - sigmamax,
        x1 - x4,
        0.10471 * x1 ** 2 + 0.04811 * x3 * x4 * (14 + x2) - 5,
        0.125 - x1,
        dx - deltamax,
        p - pc
    ]


    penalty = 0
    for i in constraints[:ng]:
        penalty += max(0, i)

    the_fitness = 1.10471 * x1 ** 2 * x2 + 0.04811 * x3 * x4 * (14 + x2)

    return the_fitness, penalty

optimizer = Minimization(design_space, obj_func)
optimizer.optimize(hmcr=0.9, par=0.2, memory_size=10, max_iter=100, log=True)
