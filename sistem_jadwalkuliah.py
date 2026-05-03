jadwal_existing = [
    {"mk": "Rekayasa Proses Bisnis", "dosen": "Yanti Andriyani", "waktu": "Senin 07.30-10.00", "ruang": "303"},
    {"mk": "Pengembangan Sistem Informasi Berbasis Web", "dosen": "Zaiful Bahri", "waktu": "Senin 07.30-10.00", "ruang": "PUSKOM"},
    {"mk": "Sistem Cerdas", "dosen": "Rahmad Kurniawan", "waktu": "Senin 10.10-12.40", "ruang": "301-A"},
    {"mk": "Komputasi Awan", "dosen": "Al Aminuddin", "waktu": "Senin 10.10-12.40", "ruang": "309"},
    {"mk": "Evaluasi Antarmuka Pengguna", "dosen": "Lina Purwanti", "waktu": "Senin 13.00-15.30", "ruang": "301-A"},
    {"mk": "Pemrograman Bahasa Alami", "dosen": "Tisha Melia", "waktu": "Senin 13.00-15.30", "ruang": "301-B"},
    {"mk": "Komputasi Awan", "dosen": "Al Aminuddin", "waktu": "Selasa 13.00-15.30", "ruang": "301-A"},
    {"mk": "Sistem Informasi Geografis", "dosen": "Gita Sastria", "waktu": "Selasa 13.00-15.30", "ruang": "309"},
    {"mk": "Pengembangan Sistem Informasi Berbasis Web", "dosen": "Zaiful Bahri", "waktu": "Selasa 13.00-15.30", "ruang": "PUSKOM"},
    {"mk": "Rekayasa Proses Bisnis", "dosen": "Yanti Andriyani", "waktu": "Rabu 07.30-10.00", "ruang": "309"},
    {"mk": "Pengembangan Sistem Informasi Berbasis Web", "dosen": "Zaiful Bahri", "waktu": "Rabu 09.30-12.00", "ruang": "PUSKOM"},
    {"mk": "Sistem Informasi Geografis", "dosen": "Teguh Sujana", "waktu": "Rabu 10.10-12.40", "ruang": "303"},
    {"mk": "Keamanan Sistem Informasi", "dosen": "Elfizar", "waktu": "Rabu 10.10-12.40", "ruang": "301-B"},
    {"mk": "Sistem Cerdas", "dosen": "Ibnu Daqiqil Id.", "waktu": "Rabu 13.00-15.30", "ruang": "301-A"},
    {"mk": "Keamanan Sistem Informasi", "dosen": "Elfizar", "waktu": "Rabu 13.00-15.30", "ruang": "309"},
    {"mk": "Keamanan Sistem Informasi", "dosen": "Elfizar", "waktu": "Kamis 07.30-10.00", "ruang": "303"},
    {"mk": "Rekayasa Proses Bisnis", "dosen": "Yanti Andriyani", "waktu": "Kamis 07.30-10.00", "ruang": "309"},
    {"mk": "Pemrograman Bahasa Alami", "dosen": "Tisha Melia", "waktu": "Kamis 10.10-12.40", "ruang": "309"},
    {"mk": "Sistem Cerdas", "dosen": "Ibnu Daqiqil Id.", "waktu": "Kamis 13.00-15.30", "ruang": "301-A"},
    {"mk": "Komputasi Awan", "dosen": "Al Aminuddin", "waktu": "Kamis 13.00-15.30", "ruang": "309"},
    {"mk": "Evaluasi Antarmuka Pengguna", "dosen": "Fatayat", "waktu": "Jumat 07.30-10.00", "ruang": "301-A"},
    {"mk": "Sistem Informasi Geografis", "dosen": "Teguh Sujana", "waktu": "Jumat 09.20-11.50", "ruang": "303"}
]

slot_waktu = [
    "Senin 07.30-10.00", "Senin 10.10-12.40", "Senin 13.00-15.30",
    "Selasa 13.00-15.30",
    "Rabu 07.30-10.00", "Rabu 09.30-12.00", "Rabu 10.10-12.40", "Rabu 13.00-15.30",
    "Kamis 07.30-10.00", "Kamis 10.10-12.40", "Kamis 13.00-15.30",
    "Jumat 07.30-10.00", "Jumat 09.20-11.50"
]

ruangan = ["103", "303", "309", "301-A", "301-B", "PUSKOM"]


prioritas_ruangan = {
    "PUSKOM": 5,
    "301-A": 4,
    "301-B": 3,
    "309": 2,
    "303": 2,
    "103": 1
}



dosen_mk = {
    "Rahmad Kurniawan": ["Sistem Cerdas"],
    "Ibnu Daqiqil Id.": ["Sistem Cerdas"],
    "Yanti Andriyani": ["Rekayasa Proses Bisnis"],
    "Zaiful Bahri": ["Pengembangan Sistem Informasi Berbasis Web"],
    "Al Aminuddin": ["Komputasi Awan"],
    "Tisha Melia": ["Pemrograman Bahasa Alami"],
    "Elfizar": ["Keamanan Sistem Informasi"],
    "Teguh Sujana": ["Sistem Informasi Geografis"],
    "Fatayat": ["Evaluasi Antarmuka Pengguna"]
}



def hitung_score(waktu, ruang, preferensi_jam):
    hari, jam_range = waktu.split(" ")
    start = float(jam_range.split("-")[0].replace(".", ""))
    pref = float(preferensi_jam.replace(".", ""))

    
    selisih = abs(start - pref)
    skor_jam = max(0, 10 - (selisih / 100))

    
    jumlah = sum(1 for j in jadwal_existing if j["waktu"].startswith(hari))
    penalti = jumlah * 0.8

    
    skor_ruang = prioritas_ruangan.get(ruang, 1)

    return skor_jam - penalti + skor_ruang



def cocok_slot(preferensi_jam):
    hasil = []
    pref = float(preferensi_jam.replace(".", ""))

    for s in slot_waktu:
        start = float(s.split(" ")[1].split("-")[0].replace(".", ""))
        if abs(start - pref) <= 400:
            hasil.append(s)

    return hasil if hasil else slot_waktu



from collections import defaultdict

def rekomendasi_jadwal(nama_dosen, preferensi_jam):
    rekomendasi = []
    kandidat = cocok_slot(preferensi_jam)

    for waktu in kandidat:
        for ruang in ruangan:
            bentrok = False

            for j in jadwal_existing:
                if j["waktu"] == waktu and j["ruang"] == ruang:
                    bentrok = True
                if j["waktu"] == waktu and j["dosen"] == nama_dosen:
                    bentrok = True

            if not bentrok:
                rekomendasi.append({
                    "Waktu": waktu,
                    "Ruangan": ruang,
                    "Score": hitung_score(waktu, ruang, preferensi_jam)
                })

    rekomendasi = sorted(rekomendasi, key=lambda x: x["Score"], reverse=True)


    group = defaultdict(list)
    for r in rekomendasi:
        group[r["Waktu"]].append(r)

    hasil = []
    for waktu, items in group.items():
        terbaik = sorted(items, key=lambda x: x["Score"], reverse=True)[0]
        hasil.append(terbaik)

    return sorted(hasil, key=lambda x: x["Score"], reverse=True)



daftar_dosen = list(dosen_mk.keys())

print("=== DAFTAR DOSEN ===")
for i, d in enumerate(daftar_dosen, 1):
    print(f"{i}. {d}")

pilih = int(input("\nPilih nomor dosen: "))
nama_dosen = daftar_dosen[pilih - 1]

print(f"\nDosen: {nama_dosen}")

mk_list = dosen_mk[nama_dosen]

print("\nMata kuliah:")
for i, mk in enumerate(mk_list, 1):
    print(f"{i}. {mk}")

pilih_mk = int(input("\nPilih nomor mata kuliah: "))
mk_input = mk_list[pilih_mk - 1]

preferensi_jam = input("\nMasukkan jam preferensi (contoh 09.00): ")



hasil = rekomendasi_jadwal(nama_dosen, preferensi_jam)

print("\n=== TOP 5 REKOMENDASI ===\n")
for i, r in enumerate(hasil[:5], 1):
    print(f"{i}. {r['Waktu']} | {r['Ruangan']} | Score: {round(r['Score'],2)}")

print("\n=== ALTERNATIF LAINNYA ===\n")
for i, r in enumerate(hasil[5:], 6):
    print(f"{i}. {r['Waktu']} | {r['Ruangan']} | Score: {round(r['Score'],2)}")



import pandas as pd

df = pd.DataFrame(hasil)
df.to_excel("rekomendasi_jadwal.xlsx", index=False)