from concurrent.futures import ThreadPoolExecutor
import numpy as np
import time

def find_min_in_sublist(sublist):
    """ Alt listedeki minimum değeri döndürür. """
    return min(sublist)

def parallel_min_finder(full_list, num_threads):
    """ Paralel olarak bir listeden en küçük değeri bulur. """
    sublist_length = len(full_list) // num_threads
    futures = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Listenin parçalarını oluştur ve her bir parça için işlem başlat
        for i in range(0, len(full_list), sublist_length):
            sublist = full_list[i:i + sublist_length]
            futures.append(executor.submit(find_min_in_sublist, sublist))

        # Her parçanın minimumunu topla ve genel minimumu bul
        min_values = [future.result() for future in futures]
        return min(min_values)

# Örnek kullanım
if __name__ == "__main__":
    start=time.time()
    sample_list = np.random.randint(0, 100000, 1000000000)  # Büyük bir rastgele liste oluştur
    num_threads = 1  # İş parçacığı sayısı
    minimum_value = parallel_min_finder(sample_list, num_threads)
    print("Listedeki minimum değer:", minimum_value)
    finish=time.time()
    print(finish-start)
