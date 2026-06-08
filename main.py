import json
from datetime import date, timedelta
from abc import ABC, abstractmethod

class Uye(ABC):

    def __init__(self, uye_id, sifre, isim, soyisim, telefon, e_posta):
        self.__uye_id = uye_id
        self.__sifre = sifre
        self.__isim = isim
        self.__soyisim = soyisim
        self.__telefon = telefon
        self.__e_posta = e_posta

    @property
    def uye_id(self):
        return self.__uye_id

    @property
    def isim(self):
        return self.__isim

    @property
    def soyisim(self):
        return self.__soyisim

    @property
    def telefon(self):
        return self.__telefon

    @telefon.setter
    def telefon(self, yeni_telefon):
        if len(yeni_telefon) < 10:
            raise ValueError("Geçersiz telefon numarası")
        self.__telefon = yeni_telefon

    @property
    def e_posta(self):
        return self.__e_posta

    @e_posta.setter
    def e_posta(self, yeni_eposta):
        if "@" not in yeni_eposta:
            raise ValueError("Geçersiz e-posta")
        self.__e_posta = yeni_eposta

class Musteri(Uye):

    ODUNC_LIMITI = 5
    ODUNC_SURESI = 14

    def __init__(self, uye_id, sifre, isim, soyisim,
                 telefon, e_posta, toplam_gecikme):
        super().__init__(uye_id, sifre, isim, soyisim,
                         telefon, e_posta)

        self.toplam_gecikme = toplam_gecikme

    def dosyaya_kaydet(self):
        return {
            "tip": "musteri",
            "uye_id": self._uye_id,
            "isim": self._isim,
            "soyisim": self._soyisim,
            "telefon": self._telefon,
            "e_posta": self._e_posta,
            "toplam_gecikme": self.toplam_gecikme
        }

class Personel(Uye):

    def dosyaya_kaydet(self):
        return {
            "tip": "personel",
            "uye_id": self._uye_id,
            "isim": self._isim,
            "soyisim": self._soyisim,
            "telefon": self._telefon,
            "e_posta": self._e_posta
        }

class Kitap:

    def __init__(self, kitap_id, kitap_ismi, yazar, sayfa, tur, okunma_sayisi):
        self.kitap_id = kitap_id
        self.kitap_ismi = kitap_ismi
        self.yazar = yazar
        self.sayfa = sayfa
        self.tur = tur
        self.okunma_sayisi = okunma_sayisi
        self.odunc_alindi = False

    def dosyaya_kitap(self):
        return {
        "kitap_id": self.kitap_id,
        "kitap_ismi": self.kitap_ismi,
        "yazar": self.yazar,
        "sayfa": self.sayfa,
        "tur": self.tur,
        "okunma_sayisi": self.okunma_sayisi,
        "odunc_alindi": self.odunc_alindi
    }

class OduncAlma:
    def __init__(self, uye_id, kitap_id):
        self.uye_id = uye_id
        self.kitap_id = kitap_id
        self.alinan_tarihi = date.today()
        self.getirme_tarihi = date.today() + timedelta(days=uye_id.ODUNC_SURESI)

# İlk ödev gibi olacak zannetmiştim :(
# Ama çok şey öğrendim, sadece Pyhton değil genel olarak programcılık üzerine

def login():
    with open("database.json", "r", encoding="utf-8") as f:
       veri = json.load(f)

    uye_bilgileri = veri["uyeler"]
    kitap_bilgileri = veri["kitaplar"]

    print("======= MENÜ =======")
    uye_id = input("ID'nizi giriniz:")

    bulunan_uye = None
    for uye_bilgisi in uye_bilgileri:
        if uye_bilgisi["uye_id"] == uye_id:
            bulunan_uye = uye_bilgisi
            break

    if bulunan_uye:
        sifre = input("Şifrenizi giriniz:")
        if bulunan_uye["sifre"] == sifre:
            return uye_id, int(uye_id) % 23
        else:
            print("Şifre hatalı.")
    else:
        print("Üye bulunamadı.")

def musteri_menu(uye_id):
    kapali = False
    while kapali == False:
        print("======= MENÜ =======")
        print("Ödünç aldığınız kitaplar için [1]")
        print("Kitap aramak için             [2]")
        print("Kitap listelemek için         [3]")
        print("Geciken kitaplarınız için     [4]")
        print("Kitap ödünç almak için        [5]")
        print("Kitap teslim etmek için       [6]")
        print("Çıkış yapmak için             [7]")
        secenek = input()

        match int(secenek):
            case 1:
                odunc_aldigim_kitaplar(uye_id)
            case 2:
                kitap_ara()
            case 3:
                kitap_listele()
            case 4:
                geciken_kitaplar(uye_id)
            case 5:
                kitap_odunc_al(uye_id)
            case 6:
                kitap_teslim_et(uye_id)
            case 7:
                kapali = True
                break
            case _:
                print("Geçerli bir seçeneği giriniz")

def personel_menu():
    kapali = False
    while kapali == False:
        print("======= MENÜ =======")
        print("Kullanıcı listesi için  [1]")
        print("Kitap listesi için      [2]")
        print("Kullanıcı eklemek için  [3]")
        print("Kullanıcı çıkarmak için [4]")
        print("Kitap eklemek için      [5]")
        print("Kitap çıkarmak için     [6]")
        print("En çok okunan kitaplar  [7]")
        print("Çıkış yapmak için       [8]")
        secenek = input()

        match int(secenek):
            case 1:
                uye_listele()
            case 2:
                kitap_listele()
            case 3:
                uye_ekle()
            case 4:
                uye_cikar()
            case 5:
                kitap_ekle()
            case 6:
                kitap_cikar()
            case 7:
                en_cok_okunan_kitaplar()
            case 8:
                kapali = True
                break
            case _:
                print("Geçerli bir seçeneği giriniz")


def odunc_aldigim_kitaplar(uye_id):
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    aktif_kiralamalar = [
        o for o in veri["odunc_almalar"]
        if str(o["uye_id"]) == str(uye_id) and not o["teslim_edildi"]
    ]

    if len(aktif_kiralamalar) == 0:
        print("Kiralanan kitabınız bulunmamaktadır.")
        return

    print("\n======= KİRALADIĞINIZ KİTAPLAR =======")
    for odunc in aktif_kiralamalar:
        kitap_ismi = "Bilinmiyor"
        for kitap in veri["kitaplar"]:
            if str(kitap["kitap_id"]) == str(odunc["kitap_id"]):
                kitap_ismi = kitap["kitap_ismi"]
                break

        bugun = date.today()
        getirme_tarihi = date.fromisoformat(odunc["getirme_tarihi"])
        kalan_gun = (getirme_tarihi - bugun).days

        if kalan_gun < 0:
            durum = f"{abs(kalan_gun)} gün gecikmiş!"
        else:
            durum = f"{kalan_gun} gün kaldı"

        print(f"Kitap: {kitap_ismi} | Alınan: {odunc['alinan_tarih']} | Teslim: {odunc['getirme_tarihi']} | Durum: {durum}")
    print("=======================================\n")

def en_cok_okunan_kitaplar():
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    kitaplar = veri["kitaplar"]

    if len(kitaplar) == 0:
        print("Kayıtlı kitap bulunmamaktadır.")
        return

    sirali_kitaplar = sorted(
        kitaplar,
        key=lambda kitap: kitap["okunma_sayisi"],
        reverse=True
    )

    print("\n======= EN ÇOK OKUNAN KİTAPLAR =======")

    for sira, kitap in enumerate(sirali_kitaplar, start=1):
        print(
            f"{sira}. {kitap['kitap_ismi']} | "
            f"Yazar: {kitap['yazar']} | "
            f"Okunma Sayısı: {kitap['okunma_sayisi']}"
        )

    print("======================================\n")

def kitap_odunc_al(uye_id):
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    aktif_kiralamalar = [
        o for o in veri["odunc_almalar"]
        if str(o["uye_id"]) == str(uye_id) and not o["teslim_edildi"]
    ]

    if len(aktif_kiralamalar) >= 5:
        print("Kiralama limitinize ulaştınız (max 5 kitap).")
        return

    kitap_id = input("Kiralamak istediğiniz kitabın ID'si: ")

    bulunan_kitap = None
    for kitap in veri["kitaplar"]:
        if str(kitap["kitap_id"]) == kitap_id:
            bulunan_kitap = kitap
            break

    if not bulunan_kitap:
        print("Kitap bulunamadı.")
        return

    if bulunan_kitap["odunc_alindi"]:
        print("Bu kitap şu an başkasında.")
        return

    bulunan_kitap["odunc_alindi"] = True
    bulunan_kitap["okunma_sayisi"] += 1

    alinan_tarih = str(date.today())
    getirme_tarihi = str(date.today() + timedelta(days=14))

    yeni_odunc = {
        "uye_id": uye_id,
        "kitap_id": kitap_id,
        "alinan_tarih": alinan_tarih,
        "getirme_tarihi": getirme_tarihi,
        "teslim_edildi": False
    }

    veri["odunc_almalar"].append(yeni_odunc)

    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

    print(f"'{bulunan_kitap['kitap_ismi']}' kitabı kiralandı.")
    print(f"Teslim tarihi: {getirme_tarihi}")

def kitap_teslim_et(uye_id):
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    aktif_kiralamalar = [
        o for o in veri["odunc_almalar"]
        if str(o["uye_id"]) == str(uye_id) and not o["teslim_edildi"]
    ]

    if len(aktif_kiralamalar) == 0:
        print("Teslim edilecek kitabınız bulunmamaktadır.")
        return

    print("\n======= AKTİF KİTAPLAR =======")
    for odunc in aktif_kiralamalar:
        kitap_ismi = "Bilinmiyor"

        for kitap in veri["kitaplar"]:
            if str(kitap["kitap_id"]) == str(odunc["kitap_id"]):
                kitap_ismi = kitap["kitap_ismi"]
                break

        print(f"ID: {odunc['kitap_id']} | Kitap: {kitap_ismi}")

    kitap_id = input("\nTeslim etmek istediğiniz kitabın ID'si: ")

    bulunan_odunc = None
    for odunc in aktif_kiralamalar:
        if str(odunc["kitap_id"]) == str(kitap_id):
            bulunan_odunc = odunc
            break

    if not bulunan_odunc:
        print("Bu kitaba ait aktif kiralama bulunamadı.")
        return
    
    bulunan_odunc["teslim_edildi"] = True

    for kitap in veri["kitaplar"]:
        if str(kitap["kitap_id"]) == str(kitap_id):
            kitap["odunc_alindi"] = False
            kitap_ismi = kitap["kitap_ismi"]
            break

    bugun = date.today()
    teslim_tarihi = date.fromisoformat(bulunan_odunc["getirme_tarihi"])

    if bugun > teslim_tarihi:
        gecikme_gunu = (bugun - teslim_tarihi).days

        for uye in veri["uyeler"]:
            if str(uye["uye_id"]) == str(uye_id):
                uye["toplam_gecikme"] += gecikme_gunu
                break

        print(f"Kitap {gecikme_gunu} gün gecikmeli teslim edildi.")
    else:
        print("Kitap zamanında teslim edildi.")

    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

    print(f"'{kitap_ismi}' kitabı başarıyla teslim edildi.")

def kitap_ara():
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    print("Arama kriteri seçiniz:")
    print("[1] Kitap adı")
    print("[2] Yazar")
    print("[3] Tür")
    kriter = input()

    arama = input("Aranacak kelime: ").lower()

    match int(kriter):
        case 1:
            sonuclar = [k for k in veri["kitaplar"] if arama in k["kitap_ismi"].lower()]
        case 2:
            sonuclar = [k for k in veri["kitaplar"] if arama in k["yazar"].lower()]
        case 3:
            sonuclar = [k for k in veri["kitaplar"] if arama in k["tur"].lower()]
        case _:
            print("Geçersiz seçenek.")
            return

    if len(sonuclar) == 0:
        print("Sonuç bulunamadı.")
        return

    print(f"\n{len(sonuclar)} sonuç bulundu:")
    print("======= ARAMA SONUÇLARI =======")
    for kitap in sonuclar:
        durum = "Ödünçte" if kitap["odunc_alindi"] else "Müsait"
        print(f"ID: {kitap['kitap_id']} | İsim: {kitap['kitap_ismi']} | Yazar: {kitap['yazar']} | Tür: {kitap['tur']} | Durum: {durum}")
    print("================================\n")

def geciken_kitaplar(uye_id):
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    bugun = date.today()
    gecikme_var = False

    print("\n======= GECİKEN KİTAPLARINIZ =======")
    for odunc in veri["odunc_almalar"]:
        if str(odunc["uye_id"]) == str(uye_id) and not odunc["teslim_edildi"]:
            getirme_tarihi = date.fromisoformat(odunc["getirme_tarihi"])

            if bugun > getirme_tarihi:
                gecikme_var = True
                gecikme_gun = (bugun - getirme_tarihi).days

                kitap_ismi = "Bilinmiyor"
                for kitap in veri["kitaplar"]:
                    if str(kitap["kitap_id"]) == str(odunc["kitap_id"]):
                        kitap_ismi = kitap["kitap_ismi"]
                        break

                print(f"Kitap: {kitap_ismi} | Teslim tarihi: {odunc['getirme_tarihi']} | Gecikme: {gecikme_gun} gün")

    if not gecikme_var:
        print("Geciken kitabınız bulunmamaktadır.")
    print("=====================================\n")

def uye_listele():
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    uyeler = veri["uyeler"]

    if len(uyeler) == 0:
        print("Kayıtlı üye bulunmamaktadır.")
        return

    print("\n======= ÜYE LİSTESİ =======")
    for uye in uyeler:
        print(f"ID: {uye['uye_id']} | Ad Soyad: {uye['isim']} {uye['soyisim']} | Telefon: {uye['telefon']} | E-posta: {uye['e_posta']} | Toplam Gecikme: {uye['toplam_gecikme']}")
    print("============================\n")

def kitap_listele():
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    kitaplar = veri["kitaplar"]

    if len(kitaplar) == 0:
        print("Kayıtlı kitap bulunmamaktadır.")
        return

    print("\n======= KİTAP LİSTESİ =======")
    for kitap in kitaplar:
        durum = "Ödünçte" if kitap["odunc_alindi"] else "Müsait"
        print(f"ID: {kitap['kitap_id']} | İsim: {kitap['kitap_ismi']} | Yazar: {kitap['yazar']} | Tür: {kitap['tur']} | Sayfa: {kitap['sayfa']} | Okunma: {kitap['okunma_sayisi']} | Durum: {durum}")
    print("==============================\n")

def kitap_ekle():
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    kitap_id = input("Kitap ID: ")
    kitap_ismi = input("Kitap ismi: ")
    yazar = input("Yazar: ")
    sayfa = input("Sayfa sayısı: ")
    tur = input("Tür: ")

    yeni_kitap = {
        "kitap_id": kitap_id,
        "kitap_ismi": kitap_ismi,
        "yazar": yazar,
        "sayfa": int(sayfa),
        "tur": tur,
        "okunma_sayisi": 0,
        "odunc_alindi": False
    }

    veri["kitaplar"].append(yeni_kitap)

    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

    print(f"'{kitap_ismi}' kitabı eklendi.")

def kitap_cikar():
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    kitap_id = input("Çıkarılacak kitabın ID'si: ")

    bulunan_kitap = None
    for kitap in veri["kitaplar"]:
        if str(kitap["kitap_id"]) == kitap_id:
            bulunan_kitap = kitap
            break

    if bulunan_kitap:
        if bulunan_kitap["odunc_alindi"]:
            print("Bu kitap şu an ödünçte, çıkarılamaz.")
            return

        veri["kitaplar"].remove(bulunan_kitap)

        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)

        print(f"'{bulunan_kitap['kitap_ismi']}' kitabı silindi.")
    else:
        print("Kitap bulunamadı.")

def uye_ekle():
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    uye_id = input("Üye ID: ")
    sifre = input("Şifre: ")
    isim = input("İsim: ")
    soyisim = input("Soyisim: ")
    telefon = input("Telefon: ")
    e_posta = input("E-posta: ")

    for uye in veri["uyeler"]:
        if str(uye["uye_id"]) == uye_id:
            print("Bu ID zaten kullanımda.")
            return

    yeni_uye = {
        "uye_id": uye_id,
        "sifre": sifre,
        "isim": isim,
        "soyisim": soyisim,
        "telefon": telefon,
        "e_posta": e_posta,
        "toplam_gecikme": 0
    }

    veri["uyeler"].append(yeni_uye)

    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)

    print(f"'{isim} {soyisim}' üye olarak eklendi.")

def uye_cikar():
    with open("database.json", "r", encoding="utf-8") as f:
        veri = json.load(f)

    uye_id = input("Çıkarılacak üyenin ID'si: ")

    bulunan_uye = None
    for uye in veri["uyeler"]:
        if str(uye["uye_id"]) == uye_id:
            bulunan_uye = uye
            break

    if bulunan_uye:
        veri["uyeler"].remove(bulunan_uye)

        with open("database.json", "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=2)

        print(f"'{bulunan_uye['isim']} {bulunan_uye['soyisim']}' üye listesinden silindi.")
    else:
        print("Üye bulunamadı.")


def main():
    aktif_uye_id, yetki = login()
    if yetki != 0:
        musteri_menu(aktif_uye_id)
    elif yetki == 0:
        personel_menu()

main()