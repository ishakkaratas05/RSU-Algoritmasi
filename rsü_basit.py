def generate_secure_key(seed, length=64):
    x = seed
    k = 0x5555555555555555
    m = (2**64) - 59
    key = []

    for _ in range(length):
        if x % 2 == 0:
            x = (x // 2) ^ k
        else:
            x = (3 * x + 1) % m
        
        # 64-bit Bitwise Rotation (Karıştırma katmanı)
        x = ((x & 0xFFFFFFFFFFFFFFFF) >> 3) | ((x << 61) & 0xFFFFFFFFFFFFFFFF)
        
        # Çıktı olarak son biti al
        key.append(str(x % 2))
    
    return "".join(key)

# Test
tohum = 987654321
anahtar = generate_secure_key(tohum, 32)
print(f"Seed: {tohum}")
print(f"Üretilen 32-bit Anahtar: {anahtar}")