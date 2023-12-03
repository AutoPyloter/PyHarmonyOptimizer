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
from pyharmony import Continuous, Discrete, Categorical, Constant, Minimization
import math

def calculate_volume(D, H):
    radius = D / 2
    return math.pi * math.pow(radius, 2) * H

def calculate_cost(harmony):
    H, Top, SideThickness, Diameter, BaseThickness = harmony['H'], harmony['Top'], harmony['SideThickness'], harmony['Diameter'], harmony['BaseThickness']
    metal_cost_per_cm3 = 3  # dolar
    volume = calculate_volume(Diameter, H)
    
    # İlk olarak tabanın hacmini hesapla
    total_metal_volume = math.pi * math.pow(Diameter / 2, 2) * BaseThickness / 10

    # Yan yüzey kalınlığını kontrol et
    if Top == "açık":
        SideThickness *= 2
    else:
        # Üst kapalıysa, üst dairenin hacmini de ekle
        total_metal_volume += math.pi * math.pow(Diameter / 2, 2) * BaseThickness / 10

    # Yan yüzeyin hacmini ekle
    total_metal_volume += math.pi * Diameter * H * SideThickness / 10

    # Maliyeti hesapla
    cost = total_metal_volume * metal_cost_per_cm3

    # Eğer hacim 250 cm³'ten azsa 100 dolar ekle
    if volume < 250:
        cost += 100

    return cost

# Tasarım Değişkenleri
design = {
    'H': Discrete([10, 12, 13, 17]),  #cm
    'Top': Categorical(["açık", "kapalı"]),
    'SideThickness': Continuous(2, 3),  # mm
    'Diameter': Discrete([3, 4, 5, 6]),  # cm
    'BaseThickness': Constant(2)  # Taban ve üst kalınlığı, mm
}

# Optimizasyon
optimizer = Minimization(design, calculate_cost)
best_solution = optimizer.optimize(HMCR=0.8, PAR=0.3, memory_size=100, max_iter=1000)
print("En iyi çözüm:", best_solution)

