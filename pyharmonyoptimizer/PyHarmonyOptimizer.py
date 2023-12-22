import random
import types
from abc import ABC, abstractmethod


class Sampler(ABC):
    """
    An abstract base class representing the foundation for sampler classes.
    Every sampler derived from this class must implement the 'sample' method.
    """

    @abstractmethod
    def sample(self):
        """Generates a random value."""
        pass


class Continuous(Sampler):
    """
    A sampler designed for continuous values.
    It generates continuous values within a specified range.
    """

    def __init__(self, *args):
        # Check if the user provided more than two values
        if len(args) != 2:
            raise ValueError("Only two values should be provided: min_val and max_val.")

        min_val, max_val = args

        # Check if min_val and max_val are of the appropriate type
        if not isinstance(min_val, (float, int)):
            raise TypeError("min_val must be a number.")
        if not isinstance(max_val, (float, int)):
            raise TypeError("max_val must be a number.")

        # Check if min_val is less than max_val to create a sensible range
        if min_val >= max_val:
            raise ValueError("The minimum value should be less than the maximum value.")

        self.min_val = min_val
        self.max_val = max_val

    def sample(self):
        """Generates a random continuous value within the specified range."""
        return random.uniform(self.min_val, self.max_val)


class Discrete(Sampler):
    """
    A sampler designed for discrete values.
    It selects a random value from a given list of values.
    """

    def __init__(self, values):
        if not isinstance(values, list):
            raise TypeError("Values must be a list.")

        """
        Args:
            values (list): List of values to be sampled from.

        Raises:
            ValueError: If the list of values is empty.
        """
        if not values:
            raise ValueError("The list of values cannot be empty.")
        self.values = values

    def sample(self):
        """Selects a random discrete value from the provided list."""
        return random.choice(self.values)


class Constant(Sampler):
    def __init__(self, *args):
        # Ensure that the user provided only one argument
        if len(args) != 1:
            raise ValueError("The Constant class only accepts one value.")

        self.value = args[0]

    def sample(self):
        """Returns the constant value."""
        return self.value


class Categorical(Sampler):
    """
    A sampler designed for categorical values.
    It randomly selects a category from the given list of categories.
    """

    def __init__(self, categories):
        """
        Args:
            categories (list): List of categories.

        Raises:
            ValueError: If the list of categories is empty.
        """
        if not categories:
            raise ValueError("The list of categories cannot be empty.")
        self.categories = categories

    def sample(self):
        """Randomly selects a category from the provided list."""
        return random.choice(self.categories)


class Optimization(ABC):
    """
    An abstract base class for optimization algorithms.
    Every derived class must implement the 'optimize' method.
    """

    def __init__(self, design, objective):
        """
        The constructor for the Optimization class.

        Args:
            design (dict): A dictionary containing design variables.
            objective (callable): The objective function.

        Raises:
            ValueError: If the design dictionary is empty or the objective function is not callable.
        """
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
        """
        Initializes the harmony memory.

        Args:
            size (int): The size of the harmony memory.

        Raises:
            ValueError: If the size is less than or equal to zero.
        """
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
        """
        Generates a new harmony.

        Args:
            hmcr (float): Harmony Memory Considering Rate.
            par (float): Pitch Adjusting Rate.

        Returns:
            dict: The newly generated harmony.
        """
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
        """Performs the optimization process."""
        pass


class Minimization(Optimization):
    """
    A class designed to minimize a specific objective function.
    """
    def print_harmony_memory(self):
        """Harmony belleğindeki tüm tasarımları ve fitness değerlerini yazdırır."""
        print("Harmony Memory:")
        num=1
        for harmony, fitness in self.harmony_memory:
            print(f"  Harmony {num}: {harmony}, Fitness: {fitness}")
            num+=1
    def optimize(self, hmcr=0.8, par=0.3, memory_size=10, max_iter=100, log=False):
        if not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("The max_iter must be an integer and cannot be less than 1.")

        if not isinstance(memory_size, int) or memory_size < 2:
            raise ValueError("The memory_size must be an integer and cannot be less than 2.")

        """
        Initiates and executes the minimization process.

        Args:
            hmcr (float): Harmony Memory Considering Rate. Default value is 0.8.
            par (float): Pitch Adjusting Rate. Default value is 0.3.
            memory_size (int, optional): The size of the harmony memory. Default value is 10.
            max_iter (int, optional): The maximum number of iterations. Default value is 100.

        Returns:
            tuple: A tuple containing the best harmony and its corresponding fitness value.
        """
        self.initialize_harmony_memory(memory_size)
        for index in range(max_iter):
            new_harmony = self.generate_new_harmony(hmcr, par)
            new_fitness = self.objective(new_harmony)
            worst_harmony = max(self.harmony_memory, key=lambda x: x[1])
            if worst_harmony[1] > new_fitness:
                self.harmony_memory.remove(worst_harmony)
                self.harmony_memory.append((new_harmony, new_fitness))
            if log:
                print("iteration:", index + 1, min(self.harmony_memory, key=lambda x: x[1]))
        return min(self.harmony_memory, key=lambda x: x[1])


class Maximization(Optimization):
    """
    A class designed to maximize a specific objective function.
    """
    def print_harmony_memory(self):
        """Harmony belleğindeki tüm tasarımları ve fitness değerlerini yazdırır."""
        print("Harmony Memory:")
        num=1
        for harmony, fitness in self.harmony_memory:
            print(f"  Harmony{num}: {harmony}, Fitness: {fitness}")
    def optimize(self, hmcr=0.8, par=0.3, memory_size=10, max_iter=300, log=False):
        if not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("The max_iter must be an integer and cannot be less than 1.")

        if not isinstance(memory_size, int) or memory_size < 2:
            raise ValueError("The memory_size must be an integer and cannot be less than 2.")

        """
        Initiates and executes the maximization process.

        Args:
            hmcr (float): Harmony Memory Considering Rate.
            par (float): Pitch Adjusting Rate.
            memory_size (int, optional): The size of the harmony memory. Default value is 10.
            max_iter (int, optional): The maximum number of iterations. Default value is 100.

        Returns:
            tuple: A tuple containing the best harmony and its corresponding fitness value.
        """
        self.initialize_harmony_memory(memory_size)
        for index in range(max_iter):
            new_harmony = self.generate_new_harmony(hmcr, par)
            new_fitness = self.objective(new_harmony)
            worst_harmony = min(self.harmony_memory, key=lambda x: x[1])
            if worst_harmony[1] < new_fitness:
                self.harmony_memory.remove(worst_harmony)
                self.harmony_memory.append((new_harmony, new_fitness))
            if log:
                print("iteration:", index + 1, min(self.harmony_memory, key=lambda x: x[1]))
        return max(self.harmony_memory, key=lambda x: x[1])




if __name__ == "__main__":
    try:
        print("This module is written by Abdulkadir Özcan.")
    except Exception as e:
        print(f"An error occurred: {e}")

