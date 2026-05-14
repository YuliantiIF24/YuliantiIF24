import hashlib
import json

def buat_hash_md5(data: dict) -> str:
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

def input_data_user(label: str) -> dict:
    print(f"\n{'='*40}")
    print(f"  INPUT DATA {label}")
    print(f"{'='*40}")
    nama  = input("  Nama     : ").strip()
    email = input("  Email    : ").strip()
    hp    = input("  Nomor HP : ").strip()
    return {"nama": nama, "email": email, "nomor_hp": hp}

def tampilkan_profil(data: dict):
    print(f"    Nama     : {data['nama']}")
    print(f"    Email    : {data['email']}")
    print(f"    Nomor HP : {data['nomor_hp']}")

def main():
    print("╔══════════════════════════════════════════╗")
    print("║   SISTEM DETEKSI PERUBAHAN PROFIL USER   ║")
    print("║          (MD5 Checksum Method)           ║")
    print("╚══════════════════════════════════════════╝")

    data_awal = input_data_user("AWAL")

    hash_awal = buat_hash_md5(data_awal)
    print(f"\n✔  Hash MD5 awal berhasil disimpan.")
    print(f"   Hash Awal : {hash_awal}")

    input("\nTekan [Enter] untuk memasukkan data baru...")
    data_baru = input_data_user("BARU")

    hash_baru = buat_hash_md5(data_baru)

    print(f"\n{'='*44}")
    print("  HASIL PERBANDINGAN HASH MD5")
    print(f"{'='*44}")
    print(f"  Hash Lama : {hash_awal}")
    print(f"  Hash Baru : {hash_baru}")
    print(f"{'='*44}")

    print("\n  DATA PROFIL LAMA:")
    tampilkan_profil(data_awal)
    print("\n  DATA PROFIL BARU:")
    tampilkan_profil(data_baru)

    print(f"\n{'='*44}")
    if hash_awal == hash_baru:
        print("  STATUS : ✅  DATA TIDAK BERUBAH")
        print("  Tidak ada modifikasi yang terdeteksi.")
    else:
        print("  STATUS : ⚠️   DATA TELAH BERUBAH / DIMODIFIKASI!")
        print("  Perubahan terdeteksi pada profil user.")

        perubahan = []
        for field in ["nama", "email", "nomor_hp"]:
            if data_awal[field] != data_baru[field]:
                perubahan.append(field)
        print(f"\n  Field yang berubah: {', '.join(perubahan)}")
    print(f"{'='*44}\n")

if __name__ == "__main__":
    main()