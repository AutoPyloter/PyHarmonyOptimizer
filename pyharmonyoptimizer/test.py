sonuclar = []

with open('sonuclar92.txt', 'r') as file:
    for line in file:
        if 'Iteration 5000,' in line:
            sonuclar.append(line.strip())

for sonuc in sonuclar:
    print(sonuc)
