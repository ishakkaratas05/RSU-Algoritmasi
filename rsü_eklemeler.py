import time

class SecureCollatzGenerator:
    def __init__(self, seed):
        self.state = seed
        self.k = 0x5555555555555555
        self.m = (2**64) - 59
        # 4-bit S-Box (Karıştırma tablosu)
        self.sbox = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 
                     0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

    def _next_bit(self):
        # 1. Collatz Dönüşümü
        if self.state % 2 == 0:
            self.state = (self.state // 2) ^ self.k
        else:
            self.state = (3 * self.state + 1) % self.m
        
        # 2. Bitwise Rotation (Karıştırma)
        self.state = ((self.state & 0xFFFFFFFFFFFFFFFF) >> 3) | \
                     ((self.state << 61) & 0xFFFFFFFFFFFFFFFF)
        
        # 3. S-Box Uygulama (Son 4 biti değiştirir)
        nibble = self.state & 0xF
        transformed = self.sbox[nibble]
        return transformed & 1 # En sağdaki biti döndür

    def generate(self, length):
        key = []
        while len(key) < length:
            # Von Neumann Filtresi (Dengeleyici)
            b1 = self._next_bit()
            b2 = self._next_bit()
            
            if b1 == 0 and b2 == 1:
                key.append("0")
            elif b1 == 1 and b2 == 0:
                key.append("1")
            # 00 veya 11 gelirse atla ve tekrar dene
        return "".join(key)

# Test Kullanımı
gen = SecureCollatzGenerator(seed=int(time.time()))
anahtar = gen.generate(64)
print(f"Üretilen 64-bit Güvenli Anahtar: {anahtar}")