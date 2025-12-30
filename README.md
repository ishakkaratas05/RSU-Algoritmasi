Giriş: Kullanıcı bir Seed değeri sağlar.

İç Durum Güncelleme: Sayı çift ise x/2 ^ K, tek ise (3x+1) % M işlemi yapılır.

Difüzyon (Yayılma): 64-bitlik sayı 3 birim sağa döndürülerek bitlerin yerleri değiştirilir.

Konfüzyon (Karıştırma): Sayının son 4 biti (nibble), S-Box tablosu kullanılarak doğrusal olmayan bir şekilde değiştirilir.

Dengeleme: Ardışık iki bit alınır (Von Neumann). Farklı iseler (01 veya 10) çıktı üretilir, aynı iseler bu adım tekrarlanır.

Çıkış: İstatistiksel olarak mükemmel dengeli bir anahtar akışı elde edilir.
