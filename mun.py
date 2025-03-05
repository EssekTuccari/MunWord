import os
import time
import base64
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Terminali temizleme fonksiyonu
def temizle():
    os.system("clear" if os.name == "posix" else "cls")

# Rastgele AES anahtarı oluşturma fonksiyonu
def rastgele_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Şifreleme fonksiyonu (AES-256)
def sifrele(metin, key):
    key = key.encode("utf-8")[:32].ljust(32, b'\0')  # Anahtar 32 bayt olmalı
    cipher = AES.new(key, AES.MODE_CBC)
    sifreli_veri = cipher.encrypt(pad(metin.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + sifreli_veri).decode()

# Şifre çözme fonksiyonu
def coz(sifreli_metin, key):
    try:
        key = key.encode("utf-8")[:32].ljust(32, b'\0')
        sifreli_veri = base64.b64decode(sifreli_metin)
        iv, veri = sifreli_veri[:16], sifreli_veri[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(veri), AES.block_size).decode()
    except:
        return "Hatalı anahtar veya şifreli metin!"

# Animasyon efekti
def animasyon(mesaj):
    print(" ")
    for _ in range(3):
        print(f"\r{mesaj}.  ", end="", flush=True)
        time.sleep(0.05)
        print(f"\r{mesaj}.. ", end="", flush=True)
        time.sleep(0.05)
        print(f"\r{mesaj}...", end="", flush=True)
        time.sleep(0.05)
    print("\r" + " " * len(mesaj) + "\r", end="")

# Ana menü
def menu():
    while True:
        temizle()
        print("\033[34m" + "MUNWORD".center(50) + "\033[0m")  # Mavi renk
        print("\n[1] Şifrele")
        print("[2] Şifreyi Çöz")
        print("[3] Key Al")
        print("[0] Çıkış\n")

        secim = input("Seçiminiz: ")

        if secim == "1":
            temizle()
            metin = input("Şifrelemek istediğiniz metni giriniz: ")
            key = input("Key giriniz: ")
            animasyon("Şifreleniyor")
            sifreli_metin = sifrele(metin, key)
            print("\nŞifrelenmiş Metin:", sifreli_metin)
        
        elif secim == "2":
            temizle()
            sifreli_metin = input("Çözmek istediğiniz şifreli metni giriniz: ")
            key = input("Key giriniz: ")
            animasyon("Şifre çözülüyor")
            cozulmus_metin = coz(sifreli_metin, key)
            print("\nÇözülen Metin:", cozulmus_metin)
        
        elif secim == "3":
            temizle()
            animasyon("Key oluşturuluyor")
            print("\nRastgele Key:", rastgele_key())

        elif secim == "0":
            temizle()
            print("Çıkış yapılıyor...")
            time.sleep(1)
            break
        
        else:
            print("\nGeçersiz seçim!")

        input("\nMenüye dönmek için ENTER'a basın...")

# Programı çalıştır
if __name__ == "__main__":
    menu()
