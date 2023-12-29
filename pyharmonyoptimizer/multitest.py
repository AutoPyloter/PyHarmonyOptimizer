from datetime import datetime
from collections import defaultdict

class Cari:
    def __init__(self, adi, bakiye=0):
        self.adi = adi
        self.bakiye = bakiye

    def para_ekle(self, miktar, odeme_sekli):
        self.bakiye += miktar
        print(f"{miktar} TL {self.adi} cari hesabına {odeme_sekli} yoluyla eklendi. Yeni bakiye: {self.bakiye} TL")

    def durum_goster(self):
        return f"Cari Adı: {self.adi}, Bakiye: {self.bakiye} TL"

class Harcama:
    harcama_listesi = []
    cari_hesaplar = {}

    def __init__(self, santiye, aciklama, tarih, belge_turu, yapan_kisi, firma, miktar, cari):
        self.santiye = santiye
        self.aciklama = aciklama
        self.tarih = datetime.strptime(tarih, '%Y-%m-%d')
        self.belge_turu = belge_turu
        self.yapan_kisi = yapan_kisi
        self.firma = firma
        self.miktar = miktar
        self.cari = cari
        if cari not in Harcama.cari_hesaplar:
            Harcama.cari_hesaplar[cari] = Cari(cari)
        Harcama.cari_hesaplar[cari].para_ekle(-miktar, "Harcama")
        Harcama.harcama_listesi.append(self)

    def __str__(self):
        return f"{self.santiye} - {self.aciklama} - {self.tarih.strftime('%Y-%m-%d')} - {self.miktar} TL"

    @classmethod
    def harcama_sil(cls, harcama):
        cls.harcama_listesi.remove(harcama)
        cls.cari_hesaplar[harcama.cari].para_ekle(harcama.miktar, "Harcama İptali")

    @classmethod
    def harcama_guncelle(cls, harcama, yeni_bilgiler):
        eski_miktar = harcama.miktar
        harcama.santiye = yeni_bilgiler.get('santiye', harcama.santiye)
        harcama.aciklama = yeni_bilgiler.get('aciklama', harcama.aciklama)
        harcama.tarih = yeni_bilgiler.get('tarih', harcama.tarih)
        harcama.belge_turu = yeni_bilgiler.get('belge_turu', harcama.belge_turu)
        harcama.yapan_kisi = yeni_bilgiler.get('yapan_kisi', harcama.yapan_kisi)
        harcama.firma = yeni_bilgiler.get('firma', harcama.firma)
        harcama.miktar = yeni_bilgiler.get('miktar', harcama.miktar)
        fark = harcama.miktar - eski_miktar
        cls.cari_hesaplar[harcama.cari].para_ekle(-fark, "Güncelleme")

    @classmethod
    def harcamalari_listele(cls):
        for harcama in cls.harcama_listesi:
            print(harcama)

    @classmethod
    def filtrele(cls, **kwargs):
        sonuclar = cls.harcama_listesi
        for key, value in kwargs.items():
            if key == "tarih":
                sonuclar = [h for h in sonuclar if value[0] <= h.tarih <= value[1]]
            elif key == "miktar":
                sonuclar = [h for h in sonuclar if value[0] <= h.miktar <= value[1]]
            elif key == "santiye":
                sonuclar = [h for h in sonuclar if h.santiye == value]
            elif key == "belge_turu":
                sonuclar = [h for h in sonuclar if h.belge_turu == value]
        return sonuclar

# Kullanım örneği
cari_A = Cari("Cari A", 10000)
cari_A.para_ekle(2000, "Elden")
print(cari_A.durum_goster())

harcama1 = Harcama("Santiye A", "Malzeme Alımı", "2023-12-01", "Fiş", "Ahmet", "Yıldız İnşaat", 1000, "Cari A")
harcama2 = Harcama("Santiye B", "Taşıma", "2023-12-02", "Makbuz", "Mehmet", "Güneş Nakliyat", 1500, "Cari A")

# Harcamaları listeleme
Harcama.harcamalari_listele()

# Harcama Güncelleme
Harcama.harcama_guncelle(harcama1, {"miktar": 1200})
print(Harcama.cari_hesaplar["Cari A"].durum_goster())

# Harcama Silme
Harcama.harcama_sil(harcama2)
print(Harcama.cari_hesaplar["Cari A"].durum_goster())

# Tarihe göre filtreleme
for harcama in Harcama.filtrele(tarih=(datetime(2023, 12, 1), datetime(2023, 12, 31))):
    print(harcama)
