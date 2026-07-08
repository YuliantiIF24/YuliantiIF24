"""
=====================================================================
 PROGRAM ALGORITMA GENETIKA UNTUK PENCARIAN KATA
 DALAM KAMUS BAHASA DAERAH (BAHASA BUGIS)
=====================================================================
 Nama   : Yulianti
 NIM    : 105841116224
 Prodi  : Informatika
=====================================================================
"""

import random


# =====================================================================
# 0. KODE WARNA UNTUK OUTPUT TERMINAL (ANSI escape code)
# =====================================================================
class Warna:
    RESET   = "\033[0m"
    JUDUL   = "\033[1;36m"   # cyan tebal   -> judul menu utama
    HEADER  = "\033[1;33m"   # kuning tebal -> judul hasil/perhitungan tiap menu
    DATA    = "\033[0;36m"   # cyan         -> data kata/kromosom
    ANGKA   = "\033[0;35m"   # magenta      -> angka fitness/probabilitas
    SUKSES  = "\033[1;32m"   # hijau tebal  -> pesan berhasil/ditemukan
    ERROR   = "\033[1;31m"   # merah tebal  -> pesan error/gagal/tidak ditemukan
    INFO    = "\033[0;37m"   # putih        -> info/petunjuk lanjutan


def cetak_judul(teks):
    print(f"\n{Warna.JUDUL}{teks}{Warna.RESET}")


def cetak_header(teks):
    print(f"\n{Warna.HEADER}{teks}{Warna.RESET}")


def cetak_data(teks):
    print(f"{Warna.DATA}{teks}{Warna.RESET}")


def cetak_sukses(teks):
    print(f"{Warna.SUKSES}{teks}{Warna.RESET}")


def cetak_error(teks):
    print(f"{Warna.ERROR}{teks}{Warna.RESET}")


def cetak_info(teks):
    print(f"{Warna.INFO}{teks}{Warna.RESET}")

# =====================================================================
# 1. DATASET KAMUS BAHASA BUGIS (minimal 10 data kata)
# =====================================================================
kamus = [
    {"bugis": "bola",  "arti": "rumah"},
    {"bugis": "jari",  "arti": "tangan"},
    {"bugis": "bosi",  "arti": "hujan"},
    {"bugis": "esso",  "arti": "hari"},
    {"bugis": "wenni", "arti": "malam"},
    {"bugis": "piso",  "arti": "pisau"},
    {"bugis": "waju",  "arti": "baju"},
    {"bugis": "liwe",  "arti": "sangat"},
    {"bugis": "lopi",  "arti": "perahu"},
    {"bugis": "aseng", "arti": "nama"},
    {"bugis": "jokka", "arti": "jalan"},
    {"bugis": "bale",  "arti": "ikan"},
    {"bugis": "atau",  "arti": "kanan"},
    {"bugis": "lawo",  "arti": "labu"},
    {"bugis": "pitu",  "arti": "tujuh"},
    {"bugis": "lipa'",  "arti": "sarung"},
    {"bugis": "magai",  "arti": "kenapa"},

]

# Alfabet yang digunakan untuk membangkitkan individu (gen) secara acak
ALPHABET = "abcdefghijklmnopqrstuvwxyz'"
UKURAN_POPULASI = 10   # jumlah individu dalam satu populasi
LAJU_MUTASI = 0.1      # peluang mutasi per gen (huruf)


# =====================================================================
# 2. KELAS ALGORITMA GENETIKA
# =====================================================================
class GA:
    def __init__(self):
        self.target = None
        self.populasi = []
        self.fitness = []
        self.probabilitas = []
        self.terpilih = []
        self.hasil_crossover = []
        self.detail_crossover = []
        self.hasil_mutasi = []
        self.detail_mutasi = []
        self.generasi = 0

    def buat_individu_acak(self, jumlah, panjang):
        return ["".join(random.choice(ALPHABET) for _ in range(panjang))
                for _ in range(jumlah)]

    def set_target(self, kata, populasi):
        """Inisialisasi target pencarian & populasi awal (Generasi ke-0)
        dengan populasi yang SUDAH ditentukan (input manual atau acak)."""
        self.target = kata
        self.generasi = 0
        self.populasi = populasi
        self.fitness = []
        self.terpilih = []
        self.hasil_crossover = []
        self.hasil_mutasi = []

    def hitung_fitness_individu(self, individu):
        cocok = sum(1 for a, b in zip(individu, self.target) if a == b)
        return cocok / len(self.target)

    def hitung_semua_fitness(self):
        self.fitness = [self.hitung_fitness_individu(ind) for ind in self.populasi]
        return self.fitness

    def seleksi_roulette(self):
        total = sum(self.fitness)
        if total == 0:
            self.probabilitas = [1 / len(self.fitness)] * len(self.fitness)
        else:
            self.probabilitas = [f / total for f in self.fitness]

        # Membuat interval kumulatif (metode Roulette Wheel Selection
        # sesuai materi: interval individu ke-i = [batas_bawah, batas_atas))
        interval = []
        batas_bawah = 0.0
        for p in self.probabilitas:
            batas_atas = batas_bawah + p
            interval.append((batas_bawah, batas_atas))
            batas_bawah = batas_atas
        self.interval = interval

        # "Memutar roda roulette" sebanyak ukuran populasi. Setiap putaran
        # menghasilkan satu angka acak [0,1) yang menentukan individu mana
        # yang terpilih berdasarkan interval tempat angka itu jatuh.
        terpilih = []
        angka_acak_list = []
        for _ in range(len(self.populasi)):
            r = random.random()
            angka_acak_list.append(r)
            for i, (bawah, atas) in enumerate(interval):
                batas_akhir = (i == len(interval) - 1)
                if bawah <= r < atas or (batas_akhir and r <= atas):
                    terpilih.append(self.populasi[i])
                    break
        self.terpilih = terpilih
        self.angka_acak = angka_acak_list
        return terpilih, self.probabilitas, interval, angka_acak_list

    def crossover(self):
        anak = []
        detail = []
        induk = self.terpilih[:]
        random.shuffle(induk)
        for i in range(0, len(induk) - 1, 2):
            p1, p2 = induk[i], induk[i + 1]
            titik = random.randint(1, len(p1) - 1) if len(p1) > 1 else 1
            a1 = p1[:titik] + p2[titik:]
            a2 = p2[:titik] + p1[titik:]
            anak.extend([a1, a2])
            detail.append((p1, p2, titik, a1, a2))
        if len(induk) % 2 == 1:
            anak.append(induk[-1])
        self.hasil_crossover = anak
        self.detail_crossover = detail
        return anak, detail

    def mutasi(self):
        hasil = []
        detail = []
        for individu in self.hasil_crossover:
            gen = list(individu)
            catatan = []
            for i in range(len(gen)):
                if random.random() < LAJU_MUTASI:
                    lama = gen[i]
                    gen[i] = random.choice(ALPHABET)
                    catatan.append((i, lama, gen[i]))
            hasil.append("".join(gen))
            detail.append(catatan)
        self.hasil_mutasi = hasil
        self.detail_mutasi = detail
        return hasil, detail

    def generasi_baru(self):
        # --- ELITISM ---
        # Simpan individu terbaik dari generasi SEBELUM ini, supaya tidak
        # hilang meskipun hasil crossover/mutasi generasi baru kebetulan
        # lebih buruk. Ini mencegah fitness terbaik menurun/hilang
        # (mencegah kejadian "mentok" karena gen penting hilang).
        if self.fitness:
            idx_elit = self.fitness.index(max(self.fitness))
            elit_individu = self.populasi[idx_elit]
            elit_fitness = self.fitness[idx_elit]
        else:
            elit_individu, elit_fitness = None, -1

        populasi_baru = self.hasil_mutasi[:]
        fitness_baru = [self.hitung_fitness_individu(ind) for ind in populasi_baru]

        if elit_individu is not None and elit_fitness > max(fitness_baru):
            idx_terlemah = fitness_baru.index(min(fitness_baru))
            populasi_baru[idx_terlemah] = elit_individu
            fitness_baru[idx_terlemah] = elit_fitness

        self.populasi = populasi_baru
        self.fitness = fitness_baru
        self.generasi += 1
        self.terpilih = []
        self.hasil_crossover = []
        self.hasil_mutasi = []
        return self.populasi, self.fitness


# =====================================================================
# 3. FUNGSI-FUNGSI KAMUS
# =====================================================================
def cari_kata(kata):
    for entri in kamus:
        if entri["bugis"].lower() == kata.lower():
            return entri
    return None


def tampilkan_kamus():
    cetak_judul("=== DATASET KAMUS BAHASA BUGIS ===")
    print(f"{'No':<4}{'Kata Bugis':<15}{'Arti':<20}")
    print("-" * 39)
    for i, e in enumerate(kamus, 1):
        cetak_data(f"{i:<4}{e['bugis']:<15}{e['arti']:<20}")


# =====================================================================
# 4. MENU UTAMA
# =====================================================================
def menu():
    ga = GA()
    while True:
        print(f"\n{Warna.JUDUL}=== Kamus Bahasa Daerah ==={Warna.RESET}")
        print("1. Tampilkan Kamus")
        print("2. Cari Kata")
        print("3. Jalankan Algoritma Genetika")
        print("4. Tampilkan Populasi")
        print("5. Hasil Fitness")
        print("6. Seleksi Roulette")
        print("7. Cross Over")
        print("8. Mutasi")
        print("9. Generasi Baru")
        print("10. Keluar")
        while True:
            pilihan = input("Pilih menu (1-10): ").strip()
            if pilihan in [str(i) for i in range(1, 11)]:
                break
            cetak_error("Pilihan tidak valid. Masukkan angka 1-10 saja.")

        if pilihan == "1":
            tampilkan_kamus()

        elif pilihan == "2":
            while True:
                kata = input("Masukkan kata Bugis yang dicari "
                             "(atau ketik 'batal' untuk kembali ke menu): ").strip()
                if kata.lower() == "batal":
                    break
                hasil = cari_kata(kata)
                if hasil:
                    cetak_sukses(f"Ditemukan! '{hasil['bugis']}' artinya '{hasil['arti']}'")
                    break
                else:
                    cetak_error(f"Kata '{kata}' tidak ditemukan dalam kamus. "
                                f"Coba masukkan kata lain (lihat menu 1 untuk daftar "
                                f"kata yang tersedia), atau ketik 'batal'.")

        elif pilihan == "3":
            hasil = None
            while True:
                kata = input("Masukkan kata target dari kamus untuk dicari via GA "
                             "(atau ketik 'batal' untuk kembali ke menu): ").strip()
                if kata.lower() == "batal":
                    break
                hasil = cari_kata(kata)
                if hasil:
                    break
                cetak_error(f"Kata '{kata}' tidak ada di kamus. Masukkan kata yang "
                            f"benar-benar terdapat di kamus (lihat menu 1 untuk "
                            f"daftar kata), atau ketik 'batal'.")
            if not hasil:
                continue

            target = hasil["bugis"]
            panjang = len(target)
            cetak_header(f"Target GA: '{target}' (arti: {hasil['arti']}), "
                          f"panjang {panjang} huruf")

            print("\nPilih metode pengisian populasi awal (Generasi ke-0):")
            print("  1. Input manual (kromosom ditentukan sendiri)")
            print("  2. Acak otomatis (dibangkitkan program)")
            while True:
                metode = input("Pilih (1/2): ").strip()
                if metode in ("1", "2"):
                    break
                cetak_error("Pilihan tidak dikenali. Ketik 1 untuk input manual "
                            "atau 2 untuk acak otomatis.")

            if metode == "1":
                while True:
                    jumlah_input = input(
                        f"Jumlah individu/kromosom pada populasi awal "
                        f"(disarankan {UKURAN_POPULASI}): ").strip()
                    try:
                        jumlah = int(jumlah_input)
                        if jumlah <= 0:
                            raise ValueError
                        break
                    except ValueError:
                        cetak_error("Masukkan angka bulat positif yang valid, "
                                    "contoh: 8")

                print(f"\nMasukkan {jumlah} kromosom, masing-masing HARUS "
                      f"terdiri dari {panjang} huruf (boleh huruf apa saja, "
                      f"bebas ditentukan sendiri):")
                populasi_manual = []
                for i in range(1, jumlah + 1):
                    while True:
                        individu = input(f"  Kromosom {i}: ").strip().lower()
                        if len(individu) != panjang:
                            cetak_error(f"    Panjang harus {panjang} huruf "
                                        f"(input kamu {len(individu)} huruf). "
                                        f"Masukkan ulang Kromosom {i}:")
                            continue
                        break
                    populasi_manual.append(individu)
                ga.set_target(target, populasi_manual)

            else:
                populasi_acak = ga.buat_individu_acak(UKURAN_POPULASI, panjang)
                ga.set_target(target, populasi_acak)

            cetak_header(f"Populasi awal (Generasi {ga.generasi}):")
            for i, ind in enumerate(ga.populasi, 1):
                cetak_data(f"  Individu {i}: {ind}")
            cetak_info("\nLanjutkan proses: menu 5 (Fitness) -> 6 (Roulette) -> "
                       "7 (Cross Over) -> 8 (Mutasi) -> 9 (Generasi Baru).")

        elif pilihan == "4":
            if not ga.populasi:
                cetak_error("Belum ada populasi. Jalankan menu 3 terlebih dahulu.")
                continue
            cetak_header(f"Populasi Generasi ke-{ga.generasi}:")
            for i, ind in enumerate(ga.populasi, 1):
                cetak_data(f"  Individu {i}: {ind}")

        elif pilihan == "5":
            if not ga.populasi:
                cetak_error("Belum ada populasi. Jalankan menu 3 terlebih dahulu.")
                continue
            fit = ga.hitung_semua_fitness()
            cetak_header(f"Perhitungan Fitness Generasi ke-{ga.generasi} "
                         f"(target: '{ga.target}'):")
            for i, (ind, f) in enumerate(zip(ga.populasi, fit), 1):
                cocok = sum(1 for a, b in zip(ind, ga.target) if a == b)
                print(f"  Individu {i}: {Warna.DATA}{ind:<10}{Warna.RESET} -> cocok "
                      f"{cocok}/{len(ga.target)} huruf -> fitness = "
                      f"{Warna.ANGKA}{f:.2f}{Warna.RESET}")
            terbaik = max(fit)
            cetak_info(f"Fitness terbaik: {terbaik:.2f}")
            if terbaik == 1.0:
                cetak_sukses(">>> Kata target berhasil ditemukan oleh Algoritma Genetika! <<<")

        elif pilihan == "6":
            if not ga.fitness:
                cetak_error("Hitung fitness terlebih dahulu lewat menu 5.")
                continue
            terpilih, prob, interval, angka_acak = ga.seleksi_roulette()
            total = sum(ga.fitness)
            cetak_header("Perhitungan Seleksi Roulette Wheel:")
            cetak_info(f"Total fitness populasi = {total:.2f}")
            print(f"\n  {'Individu':<10}{'Fitness':<10}{'Probabilitas':<14}{'Interval':<20}")
            for i, (ind, f, p, (bawah, atas)) in enumerate(
                    zip(ga.populasi, ga.fitness, prob, interval), 1):
                print(f"  {Warna.DATA}{ind:<10}{Warna.RESET}{Warna.ANGKA}{f:<10.2f}"
                      f"{p:<14.2%}{Warna.RESET}{bawah:.2f} - {atas:.2f}")

            cetak_header("Putaran Roulette Wheel (angka acak menentukan individu terpilih):")
            for i, (r, ind) in enumerate(zip(angka_acak, terpilih), 1):
                print(f"  Putaran {i}: angka acak = {Warna.ANGKA}{r:.2f}{Warna.RESET} "
                      f"-> terpilih: {Warna.SUKSES}{ind}{Warna.RESET}")

        elif pilihan == "7":
            if not ga.terpilih:
                cetak_error("Lakukan seleksi roulette terlebih dahulu lewat menu 6.")
                continue
            anak, detail = ga.crossover()
            cetak_header("Perhitungan Cross Over (metode: single-point crossover):")
            for idx, (p1, p2, titik, a1, a2) in enumerate(detail, 1):
                print(f"  Pasangan {idx}: Induk1={Warna.DATA}{p1}{Warna.RESET}  "
                      f"Induk2={Warna.DATA}{p2}{Warna.RESET}  (titik potong ke-{titik})")
                print(f"    -> Anak1 = {Warna.SUKSES}{a1}{Warna.RESET}")
                print(f"    -> Anak2 = {Warna.SUKSES}{a2}{Warna.RESET}")

        elif pilihan == "8":
            if not ga.hasil_crossover:
                cetak_error("Lakukan cross over terlebih dahulu lewat menu 7.")
                continue
            hasil, detail = ga.mutasi()
            cetak_header(f"Perhitungan Mutasi (laju mutasi = {LAJU_MUTASI:.0%} per huruf):")
            for i, (ind, mut) in enumerate(zip(hasil, detail), 1):
                if mut:
                    ket = ", ".join([f"posisi {p}: '{l}'->'{b}'" for p, l, b in mut])
                    print(f"  Individu {i}: {Warna.DATA}{ind:<10}{Warna.RESET} "
                          f"({Warna.SUKSES}mutasi -> {ket}{Warna.RESET})")
                else:
                    print(f"  Individu {i}: {Warna.DATA}{ind:<10}{Warna.RESET} "
                          f"(tidak ada mutasi)")

        elif pilihan == "9":
            if not ga.hasil_mutasi:
                cetak_error("Lakukan mutasi terlebih dahulu lewat menu 8.")
                continue
            populasi_baru, fitness_baru = ga.generasi_baru()
            cetak_header(f"=== Hasil Generasi ke-{ga.generasi} ===")
            for i, (ind, f) in enumerate(zip(populasi_baru, fitness_baru), 1):
                print(f"  Individu {i}: {Warna.DATA}{ind:<10}{Warna.RESET} -> "
                      f"fitness = {Warna.ANGKA}{f:.2f}{Warna.RESET}")
            terbaik = max(fitness_baru)
            cetak_info(f"Fitness terbaik generasi ke-{ga.generasi}: {terbaik:.2f}")
            if terbaik == 1.0:
                idx = fitness_baru.index(terbaik)
                cetak_sukses(f">>> Kata target '{ga.target}' BERHASIL ditemukan: "
                             f"{populasi_baru[idx]} <<<")
            else:
                cetak_info("Fitness belum sempurna. Lanjutkan ke generasi berikutnya "
                           "mulai dari menu 6 (Seleksi Roulette),")
                lanjut = input("atau ketik 'auto' untuk otomatis melanjutkan proses "
                               "sampai ketemu (Enter untuk kembali ke menu): ").strip().lower()
                if lanjut == "auto":
                    cetak_info("Memproses otomatis (seleksi roulette -> crossover -> "
                               "mutasi -> generasi baru) secara berulang...")
                    batas_generasi = 3000
                    while ga.generasi < batas_generasi and max(ga.fitness) < 1.0:
                        ga.seleksi_roulette()
                        ga.crossover()
                        ga.mutasi()
                        ga.generasi_baru()
                    if max(ga.fitness) == 1.0:
                        idx = ga.fitness.index(1.0)
                        cetak_sukses(f"\n>>> Ditemukan di Generasi ke-{ga.generasi}: "
                                     f"'{ga.populasi[idx]}' <<<")
                        cetak_header(f"Populasi akhir (Generasi ke-{ga.generasi}):")
                        for i, (ind, f) in enumerate(zip(ga.populasi, ga.fitness), 1):
                            print(f"  Individu {i}: {Warna.DATA}{ind:<10}{Warna.RESET} "
                                  f"-> fitness = {Warna.ANGKA}{f:.2f}{Warna.RESET}")
                    else:
                        cetak_error(f"Belum ditemukan hingga batas {batas_generasi} "
                                    f"generasi. Fitness terbaik saat ini: "
                                    f"{max(ga.fitness):.2f} pada generasi ke-{ga.generasi}.")

        elif pilihan == "10":
            cetak_sukses("Terima kasih telah menggunakan program. Sampai jumpa!")
            break


if __name__ == "__main__":
    menu()