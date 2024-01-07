import os
import re

# Klasördeki tüm dosyaları listele
klasor = '.'  # Dosyaların bulunduğu klasörün yolu. Örneğin, '/path/to/your/folder'
dosya_listesi = os.listdir(klasor)

# Regex ile 'en_iyi_sonuc*.txt' formatındaki dosyaları bul
pattern = re.compile(r'en_iyi_sonuc\d+\.txt$')

# Bulunan dosyalardan fitness değerlerini oku ve yazdır
for dosya in dosya_listesi:
    if pattern.match(dosya):
        with open(os.path.join(klasor, dosya), 'r') as file:
            icerik = file.readlines()
            fitness_degeri = icerik[-1].strip()  # En son satırdaki fitness değerini al
            print(f"{dosya}: {fitness_degeri}")
