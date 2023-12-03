# PyHarmonyOptimizer

PyHarmonyOptimizer, Python'da yazılmış esnek ve kullanımı kolay bir Harmony Search optimizasyon modülüdür. Bu modül, çeşitli türlerdeki optimizasyon problemlerini çözmek için tasarlanmıştır ve özellikle minimizasyon problemleri üzerine odaklanır.

## Harmony Arama Algoritması Nedir?

Harmony Search (HS), müzikal süreçlerden esinlenerek geliştirilmiş bir metaheuristik optimizasyon algoritmasıdır. Bu algoritma, bir müzisyen grubunun en uyumlu melodiyi aramasına benzer şekilde çalışır. HS, çözüm adaylarını "harmoniler" olarak değerlendirir ve bu harmoniler üzerinde iteratif bir şekilde iyileştirmeler yaparak optimal veya yakın-optimal çözümlere ulaşmaya çalışır.

## PyHarmonyOptimizer'ın Özellikleri

PyHarmonyOptimizer, aşağıdaki özelliklere sahiptir:

- **Çeşitli Değişken Türleri**: Modül, kategorik, sürekli ve kesikli değişkenlerin tanımlanmasına olanak tanır. Bu sayede farklı türdeki optimizasyon problemleri üzerinde çalışabilir.
- **Esneklik**: Kullanıcılar, kendi amaç fonksiyonlarını tanımlayabilir ve algoritmanın bu fonksiyonları optimize etmesini sağlayabilir.
- **Minimizasyon Yeteneği**: Bu modül, özellikle minimizasyon problemlerini çözmek için tasarlanmıştır.
- **HMCR ve PAR Parametreleri**: Harmony Memory Considering Rate (HMCR) ve Pitch Adjustment Rate (PAR) parametreleri sayesinde, algoritmanın arama davranışı üzerinde detaylı kontrol sağlanır.

## Kullanımı

PyHarmonyOptimizer'ı kullanmak için öncelikle bir amaç fonksiyonu tanımlayın ve ardından bu fonksiyonu optimizasyon sınıfına ileterek optimizasyon işlemini başlatın. İşte basit bir kullanım örneği:

```python
from pyharmony import Continuous, Discrete, Categorical, Minimization

def objective_function(harmony):
    # Amaç fonksiyonunu tanımlayın
    ...

design = {
    'A': Discrete([0, 1, 3]),
    'B': Discrete([1, 1.5, 2, 2.5, 3, 3.5]),
    'C': Continuous(4, 5),
    'D': Categorical(["yukarı", "aşağı"])
}

optimizer = Minimization(design, objective_function)
best_solution = optimizer.optimize(HMCR=0.8, PAR=0.3, memory_size=10, max_iter=100)
