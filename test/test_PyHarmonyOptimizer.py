import random
import types
from abc import ABC, abstractmethod

class Sampler(ABC):
    """
    Örnekleyici sınıflar için soyut bir temel sınıf.
    Her örnekleyicinin bir 'sample' metodu olmalıdır.
    """
    @abstractmethod
    def sample(self):
        """Rastgele bir değer üretir."""
        pass


class Continuous(Sampler):
    """
    Sürekli değerler için örnekleyici.
    Belirli bir aralıkta sürekli değerler üretir.
    """
    def __init__(self, *args):
        # Kullanıcının iki değerden fazla girmesini kontrol et
        if len(args) != 2:
            raise ValueError("Yalnızca iki değer girilmelidir: min_val ve max_val.")

        min_val, max_val = args

        # min_val ve max_val'ın uygun tipte olup olmadığını kontrol et
        if not isinstance(min_val, (float, int)):
            raise TypeError("min_val, bir sayı olmalıdır.")
        if not isinstance(max_val, (float, int)):
            raise TypeError("max_val, bir sayı olmalıdır.")

        # min_val ve max_val'ın mantıklı bir aralık oluşturup oluşturmadığını kontrol et
        if min_val >= max_val:
            raise ValueError("Minimum değer, maksimum değerden küçük olmalıdır.")

        self.min_val = min_val
        self.max_val = max_val

    def sample(self):
        """Aralıktaki rastgele bir sürekli değer üretir."""
        return random.uniform(self.min_val, self.max_val)

class Discrete(Sampler):
    """
    Ayrık değerler için örnekleyici.
    Verilen bir değerler listesinden rastgele seçim yapar.
    """
    def __init__(self, values):
        if not isinstance(values, list):
            raise TypeError("values, bir liste olmalıdır.")

        """
        Args:
            values (list): Örneklenmek üzere verilen değerler listesi.

        Raises:
            ValueError: Eğer değerler listesi boş ise.
        """
        if not values:
            raise ValueError("Değerler listesi boş olamaz.")
        self.values = values

    def sample(self):
        """Listeden rastgele bir ayrık değer seçer."""
        return random.choice(self.values)

class Constant(Sampler):
    def __init__(self, *args):
        # Kullanıcının yalnızca bir argüman girdiğinden emin ol
        if len(args) != 1:
            raise ValueError("Constant sınıfı yalnızca bir değer kabul eder.")

        self.value = args[0]

    def sample(self):
        """Sabit değeri döndürür."""
        return self.value

class Categorical(Sampler):
    """
    Kategorik değerler için örnekleyici.
    Verilen kategori listesinden rastgele bir kategori seçer.
    """
    def __init__(self, categories):
        """
        Args:
            categories (list): Kategorilerin listesi.

        Raises:
            ValueError: Eğer kategoriler listesi boş ise.
        """
        if not categories:
            raise ValueError("Kategoriler listesi boş olamaz.")
        self.categories = categories

    def sample(self):
        """Listeden rastgele bir kategori seçer."""
        return random.choice(self.categories)

class Optimization(ABC):
    """
    Optimizasyon algoritmaları için soyut temel sınıf.
    Türetilen her sınıf, optimize metodunu gerçekleştirmelidir.
    """
    def __init__(self, design, objective):
        """
        Optimizasyon sınıfının inşaatçısı.

        Args:
            design (dict): Tasarım değişkenlerini içeren sözlük.
            objective (callable): Amaç fonksiyonu.

        Raises:
            ValueError: Eğer tasarım sözlüğü boş ise veya amaç fonksiyonu çağrılabilir değilse.
        """
        if not isinstance(design, dict):
            raise TypeError("design bir sözlük (dict) olmalıdır.")
        if not design:
            raise ValueError("Tasarım sözlüğü boş olamaz.")
        if not callable(objective):
            raise ValueError("Amaç fonksiyonu çağrılabilir bir nesne olmalıdır.")
        if not isinstance(objective, types.FunctionType):
            raise TypeError("objective, bir fonksiyon olmalıdır.")
        for key, sampler in design.items():
            if not isinstance(sampler, Sampler):
                raise TypeError(f"{key} için örnekleyici bir Sampler türevi olmalıdır.")

        self.design = design
        self.objective = objective
        self.harmony_memory = []

    def initialize_harmony_memory(self, size):
        """
        Harmony memory'yi başlatır.

        Args:
            size (int): Harmony memory'nin boyutu.

        Raises:
            ValueError: Eğer boyut sıfırdan küçük veya eşitse.
        """
        if size <= 0:
            raise ValueError("Hafıza boyutu sıfırdan büyük olmalıdır.")
        for _ in range(size):
            harmony = {var: self.design[var].sample() for var in self.design}
            self.harmony_memory.append((harmony, self.objective(harmony)))

    def generate_new_harmony(self, HMCR, PAR):
        if not 0 <= HMCR <= 1:
            raise ValueError("HMCR değeri 0 ile 1 arasında olmalıdır.")
        if not 0 <= PAR <= 1:
            raise ValueError("PAR değeri 0 ile 1 arasında olmalıdır.")
        """
        Yeni bir harmony oluşturur.

        Args:
            HMCR (float): Harmony memory considering rate.
            PAR (float): Pitch adjusting rate.

        Returns:
            dict: Yeni oluşturulan harmony.
        """
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
    def optimize(self, HMCR, PAR, memory_size, max_iter,log):

        """Optimizasyon sürecini gerçekleştirir."""
        pass

class Minimization(Optimization):
    """
    Belirli bir hedef fonksiyonunu minimize etmeyi amaçlayan sınıf.
    """
    def optimize(self, HMCR=0.8, PAR=0.3, memory_size=10, max_iter=100,log=False):
        if not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("max_iter bir tam sayı olmalı ve 1'den küçük olamaz.")

        if not isinstance(memory_size, int) or memory_size < 2:
            raise ValueError("memory_size bir tam sayı olmalı ve 2'den küçük olamaz.")

        """
        Minimizasyon sürecini başlatır ve yürütür.

        Args:
            HMCR (float): Harmony memory considering rate.Varsayılan değer 0.8
            PAR (float): Pitch adjusting rate. 0.3
            memory_size (int, optional): Harmony memory'nin boyutu. Varsayılan değer 10.
            max_iter (int, optional): Maksimum iterasyon sayısı. Varsayılan değer 100.

        Returns:
            tuple: En iyi uyumu ve ilgili fitness değerini içeren tuple.
        """
        self.initialize_harmony_memory(memory_size)
        for index in range(max_iter):
            new_harmony = self.generate_new_harmony(HMCR, PAR)
            new_fitness = self.objective(new_harmony)
            worst_harmony = max(self.harmony_memory, key=lambda x: x[1])
            if worst_harmony[1] > new_fitness:
                self.harmony_memory.remove(worst_harmony)
                self.harmony_memory.append((new_harmony, new_fitness))
            if log==True:
                print("iterasyon:",index+1,min(self.harmony_memory, key=lambda x: x[1]))
        return min(self.harmony_memory, key=lambda x: x[1])

class Maximization(Optimization):
    """
    Belirli bir hedef fonksiyonunu maksimize etmeyi amaçlayan sınıf.
    """
    def optimize(self, HMCR=0.8, PAR=0.3, memory_size=10, max_iter=300,log=False):
        if not isinstance(max_iter, int) or max_iter < 1:
            raise ValueError("max_iter bir tam sayı olmalı ve 1'den küçük olamaz.")

        if not isinstance(memory_size, int) or memory_size < 2:
            raise ValueError("memory_size bir tam sayı olmalı ve 2'den küçük olamaz.")

        """
        Maksimizasyon sürecini başlatır ve yürütür.

        Args:
            HMCR (float): Harmony memory considering rate.
            PAR (float): Pitch adjusting rate.
            memory_size (int, optional): Harmony memory'nin boyutu. Varsayılan değer 10.
            max_iter (int, optional): Maksimum iterasyon sayısı. Varsayılan değer 100.

        Returns:
            tuple: En iyi uyumu ve ilgili fitness değerini içeren tuple.
        """
        self.initialize_harmony_memory(memory_size)
        for index in range(max_iter):
            new_harmony = self.generate_new_harmony(HMCR, PAR)
            new_fitness = self.objective(new_harmony)
            worst_harmony = min(self.harmony_memory, key=lambda x: x[1])
            if worst_harmony[1] < new_fitness:
                self.harmony_memory.remove(worst_harmony)
                self.harmony_memory.append((new_harmony, new_fitness))
            if log==True:
                print("iterasyon:",index+1,min(self.harmony_memory, key=lambda x: x[1]))
        return max(self.harmony_memory, key=lambda x: x[1])
