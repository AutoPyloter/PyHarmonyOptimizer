# PyHarmonyOptimizer

PyHarmonyOptimizer, Python’da yazılmış esnek ve kullanımı kolay bir Harmony Search optimizasyon modülüdür. Bu modül, çeşitli türlerdeki optimizasyon problemlerini çözmek için tasarlanmıştır ve hem minimizasyon hem de maksimizasyon problemleri üzerine odaklanır. Genişletilmiş özellikler ve gelişmiş algoritmalar içerir, bu sayede çeşitli alanlardaki optimizasyon ihtiyaçlarınıza uyum sağlar.

### Google Colaboratory üzerinden açmak için:
https://colab.research.google.com/github/AutoPyloter/PyHarmonyOptimizer/blob/main/PyHarmony.ipynb

## Harmony Arama Algoritması Nedir?

Harmony Search (HS), müzikal süreçlerden esinlenerek geliştirilmiş bir metaheuristik optimizasyon algoritmasıdır. Bu algoritma, bir müzisyen grubunun en uyumlu melodiyi aramasına benzer şekilde çalışır. HS, çözüm adaylarını "harmoniler" olarak değerlendirir ve bu harmoniler üzerinde iteratif bir şekilde iyileştirmeler yaparak optimal veya yakın-optimal çözümlere ulaşmaya çalışır.

## PyHarmonyOptimizer'ın Özellikleri

PyHarmonyOptimizer, aşağıdaki özelliklere sahiptir:

- **Çeşitli Değişken Türleri:** Modül, kategorik, sürekli ve kesikli değişkenlerin tanımlanmasına olanak tanır. Farklı türdeki optimizasyon problemleri üzerinde çalışabilme esnekliği sağlar.
  
- **Esneklik:** Kullanıcılar, kendi amaç fonksiyonlarını tanımlayabilir ve algoritmanın bu fonksiyonları optimize etmesini sağlayabilir.
  
- **Geniş Optimizasyon Yetenekleri:** Bu modül, hem minimizasyon hem de maksimizasyon problemlerini çözmek üzere genişletilmiş yeteneklere sahiptir.
  
- **HMCR ve PAR Parametreleri:** Harmony Memory Considering Rate (HMCR) ve Pitch Adjustment Rate (PAR) parametreleri sayesinde, algoritmanın arama davranışı üzerinde detaylı kontrol sağlanır.
  
- **Gelişmiş Hata Yönetimi:** Kullanıcı girdilerindeki hatalara karşı sağlam uyarı ve hata mesajları ile kullanım kolaylığı artırılmıştır.

## Kullanımı ve Örnek senaryo

PyHarmonyOptimizer'ı kullanmak için öncelikle bir amaç fonksiyonu tanımlayın ve ardından bu fonksiyonu optimizasyon sınıfına ileterek optimizasyon işlemini başlatın. İşte basit bir kullanım örneği:

# Kaynaklı Kiriş Tasarım Problemi

## Problem Tanımı

Kaynaklı kiriş tasarım problemi, yapı mühendisliğinde yaygın olarak kullanılan ve optimizasyon algoritmalarını test etmek için sıklıkla tercih edilen bir benchmark problemdir. Bu problem, bir kirişin belirli kısıtlar altında en uygun boyutlarını bulmayı amaçlar, ağırlığını minimize ederken mukavemet, yer değiştirme ve geometrik kısıtlamaları karşılamak.

## Amaç

Harmony Search algoritması kullanılarak tasarım uzayını gezerek en iyi kiriş boyutlarını bulmayı hedefler.

## Nasıl Kullanılır

Python kodu, [PyHarmonyOptimizer](https://github.com/qm2021/PyHarmonyOptimizer) kütüphanesini kullanır. Projenin temel sınıfı olan `WeldedBeamDesign`, kaynaklı kirişin boyutlarını ve optimizasyon parametrelerini içerir. 

Örnek bir tasarımın fitness değerini öğrenmek için:

```python
from PyHarmonyOptimizer import *


class WeldedBeamDesign:
    YOUNGS_MODULUS = 30e6
    SHEAR_MODULUS = 12e6
    MAX_ITERATIONS = 2000
    MEMORY_SIZE = 20
    PAR_PARAMETER = 0.1
    HMCR_PARAMETER = 0.8
    LOAD = 6000
    BEAM_LENGTH = 14
    MAX_SHEAR_STRESS = 13600
    MAX_NORMAL_STRESS = 30000
    MAX_DISPLACEMENT = 0.25
    NUMBER_OF_CONSTRAINTS = 7
    RUN=30
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

    def fitness(self):
        penalty = self.compute_penalty()
        the_fitness = 1.10471 * self.beam_width ** 2 * self.beam_height + 0.04811 * self.beam_thickness * self. \
            weld_width * (14 + self.beam_height)
        the_reference = penalty + 10 if penalty > 0 else the_fitness
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
        return optimizer.optimize(max_iter=WeldedBeamDesign.MAX_ITERATIONS,
                                  memory_size=WeldedBeamDesign.MEMORY_SIZE,
                                  par=WeldedBeamDesign.PAR_PARAMETER,
                                  hmcr=WeldedBeamDesign.HMCR_PARAMETER,
                                  log=False)

    @staticmethod
    def print_solution(solution, file=None):
        harmony, fitness = solution
        output = f"Details of the best solution:\n"
        output += '\n'.join([f"  {key}: {value}" for key, value in harmony.items()])
        output += f"\nFitness value: {fitness}\n\n"

        print(output)
        if file:
            with open(file, 'a') as f:
                f.write(output)
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
        get_fitness_for_specific_design(0.206741, 3.65285, 8.54856, 0.231265)
    except Exception as e:
        print(f"An error occurred: {e}")

```python

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
