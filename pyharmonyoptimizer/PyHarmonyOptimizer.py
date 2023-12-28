import random
import types
from abc import ABC, abstractmethod


class Sampler(ABC):

    @abstractmethod
    def sample(self):
        pass


class Continuous(Sampler):


    def __init__(self, *args):

        if len(args) != 2:
            raise ValueError("Only two values should be provided: min_val and max_val.")

        min_val, max_val = args

        if not isinstance(min_val, (float, int)):
            raise TypeError("min_val must be a number.")
        if not isinstance(max_val, (float, int)):
            raise TypeError("max_val must be a number.")

        if min_val >= max_val:
            raise ValueError("The minimum value should be less than the maximum value.")

        self.min_val = min_val
        self.max_val = max_val

    def sample(self):

        return random.uniform(self.min_val, self.max_val)


class Discrete(Sampler):


    def __init__(self, values):

        if not isinstance(values, list):
            raise TypeError("Values must be a list.")

        if not values:
            raise ValueError("The list of values cannot be empty.")
        
        self.values = values

    def sample(self):

        return random.choice(self.values)


class Constant(Sampler):


    def __init__(self, *args):
        # Ensure that the user provided only one argument
        if len(args) != 1:
            raise ValueError("The Constant class only accepts one value.")

        self.value = args[0]

    def sample(self):

        return self.value


class Categorical(Sampler):


    def __init__(self, categories):

        if not categories:
            raise ValueError("The list of categories cannot be empty.")
        self.categories = categories

    def sample(self):

        return random.choice(self.categories)


class Optimization(ABC):

    def __init__(self, design, objective):

        if not isinstance(design, dict):
            raise TypeError("The design must be a dictionary.")
        
        if not design:
            raise ValueError("The design dictionary cannot be empty.")
        
        if not callable(objective):

            raise ValueError("The objective function must be a callable object.")
        if not isinstance(objective, types.FunctionType):
            raise TypeError("The objective must be a function.")
        
        for key, sampler in design.items():

            if not isinstance(sampler, Sampler):
                raise TypeError(f"For {key}, the sampler must be an instance of Sampler.")

        self.design = design
        self.objective = objective
        self.harmony_memory = []


    def initialize_harmony_memory(self, size):
        if size <= 0:
            raise ValueError("The memory size must be greater than zero.")
        
        for _ in range(size):
            harmony = {var: self.design[var].sample() for var in self.design}
            self.harmony_memory.append((harmony, self.objective(harmony)))


    def generate_new_harmony(self, hmcr, par):

        if not 0 <= hmcr <= 1:
            raise ValueError("The hmcr value must be between 0 and 1.")
        
        if not 0 <= par <= 1:
            raise ValueError("The PAR value must be between 0 and 1.")
        
        new_harmony = {}
        for var in self.design:

            if random.random() < hmcr:
                new_harmony[var] = random.choice([h[0][var] for h in self.harmony_memory])
            else:
                new_harmony[var] = self.design[var].sample()

            if random.random() < par:
                new_harmony[var] = self.design[var].sample()
        return new_harmony
    

    @abstractmethod
    def optimize(self, hmcr, par, memory_size, max_iter, log):
        pass


    def update_harmony_memory(self, new_harmony, new_fitness, optimize_func):

        comparison_harmony = optimize_func(self.harmony_memory, key=lambda x: x[1])

        if (optimize_func == max and comparison_harmony[1] > new_fitness) or \
           (optimize_func == min and comparison_harmony[1] < new_fitness):
            self.harmony_memory.remove(comparison_harmony)
            self.harmony_memory.append((new_harmony, new_fitness))

            
    def print_harmony_memory(self):
        print("Harmony Memory:")
        num = 1
        for harmony, fitness in self.harmony_memory:
            print(f"  Harmony {num}: {harmony}, Fitness: {fitness}")
            num += 1


class Minimization(Optimization):


    def optimize(self, hmcr=0.8, par=0.3, memory_size=20, max_iter=1000, log=False):

        if not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("The max_iter must be an integer and cannot be less than 1.")

        if not isinstance(memory_size, int) or memory_size < 2:
            raise ValueError("The memory_size must be an integer and cannot be less than 2.")

        self.initialize_harmony_memory(memory_size)
        for index in range(max_iter):
            new_harmony = self.generate_new_harmony(hmcr, par)
            new_fitness = self.objective(new_harmony)
            self.update_harmony_memory(new_harmony, new_fitness, max)

            if log:
                print("iteration:", index + 1, min(self.harmony_memory, key=lambda x: x[1]))

        return min(self.harmony_memory, key=lambda x: x[1])


class Maximization(Optimization):


    def optimize(self, hmcr=0.8, par=0.3, memory_size=20, max_iter=1000, log=False):

        if not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("The max_iter must be an integer and cannot be less than 1.")

        if not isinstance(memory_size, int) or memory_size < 2:
            raise ValueError("The memory_size must be an integer and cannot be less than 2.")
        
        self.initialize_harmony_memory(memory_size)

        for index in range(max_iter):
            new_harmony = self.generate_new_harmony(hmcr, par)
            new_fitness = self.objective(new_harmony)
            self.update_harmony_memory(new_harmony, new_fitness, min)

            if log:
                print("iteration:", index + 1, max(self.harmony_memory, key=lambda x: x[1]))

        return max(self.harmony_memory, key=lambda x: x[1])

if __name__ == "__main__":
    try:
        print("This module is written by Abdulkadir Özcan.")
    except Exception as e:
        print(f"An error occurred: {e}")
