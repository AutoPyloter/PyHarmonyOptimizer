from PyHarmonyOptimizer import *


design_space = {
    'x1': Continuous(0.1,2),
    'x2': Continuous(0.1,10),
    'x3': Continuous(0.1,10),
    'x4': Continuous(0.1,2)
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


for hmcr in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    for par in [0, 0.1,0.2,0.3,0.4,0.5]:
        the_best_one = ""
        the_best_fit = float('inf')
        dosya_adi = f'sonuclar{int(hmcr*10)}{int(par*10)}.txt'
        en_iyi_dosya_adi = f'en_iyi_sonuc{int(hmcr*10)}{int(par*10)}.txt'

        with open(dosya_adi, 'w') as dosya:
            for i in range(100):
                optimizer = Minimization(design_space, obj_func)
                text = optimizer.optimize(hmcr=hmcr, par=par, memory_size=20, max_iter=5000, log=True)
                dosya.write(f"Run {i+1}:\n{text[0]} {text[1]}\n")

                if the_best_fit is None or text[1] < the_best_fit:
                    the_best_fit = text[1]
                    the_best_one = text[0]

        # Tüm iterasyonlar tamamlandıktan sonra en iyi sonucu ve fitness değerini kaydet
        with open(en_iyi_dosya_adi, 'w') as en_iyi_dosya:
            en_iyi_dosya.write(f"En iyi sonuç: {the_best_one}\nEn iyi fitness: {the_best_fit}\n")

        print(f"hmcr={hmcr}, par={par}: En iyi sonuç: {the_best_one}, En iyi fitness: {the_best_fit}")
