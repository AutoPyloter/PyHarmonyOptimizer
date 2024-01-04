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

optimizer = Minimization(design_space, obj_func)
optimizer.optimize(hmcr=0.8, par=0.3, memory_size=200, max_iter=5000, log=True)

