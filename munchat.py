import os
import time
import base64
import random
import string
import firebase_admin
from firebase_admin import credentials, db
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Firebase bağlantısı
FIREBASE_URL = "https://senin-projen.firebaseio.com/"  # Firebase URL'nizi buraya girin
FIREBASE_KEY = "firebase-anahtar.json"  # Firebase hizmet hesabı JSON dosyanız

# Firebase kimlik doğrulama
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY)
    firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_URL})

# Terminal temizleme fonksiyonu
def temizle():
    os.system("clear" if os.name == "posix" else "cls")

# Rastgele AES anahtarı oluşturma fonksiyonu
def rastgele_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# Şifreleme fonksiyonu (AES-256)
def sifrele(metin, key):
    key = key.encode("utf-8")[:32].ljust(32, b'\0')
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

# Kullanıcıdan arkadaş kodu ve şifreleme key'i al
def esles():
    temizle()
    global arkadas_kodu, aes_key
    arkadas_kodu = input("Arkadaş kodunu giriniz: ").strip()
    aes_key = input("Gizli AES anahtarını giriniz: ").strip()

    ref = db.reference(f"chats/{arkadas_kodu}")
    if ref.get() is None:
        ref.set({"messages": []})  # Yeni sohbet başlat
    
    print(f"Eşleşme başarılı! Sohbet ID: {arkadas_kodu}")
    time.sleep(1)

# Mesaj gönderme
def mesaj_gonder():
    temizle()
    mesaj = input("Göndermek istediğiniz mesajı girin: ")
    
    if not mesaj.strip():
        return

    sifreli_mesaj = sifrele(mesaj, aes_key)
    ref = db.reference(f"chats/{arkadas_kodu}/messages")
    ref.push({"sender": "client", "message": sifreli_mesaj})
    print("Mesaj gönderildi!")

# Mesajları kontrol etme
def mesaj_kontrol():
    temizle()
    ref = db.reference(f"chats/{arkadas_kodu}/messages")
    mesajlar = ref.get()

    if mesajlar:
        print("Şifreli Mesajlar:")
        for mesaj_id, veri in mesajlar.items():
            sifreli_metin = veri["message"]
            cozulmus_metin = coz(sifreli_metin, aes_key)
            print(f"- {cozulmus_metin}")
    else:
        print("Henüz mesaj yok.")

    input("\nMenüye dönmek için ENTER'a basın...")

# Ana menü
def menu():
    esles()
    while True:
        temizle()
        print("\033[34m" + "MUNCHAT".center(50) + "\033[0m")  # Mavi renk
        print("\n[1] Mesaj Gönder")
        print("[2] Mesajları Görüntüle")
        print("[0] Çıkış\n")

        secim = input("Seçiminiz: ")

        if secim == "1":
            mesaj_gonder()
        elif secim == "2":
            mesaj_kontrol()
        elif secim == "0":
            temizle()
            print("Çıkış yapılıyor...")
            time.sleep(1)
            break
        else:
            print("\nGeçersiz seçim!")
            time.sleep(1)

# Programı çalıştır
if __name__ == "__main__":
    menu()
