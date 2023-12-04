# PyHarmonyOptimizer

PyHarmonyOptimizer, Python'da yazılmış esnek ve kullanımı kolay bir Harmony Search optimizasyon modülüdür. Bu modül, çeşitli türlerdeki optimizasyon problemlerini çözmek için tasarlanmıştır ve özellikle minimizasyon problemleri üzerine odaklanır.

### Google Colaboratory üzerinden açmak için:
https://colab.research.google.com/github/AutoPyloter/PyHarmonyOptimizer/blob/main/PyHarmony.ipynb

## Harmony Arama Algoritması Nedir?

Harmony Search (HS), müzikal süreçlerden esinlenerek geliştirilmiş bir metaheuristik optimizasyon algoritmasıdır. Bu algoritma, bir müzisyen grubunun en uyumlu melodiyi aramasına benzer şekilde çalışır. HS, çözüm adaylarını "harmoniler" olarak değerlendirir ve bu harmoniler üzerinde iteratif bir şekilde iyileştirmeler yaparak optimal veya yakın-optimal çözümlere ulaşmaya çalışır.

## PyHarmonyOptimizer'ın Özellikleri

PyHarmonyOptimizer, aşağıdaki özelliklere sahiptir:

- **Çeşitli Değişken Türleri**: Modül, kategorik, sürekli ve kesikli değişkenlerin tanımlanmasına olanak tanır. Bu sayede farklı türdeki optimizasyon problemleri üzerinde çalışabilir.
- **Esneklik**: Kullanıcılar, kendi amaç fonksiyonlarını tanımlayabilir ve algoritmanın bu fonksiyonları optimize etmesini sağlayabilir.
- **Minimizasyon Yeteneği**: Bu modül, özellikle minimizasyon problemlerini çözmek için tasarlanmıştır.
- **HMCR ve PAR Parametreleri**: Harmony Memory Considering Rate (HMCR) ve Pitch Adjustment Rate (PAR) parametreleri sayesinde, algoritmanın arama davranışı üzerinde detaylı kontrol sağlanır.

## Kullanımı ve Örnek senaryo

PyHarmonyOptimizer'ı kullanmak için öncelikle bir amaç fonksiyonu tanımlayın ve ardından bu fonksiyonu optimizasyon sınıfına ileterek optimizasyon işlemini başlatın. İşte basit bir kullanım örneği:

**Silindirik Kutu Üretimi için Optimal Tasarım Seçimi: Bir Fabrika Senaryosu**

Bir fabrikada, çeşitli amaçlar için kullanılacak yeni bir silindirik kutu imal edilecektir. Bu kutunun üretim maliyetini minimize etmek ve aynı zamanda belirli gereksinimleri karşılamak üzere, çeşitli tasarım parametreleri üzerinde karar verilmesi gerekmektedir.

Silindirik kutunun bazı temel özellikleri şunlardır:

- **Yükseklik**: Kutunun yüksekliği, belirli standart ölçüler arasında değişebilir. Bu ölçüler 10, 12, 13 ve 17 cm olarak belirlenmiştir.
- **Üst Kapak**: Kutunun üst kısmı, "açık" veya "kapalı" olabilir. Bu seçim, kutunun kullanım amacına ve istenen özelliklere bağlı olarak değişkenlik gösterir.
- **Yan Yüzey Kalınlığı**: Kutunun yan yüzeylerinin kalınlığı 2 mm ile 3 mm arasında değişebilir. Ancak, üstü açık olan kutular için bu kalınlık iki katına çıkarılarak 4 mm ile 6 mm arasında olacaktır. Bu, açık kutuların daha fazla dayanıklılığa ihtiyaç duyması sebebiyledir.
- **Çap**: Kutunun çapı, 3, 4, 5 ve 6 cm arasında değişebilir. Bu ölçü, kutunun genel boyutunu ve kapasitesini etkileyecektir.
- **Taban ve Üst Kalınlıkları**: Bu iki kısım sabit bir kalınlığa sahip olup, her ikisi de 2 mm kalınlığında tasarlanmıştır.

Kutunun maliyetini etkileyen temel faktör, kullanılan metalin maliyetidir. Metalin birim fiyatı cm³ başına 3 dolar olarak belirlenmiştir. Ancak, kutunun su alma hacmi 250 cm³'ün altına düştüğünde, kutunun maliyeti 100 dolar artar. Bu, daha küçük hacimli kutuların üretim sürecinde daha fazla işçilik ve dikkat gerektirmesi nedeniyledir.

Fabrika yönetimi, bu parametreler arasındaki en uygun kombinasyonu belirleyerek, maliyeti en aza indirmeyi ve aynı zamanda ürün kalitesini korumayı amaçlamaktadır. Bu amaçla, Harmony Search algoritması kullanılarak, en düşük maliyetli tasarım seçeneği belirlenecektir.

---

Bu senaryo, fabrikanın karşılaştığı optimizasyon problemine ve bu problemin çözümüne ilişkin bir kontekst sağlar.

**Bu senaryonun çözümünde modülün kullanımı**

```python
from PyHarmonyOptimizer import *
import math

class Cylinder:
    def __init__(self, diameter, height, side_thickness, base_thickness, is_top_open):
        self.diameter = diameter
        self.height = height
        self.side_thickness = side_thickness
        self.base_thickness = base_thickness
        self.is_top_open = is_top_open

    def volume(self):
        radius = self.diameter / 2
        return math.pi * radius ** 2 * self.height

    def metal_volume(self):
        radius = self.diameter / 2
        base_volume = math.pi * radius ** 2 * self.base_thickness / 10

        if self.is_top_open:
            self.side_thickness *= 2
        else:
            base_volume += math.pi * radius ** 2 * self.base_thickness / 10

        side_volume = math.pi * self.diameter * self.height * self.side_thickness / 10
        return base_volume + side_volume

class CostCalculator:
    METAL_COST_PER_CM3 = 3  # dolar

    def calculate_cost(self, cylinder):
        volume = cylinder.volume()
        metal_volume = cylinder.metal_volume()
        cost = metal_volume * self.METAL_COST_PER_CM3

        if volume < 250:
            cost += 100

        return cost

def create_cylinder_design():
    return {
        'H': Discrete([10,12,13,17]),  # cm
        'Top': Categorical(["açık","kapalı"]),
        'SideThickness': Continuous(2,3),  # mm
        'Diameter': Discrete([3,4,5,6]),  # cm
        'BaseThickness': Constant(2)  # Taban ve üst kalınlığı, mm
    }

def optimize_design():
    design = create_cylinder_design()
    cost_calculator = CostCalculator()

    def objective_function(harmony):
        is_top_open = harmony['Top'] == "açık"
        cylinder = Cylinder(harmony['Diameter'], harmony['H'], harmony['SideThickness'], harmony['BaseThickness'], is_top_open)
        return cost_calculator.calculate_cost(cylinder)

    optimizer = Minimization(design, objective_function)
    best_solution = optimizer.optimize(max_iter=1000)
    return best_solution
try:
    best_solution = optimize_design()
    print("En iyi çözüm:", best_solution)
except Exception as e:
    print(e)
```
---

# LICENSE

MIT License

Copyright (c) 2023 Abdulkadir Özcan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
