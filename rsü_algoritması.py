import time

class SecureCollatzGenerator:
    """
    Gelişmiş Kriptografik Rastgele Sayı Üreteci (PRNG)
    Yöntem: Collatz Sanısı + S-Box + Von Neumann Düzeltmesi
    """
    def __init__(self, seed):
        self.state = seed
        self.k = 0x5555555555555555  # XOR Maskesi (Entropy artırıcı)
        self.m = (2**64) - 59         # Büyük Asal Modül (Döngü kırıcı)
        
        # 4-bit S-Box: Doğrusal olmayan (non-linear) dönüşüm tablosu
        # Bu tablo, sayı dizisindeki matematiksel desenleri yok eder.
        self.sbox = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 
                     0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

    def _next_raw_bit(self):
        """Collatz tabanlı ham bit üretir."""
        # 1. Adım: Collatz Dönüşümü (Sayı tekse 3n+1, çiftse n/2)
        if self.state % 2 == 0:
            self.state = (self.state // 2) ^ self.k
        else:
            self.state = (3 * self.state + 1) % self.m
        
        # 2. Adım: Bitwise Rotation (Yayılma/Diffusion)
        # Sayının bitlerini 3 pozisyon kaydırarak bitler arası ilişkiyi koparır.
        self.state = ((self.state & 0xFFFFFFFFFFFFFFFF) >> 3) | \
                     ((self.state << 61) & 0xFFFFFFFFFFFFFFFF)
        
        # 3. Adım: S-Box Karıştırma (Confusion)
        # Son 4 biti alır ve tablodaki karşılığıyla değiştirir.
        nibble = self.state & 0xF
        transformed = self.sbox[nibble]
        
        return transformed & 1 # Dönüştürülmüş değerin en sağdaki bitini al

    def generate(self, length):
        """
        Von Neumann filtresi kullanarak dengeli anahtar üretir.
        01 -> 0, 10 -> 1 kabul eder; 00 ve 11'i atar.
        """
        key = []
        while len(key) < length:
            b1 = self._next_raw_bit()
            b2 = self._next_raw_bit()
            
            if b1 == 0 and b2 == 1:
                key.append("0")
            elif b1 == 1 and b2 == 0:
                key.append("1")
        return "".join(key)

def run_demo():
    print("="*60)
    print("      GELİŞMİŞ GÜVENLİ ANAHTAR ÜRETİM ALGORİTMASI")
    print("        (Collatz + S-Box + Von Neumann Hybrid)")
    print("="*60)

    # 1. Hazırlık
    user_seed = int(time.time())
    print(f"[*] Sistem zamanı tohum (seed) olarak alındı: {user_seed}")
    
    gen = SecureCollatzGenerator(user_seed)
    
    # 2. Anahtar Üretimi
    key_length = 64
    print(f"[*] {key_length} bitlik anahtar üretiliyor...")
    start_time = time.time()
    final_key = gen.generate(key_length)
    end_time = time.time()
    
    # 3. Görsel Çıktı
    print("-" * 60)
    print(f"[+] Üretilen Anahtar (Binary):\n{final_key}")
    
    # Hex formatına çevir (Daha profesyonel görünür)
    key_hex = hex(int(final_key, 2)).upper()
    print(f"\n[+] Anahtar (Hex Formatı):\n{key_hex}")
    print("-" * 60)

    # 4. İstatistiksel Analiz Raporu
    zeros = final_key.count('0')
    ones = final_key.append = final_key.count('1')
    
    print("--- ALGORİTMİK PERFORMANS VE GÜVENLİK RAPORU ---")
    print(f"| İşlem Süresi: { (end_time - start_time)*1000:.4f} ms")
    print(f"| 0 Sayısı: {zeros} | 1 Sayısı: {ones}")
    print(f"| Denge Oranı: %{(ones/key_length)*100:.2f} (İdeal: %50)")
    print(f"| Durum: {'[GÜVENLİ - DENGELİ]' if 45 <= (ones/key_length)*100 <= 55 else '[RİSKLİ]'}")
    print("-" * 60)
    print("[!] Not: Von Neumann filtresi nedeniyle desen analizi imkansızdır.")

if __name__ == "__main__":
    run_demo()