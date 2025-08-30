# 🤖 VIANZZ-JASHER BOT

Bot Telegram untuk jasa share / promosi otomatis ke grup-grup yang dimasuki bot.  
Support dijalankan di **Termux**, lengkap dengan sistem premium otomatis.

---

## 🚀 Fitur Utama
- `/start` → Menampilkan menu utama  
- `/setteks` → Simpan teks promosi (otomatis jadi ID teks 1,2,3,...)  
- `/jasher` → Share teks promosi dengan reply pesan  
- `/jasher2` → Share teks promosi dengan ID teks  
- `/addprem` → Tambah user premium  
- `/delprem` → Hapus user premium  
- `/listprem` → Lihat daftar user premium  
- `/listgroup` → Lihat grup yang dimasuki bot  

### 🔔 Notifikasi Otomatis
- Bot kasih info ke **OWNER** saat:  
  - User premium expired  
  - Bot ditambahkan ke grup baru  
- User baru → wajib masukin bot ke minimal 2 grup publik + join channel admin, lalu auto-premium **2 hari**.

---

## 📲 Cara Install di Termux

1. Update & install paket dasar:
   ```bash
   pkg update -y && pkg upgrade -y
   pkg install python git -y
