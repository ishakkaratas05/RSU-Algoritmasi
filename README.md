# 🛡️ Secure Collatz-Hybrid PRNG (Sözde Rastgele Sayı Üreteci)

> **Proje Konusu:** Bilgi Sistemleri ve Güvenliği  
> **Geliştirici:** [Adın Soyadın]  
> **Temel Amaç:** Kriptografik prensiplere dayalı, istatistiksel olarak dengeli bir anahtar üretim algoritması tasarlamak.

---

## 📖 Proje Hakkında
Bu proje, bilgisayar bilimlerinin temel problemlerinden biri olan "Rastgelelik (Randomness)" üzerine odaklanmıştır. Deterministik bir makine olan bilgisayarda, gerçek rastgeleliğe en yakın sonucu elde etmek için **Kaos Teorisi** ve **Kriptografik Dönüşümler** birleştirilmiştir.

Temel matematiksel modelimiz şudur:
$$Key = G(seed)$$

Burada **G (Generator)** fonksiyonu, küçük bir tohum değerini (seed) alıp, onu tahmin edilemez ve güvenli bir bit dizisine (Key) dönüştürmektedir.

---

## 🧠 Algoritma Mimarisi ve Teknik Detaylar

Algoritmamız, çıktının tahmin edilebilirliğini (Predictability) sıfıra indirmek için **4 farklı katmandan** oluşan hibrit bir yapı kullanır.

### 1. Kaos Kaynağı: Collatz Sanısı (3n+1 Problemi)
Algoritmanın motor kısmıdır. Matematiksel olarak çözülememiş bir problem olan Collatz dizisi kullanılmıştır.
* Sayı çift ise: $n = n / 2$
* Sayı tek ise: $n = 3n + 1$
* **Amaç:** Sayının izleyeceği yörüngenin (trajectory) kaotik olmasını sağlamak ve doğrusal artışı engellemektir.

### 2. Karıştırma (Confusion) - S-Box (Substitution Box)
Matematiksel işlemler (toplama/çarpma) tersine çevrilebilir. Bunu engellemek için **doğrusal olmayan (non-linear)** bir katman eklenmiştir.
* 4-bitlik parçalar (Nibbles), önceden tanımlanmış karmaşık bir tablo (S-Box) ile değiştirilir.
* **Amaç:** Girdi ile çıktı arasındaki matematiksel ilişkiyi koparmaktır.

### 3. Yayılma (Diffusion) - Bitwise Rotation & XOR
Küçük bir değişikliğin tüm sonucu etkilemesi (Avalanche Effect) hedeflenmiştir.
* **XOR Maskeleme:** Sayı, `0x5555...` (010101...) maskesi ile XOR işlemine sokularak bitlerin tersyüz edilmesi sağlanır.
* **Rotation:** Bitler sola ve sağa kaydırılarak yer değiştirir.
* **Amaç:** Sayının sadece son basamaklarının değil, tamamının değişmesini sağlamaktır.

### 4. İstatistiksel Dengeleyici: Von Neumann Filtresi
Rastgele sayı üreteçlerinin en büyük sorunu olan "Bias" (yanlılık) problemini çözer. Ham veride `0` veya `1` gelme olasılığı eşit olmayabilir.
* Çıktıdan iki bit okunur (`b1`, `b2`).
* `01` gelirse -> Sonuç `0`
* `10` gelirse -> Sonuç `1`
* `00` veya `11` gelirse -> Veri atılır (Discard).
* **Amaç:** Çıktının %50 "0" ve %50 "1" olmasını matematiksel olarak garanti etmektir.

---

## 📝 Algoritma Sözde Kodu (Pseudocode)

```text
ALGORİTMA Secure_PRNG_Generator
GİRDİ: Seed (Tohum Değeri)
ÇIKTI: Binary Anahtar Dizisi

BAŞLAT
    State = Seed
    Key = Boş Dizi
    XOR_Mask = 0x5555...
    
    DÖNGÜ (Key Uzunluğu < Hedef Uzunluk) SÜRESİNCE:
        
        // --- 1. KAOS KATMANI (Collatz) ---
        EĞER (State % 2 == 0) İSE:
            State = (State / 2) XOR XOR_Mask
        DEĞİLSE:
            State = (3 * State + 1) MOD Büyük_Asal_Sayı
        
        // --- 2. YAYILMA KATMANI ---
        State = Bitwise_Rotate_Left(State) OR Bitwise_Rotate_Right(State)
        
        // --- 3. KARIŞTIRMA KATMANI (S-Box) ---
        Nibble = State AND 0xF
        Transformed_Bit = SBox_Tablosu[Nibble]
        
        // --- 4. FİLTRELEME KATMANI (Von Neumann) ---
        Bit_A = Bir_Sonraki_Bit_Üret()
        Bit_B = Bir_Sonraki_Bit_Üret()
        
        EĞER (Bit_A == 0 VE Bit_B == 1) İSE:
            Key'e "0" Ekle
        EĞER (Bit_A == 1 VE Bit_B == 0) İSE:
            Key'e "1" Ekle
        // (0-0 ve 1-1 durumlarında işlem yapılmaz, döngü devam eder)
        
    DÖNGÜ BİTİR
    
    DÖNDÜR Key
BİTİR
