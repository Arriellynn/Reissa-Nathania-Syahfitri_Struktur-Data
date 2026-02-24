"""
╔══════════════════════════════════════════════════════════════╗
║              SIMULASI BUKU TELEFON - Python                  ║
║              Aplikasi Pengurusan Kenalan                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
from datetime import datetime

# ─────────────────────────────────────────────
#  Data penyimpanan kenalan (dalam memori)
# ─────────────────────────────────────────────
buku_telefon = {}

FILE_DATA = "kenalan.json"


# ─────────────────────────────────────────────
#  Fungsi Utiliti
# ─────────────────────────────────────────────

def bersih_skrin():
    os.system('cls' if os.name == 'nt' else 'clear')


def tekan_enter():
    input("\n  [Tekan ENTER untuk kembali ke menu...] ")


def cetak_garis(simbol="═", panjang=60):
    print("  " + simbol * panjang)


def cetak_tajuk(tajuk):
    bersih_skrin()
    cetak_garis("═")
    print(f"  {'BUKU TELEFON':^58}")
    print(f"  {tajuk:^58}")
    cetak_garis("═")
    print()


# ─────────────────────────────────────────────
#  Fungsi Simpan & Muatkan Data (JSON)
# ─────────────────────────────────────────────

def simpan_data():
    with open(FILE_DATA, "w", encoding="utf-8") as f:
        json.dump(buku_telefon, f, ensure_ascii=False, indent=2)
    print("\n  ✔  Data berjaya disimpan ke fail '{}'.".format(FILE_DATA))


def muatkan_data():
    global buku_telefon
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r", encoding="utf-8") as f:
            buku_telefon = json.load(f)
        print(f"  ✔  {len(buku_telefon)} kenalan dimuatkan daripada '{FILE_DATA}'.")
    else:
        buku_telefon = {}


# ─────────────────────────────────────────────
#  1. Tambah Kenalan
# ─────────────────────────────────────────────

def tambah_kenalan():
    cetak_tajuk("➕  TAMBAH KENALAN BARU")

    nama = input("  Nama Penuh   : ").strip()
    if not nama:
        print("\n  ✘  Nama tidak boleh kosong!")
        tekan_enter()
        return

    if nama.lower() in [k.lower() for k in buku_telefon]:
        print(f"\n  ✘  Kenalan '{nama}' sudah wujud!")
        tekan_enter()
        return

    nombor  = input("  No. Telefon  : ").strip()
    emel    = input("  E-mel        : ").strip()
    alamat  = input("  Alamat       : ").strip()
    catatan = input("  Catatan      : ").strip()

    buku_telefon[nama] = {
        "nombor" : nombor,
        "emel"   : emel,
        "alamat" : alamat,
        "catatan": catatan,
        "tarikh" : datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    print(f"\n  ✔  Kenalan '{nama}' berjaya ditambah!")
    simpan_data()
    tekan_enter()


# ─────────────────────────────────────────────
#  2. Papar Semua Kenalan
# ─────────────────────────────────────────────

def papar_semua():
    cetak_tajuk("📋  SENARAI SEMUA KENALAN")

    if not buku_telefon:
        print("  (Tiada kenalan dalam buku telefon)")
        tekan_enter()
        return

    senarai = sorted(buku_telefon.keys())
    print(f"  {'#':<4} {'NAMA':<25} {'NO. TELEFON':<20} {'E-MEL'}")
    cetak_garis("─")

    for i, nama in enumerate(senarai, 1):
        info   = buku_telefon[nama]
        nombor = info.get("nombor", "-")
        emel   = info.get("emel", "-")
        print(f"  {i:<4} {nama:<25} {nombor:<20} {emel}")

    cetak_garis("─")
    print(f"\n  Jumlah kenalan: {len(buku_telefon)}")
    tekan_enter()


# ─────────────────────────────────────────────
#  3. Cari Kenalan
# ─────────────────────────────────────────────

def cari_kenalan():
    cetak_tajuk("🔍  CARI KENALAN")

    kata_kunci = input("  Masukkan nama / no. telefon / e-mel : ").strip().lower()
    if not kata_kunci:
        tekan_enter()
        return

    hasil = []
    for nama, info in buku_telefon.items():
        if (kata_kunci in nama.lower()
                or kata_kunci in info.get("nombor", "").lower()
                or kata_kunci in info.get("emel", "").lower()):
            hasil.append((nama, info))

    if not hasil:
        print(f"\n  ✘  Tiada kenalan ditemui untuk '{kata_kunci}'.")
    else:
        print(f"\n  Ditemui {len(hasil)} kenalan:\n")
        for nama, info in hasil:
            cetak_garis("─")
            _cetak_maklumat(nama, info)

    cetak_garis("─")
    tekan_enter()


def _cetak_maklumat(nama, info):
    print(f"  👤  Nama    : {nama}")
    print(f"      Telefon : {info.get('nombor', '-')}")
    print(f"      E-mel   : {info.get('emel', '-')}")
    print(f"      Alamat  : {info.get('alamat', '-')}")
    print(f"      Catatan : {info.get('catatan', '-')}")
    print(f"      Ditambah: {info.get('tarikh', '-')}")


# ─────────────────────────────────────────────
#  4. Kemaskini Kenalan
# ─────────────────────────────────────────────

def kemaskini_kenalan():
    cetak_tajuk("✏️   KEMASKINI KENALAN")

    nama = input("  Nama kenalan yang ingin dikemaskini : ").strip()

    kunci_sebenar = None
    for k in buku_telefon:
        if k.lower() == nama.lower():
            kunci_sebenar = k
            break

    if not kunci_sebenar:
        print(f"\n  ✘  Kenalan '{nama}' tidak ditemui.")
        tekan_enter()
        return

    info = buku_telefon[kunci_sebenar]
    print(f"\n  Maklumat semasa untuk '{kunci_sebenar}':")
    cetak_garis("─")
    _cetak_maklumat(kunci_sebenar, info)
    cetak_garis("─")

    print("\n  (Tekan ENTER untuk kekalkan nilai asal)\n")
    nombor  = input(f"  No. Telefon [{info.get('nombor','')}] : ").strip() or info.get("nombor", "")
    emel    = input(f"  E-mel       [{info.get('emel','')}] : ").strip() or info.get("emel", "")
    alamat  = input(f"  Alamat      [{info.get('alamat','')}] : ").strip() or info.get("alamat", "")
    catatan = input(f"  Catatan     [{info.get('catatan','')}] : ").strip() or info.get("catatan", "")

    buku_telefon[kunci_sebenar].update({
        "nombor" : nombor,
        "emel"   : emel,
        "alamat" : alamat,
        "catatan": catatan,
    })

    print(f"\n  ✔  Maklumat '{kunci_sebenar}' berjaya dikemaskini!")
    simpan_data()
    tekan_enter()


# ─────────────────────────────────────────────
#  5. Padam Kenalan
# ─────────────────────────────────────────────

def padam_kenalan():
    cetak_tajuk("🗑️   PADAM KENALAN")

    nama = input("  Nama kenalan yang ingin dipadam : ").strip()

    kunci_sebenar = None
    for k in buku_telefon:
        if k.lower() == nama.lower():
            kunci_sebenar = k
            break

    if not kunci_sebenar:
        print(f"\n  ✘  Kenalan '{nama}' tidak ditemui.")
        tekan_enter()
        return

    print(f"\n  Maklumat kenalan:")
    cetak_garis("─")
    _cetak_maklumat(kunci_sebenar, buku_telefon[kunci_sebenar])
    cetak_garis("─")

    sahkan = input(f"\n  Adakah anda pasti ingin memadam '{kunci_sebenar}'? (y/n) : ").strip().lower()
    if sahkan == 'y':
        del buku_telefon[kunci_sebenar]
        print(f"\n  ✔  Kenalan '{kunci_sebenar}' berjaya dipadam.")
        simpan_data()
    else:
        print("\n  ✘  Pemadaman dibatalkan.")

    tekan_enter()


# ─────────────────────────────────────────────
#  6. Lihat Butiran Kenalan
# ─────────────────────────────────────────────

def lihat_butiran():
    cetak_tajuk("ℹ️   BUTIRAN KENALAN")

    nama = input("  Nama kenalan : ").strip()

    kunci_sebenar = None
    for k in buku_telefon:
        if k.lower() == nama.lower():
            kunci_sebenar = k
            break

    if not kunci_sebenar:
        print(f"\n  ✘  Kenalan '{nama}' tidak ditemui.")
    else:
        cetak_garis("─")
        _cetak_maklumat(kunci_sebenar, buku_telefon[kunci_sebenar])
        cetak_garis("─")

    tekan_enter()


# ─────────────────────────────────────────────
#  7. Statistik
# ─────────────────────────────────────────────

def statistik():
    cetak_tajuk("📊  STATISTIK BUKU TELEFON")

    jumlah      = len(buku_telefon)
    ada_emel    = sum(1 for v in buku_telefon.values() if v.get("emel"))
    ada_alamat  = sum(1 for v in buku_telefon.values() if v.get("alamat"))
    ada_catatan = sum(1 for v in buku_telefon.values() if v.get("catatan"))

    cetak_garis("─")
    print(f"  Jumlah kenalan          : {jumlah}")
    print(f"  Kenalan dengan e-mel    : {ada_emel}")
    print(f"  Kenalan dengan alamat   : {ada_alamat}")
    print(f"  Kenalan dengan catatan  : {ada_catatan}")
    cetak_garis("─")

    if jumlah > 0:
        print("\n  5 Kenalan Terbaru:")
        terbaru = sorted(buku_telefon.items(),
                         key=lambda x: x[1].get("tarikh", ""),
                         reverse=True)[:5]
        for nama, info in terbaru:
            print(f"    • {nama}  ({info.get('tarikh','-')})")

    tekan_enter()


# ─────────────────────────────────────────────
#  Menu Utama
# ─────────────────────────────────────────────

def menu_utama():
    muatkan_data()

    while True:
        bersih_skrin()
        cetak_garis("═")
        print(f"  {'📞  BUKU TELEFON DIGITAL':^58}")
        print(f"  {'Sistem Pengurusan Kenalan v1.0':^58}")
        cetak_garis("═")
        print()
        print("  [1]  ➕  Tambah Kenalan Baru")
        print("  [2]  📋  Papar Semua Kenalan")
        print("  [3]  🔍  Cari Kenalan")
        print("  [4]  ✏️   Kemaskini Maklumat Kenalan")
        print("  [5]  🗑️   Padam Kenalan")
        print("  [6]  ℹ️   Lihat Butiran Kenalan")
        print("  [7]  📊  Statistik")
        print("  [0]  🚪  Keluar")
        print()
        cetak_garis("─")
        print(f"  Kenalan dalam buku : {len(buku_telefon)}")
        cetak_garis("─")

        pilihan = input("\n  Pilih menu [0-7] : ").strip()

        if   pilihan == "1": tambah_kenalan()
        elif pilihan == "2": papar_semua()
        elif pilihan == "3": cari_kenalan()
        elif pilihan == "4": kemaskini_kenalan()
        elif pilihan == "5": padam_kenalan()
        elif pilihan == "6": lihat_butiran()
        elif pilihan == "7": statistik()
        elif pilihan == "0":
            bersih_skrin()
            cetak_garis("═")
            print(f"  {'Terima kasih kerana menggunakan Buku Telefon!':^58}")
            print(f"  {'Jumpa lagi! 👋':^58}")
            cetak_garis("═")
            print()
            break
        else:
            print("\n  ✘  Pilihan tidak sah. Sila pilih 0 hingga 7.")
            tekan_enter()


# ─────────────────────────────────────────────
#  Titik Masuk Program
# ─────────────────────────────────────────────

if __name__ == "__main__":
    menu_utama()
