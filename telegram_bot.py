from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, Updater, CallbackQueryHandler, CommandHandler, MessageHandler, ConversationHandler, filters, CallbackContext, ContextTypes
#from telethon.sync import TelegramClient
#from telethon import TelegramClient
import asyncio
from telethon import TelegramClient

import datetime
import os
import requests
from bug import allbug

from cryptography.fernet import Fernet

pathkey = ""
# Baca kunci enkripsi
with open(pathkey, "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Baca token terenkripsi dari file
with open("encrypted_token.txt", "rb") as enc_file:
    encrypted_token = enc_file.read()

# Dekripsi token
decrypted_token = fernet.decrypt(encrypted_token).decode()

print(f"Decrypted Token: {decrypted_token}")

# Token bot Telegram Anda notif_dari_bot
TOKEN = decrypted_token

chat_id_pengguna = None
pesan = None
# Status conversation
BUG = 1
HPSBUG = 1
file_pathbug = "/home/gapesta/coding/python/bot tgm/dari ia/bug.py"


# Dictionary untuk menyimpan pilihan pengguna
user_choices = {}
#user_data = []

PHOTO_DIR = "/home/gapesta/Downloads/dari_bot/downloaded_photos"
OGG_DIR = "/home/gapesta/Downloads/dari_bot/downloaded_voice"
DOCU_DIR = "/home/gapesta/Downloads/dari_bot/downloaded_docu"
MP3_DIR = "/home/gapesta/Downloads/dari_bot/downloaded_mp3"
VIDEO_DIR = "/home/gapesta/Downloads/dari_bot/downloaded_video"

# Buat folder jika belum ada
if not os.path.exists(PHOTO_DIR ):
    os.makedirs(PHOTO_DIR )
if not os.path.exists(VIDEO_DIR ):
    os.makedirs(VIDEO_DIR )
# Buat folder jika belum ada
if not os.path.exists(OGG_DIR):
    os.makedirs(OGG_DIR )
if not os.path.exists(MP3_DIR ):
    os.makedirs(MP3_DIR )
if not os.path.exists(DOCU_DIR  ):
    os.makedirs(DOCU_DIR )
#os.makedirs(PHOTO_DIR, exist_ok=True)


# Handler untuk perintah /start
async def start(update: Update, context: CallbackContext):
    # Membuat keyboard menu
    keyboard = [["CEK ID USERNAME"], ["KIRIMI KAMI PESAN"], ["GENERATE BUG"], ["MENU BUG"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    # Mengirim pesan dengan menu
    await update.message.reply_text(
        "Pilih menu di bawah ini:",
        reply_markup=reply_markup
    )

# Handler untuk perintah /kirim
async def kirim(update: Update, context: CallbackContext):
    global chat_id_pengguna, pesan
    global TOKEN
    # kirim pesan
    url_root = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    
    

    # Mengambil argumen dari command
    args = context.args  # args berisi semua kata setelah /kirim
    
    if len(args) >= 1:
        chat_id_pengguna = args[0]  # Kata pertama setelah /kirim sebagai chat ID
        pesan = ' '.join(args[1:])  # Gabungkan kata kedua dan seterusnya sebagai pesan
        payloadini = {
        'chat_id': chat_id_pengguna,
        'text': pesan,
        'parse_mode': 'HTML'  # atau 'Markdown'
    }
        # Validasi: pastikan chat ID adalah 10 digit angka
        if chat_id_pengguna.isdigit() and len(chat_id_pengguna) == 10:
            sent_message_id = await update.message.reply_text(f'💾 Chat ID Anda telah disimpan sementara: {chat_id_pengguna}')
            if pesan:
                response = requests.post(url_root, json=payloadini)
                # Memeriksa status dan konten respons
                if response.status_code == 200:
                    print('Pesan terkirim!')
                    sent_message = await update.message.reply_text(f'✅️Pesan Anda berhasil terkirim')
                    await asyncio.sleep(5)
                    try:
                        await sent_message.delete()
                        print(f"✅️ Berhasil menghapus pesan")
                    except Exception as e:
                        print(f"❌ Gagal menghapus pesan: {e}")
                    # Mengambil data JSON dari respons
                    response_data = response.json()
                    print('Data Respons:', response_data)
                    
                else:
                    print('Gagal mengirim pesan. Status code:', response.status_code)
                    print('Detail Respons:', response.text)
                    sent_message = await update.message.reply_text(f'❌Pesan Anda Gagal terkirim')
                    # Tunggu 5 detik
                    await asyncio.sleep(5)
                    # Hapus pesan bot
                    try:
                        await sent_message.delete()
                        print(f"✅️ Berhasil menghapus pesan")
                    except Exception as e:
                        print(f"❌ Gagal menghapus pesan: {e}")
            else:
                await update.message.reply_text('❌ Tidak ada pesan yang diberikan untuk dikirim.')
            await asyncio.sleep(2)
            # Hapus pesan bot
            try:
                await sent_message_id.delete()
                print(f"✅️ Berhasil menghapus pesan")
            except Exception as e:
                print(f"❌ Gagal menghapus pesan: {e}")
        else:
            await update.message.reply_text('Chat ID tidak valid. Pastikan Anda memasukkan 10 digit angka.')
    else:
        await update.message.reply_text('Silakan masukkan chat ID dan pesan setelah /kirim.')

# Fungsi untuk menangani perintah /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Berikut adalah daftar perintah yang tersedia:\n"
        "/start - untuk memulai bot.\n"
        "/kirim chat_id - untuk kirim pesan keUser lain.\n°Cth gunakan format: /kirim chat_id pesannya\n"
        "/id @username - untuk cek ID User.\n°Cth gunakan format: /id @notif_dari_bot\n"
        "/help - Menampilkan daftar perintah yang tersedia.\n"
    )
    await update.message.reply_text(help_text)

# Handler untuk menu "CEK ID USERNAME"
async def cek_chat_id_username(update: Update, context: CallbackContext):
    user_name = update.message.from_user.first_name if update.message.from_user.first_name else "-"
    last_name = update.message.from_user.last_name if update.message.from_user.last_name else "-"
    full_name = update.message.from_user.full_name if update.message.from_user.full_name else "-"
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    #wktu = update.message.date
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Mengirim balasan dengan chat ID dan username
    update.message.reply_text(
        f"Hello {user_name}\nchat id: {chat_id}\nfirst name: {user_name}\nlast name: {last_name}\nfull name: {full_name}\nUsername: @{username}\nwaktu: {current_time}"
    )

# Handler untuk menu "KIRIMI KAMI PESAN"
async def kirim_pesan_kedeveloper(update: Update, context: CallbackContext):
    
    chat_id = 5867172791
    TOKEN = "8162337811:AAH1XJumlhBsyjZ3VhV5jUI4gF4t18x8xCg"
    user_name_penggirim = update.message.from_user.first_name
    chat_id_penggirim = update.message.chat_id
    username_penggirim = update.message.from_user.username
    text = update.message.text.lower()
    current_time_penggirim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tampikan_id = f"========================\n👤 Nama      : {user_name_penggirim}\n🆔 User ID   : {chat_id_penggirim}\n🌐 UserName: @{username_penggirim}\nwaktu: 📅 {current_time_penggirim}\n========================\n"
    text = tampikan_id + text
    
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'  # atau 'Markdown'
    }
    
    response = requests.post(url, json=payload)
    #return response.json()

    if response.status_code  == 200:
        """Balas pesan pengguna dan hapus setelah 5 detik"""
        sent_message = await update.message.reply_text("✅️ Pesan berhasil terkirim.")

        # Tunggu 5 detik
        await asyncio.sleep(5)

        # Hapus pesan bot
        try:
            await sent_message.delete()
            print(f"✅️ Berhasil menghapus pesan")
        except Exception as e:
            print(f"❌ Gagal menghapus pesan: {e}")
    else:
        print(f"Error: {response.status_code}, Response: {response.text}")
        """Balas pesan pengguna dan hapus setelah 5 detik"""
        sent_message = await update.message.reply_text(f"❌ {response.status_code} Gagal menggirim pesan.")

        # Tunggu 5 detik
        await asyncio.sleep(5)

        # Hapus pesan bot
        try:
            await sent_message.delete()
            print(f"✅️ Berhasil menghapus pesan")
        except Exception as e:
            print(f"❌ Gagal menghapus pesan: {e}")
            
    #return response.json()
    # Jika pesan adalah "assalamualaikum", balas dengan "walaikumsalam"
    #if text != "":
    #    await update.message.reply_text("pesan berhasil terkirim")

# Fungsi untuk menangani perintah /id @username
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text("Silakan gunakan format: /id @username")
        return
    
    username = context.args[0]
    #API_ID = 9308092  # Ganti dengan API ID Anda
    #API_HASH = "9e1a1d2148e94eaa640851bc4046903b"  # Ganti dengan API Hash Anda
    # Ganti dengan api_id dan api_hash Anda
    api_id = '9308092'
    api_hash = '9e1a1d2148e94eaa640851bc4046903b'

    # Ganti dengan nomor telepon Anda
    phone_number = '+60137009088'
    
    # Inisialisasi client
    client = TelegramClient('session_login', api_id, api_hash)
    # Menjalankan client
    await client.start(phone_number)

    try:
        # Mendapatkan pengguna berdasarkan username
        user = await client.get_entity(username)
        print(f'Chat ID untuk {username} adalah: {user.id}')
        user_info = (
                "========================\n"
                f"🆔 Chat ID: {user.id}\n"
                f"👤 First Name: {user.first_name}\n"
                f"👤 Last Name: {user.last_name if user.last_name else 'Tidak ada'}\n"
                f"👤 Username: @{user.username if user.username else 'Tidak ada'}\n"
                "========================"
            )
        await update.message.reply_text(user_info)
    except Exception as e:
        print(f"Username : {e} tidak ditemukan.")
        await update.message.reply_text(f"Tidak dapat menemukan pengguna dengan username {username}. Pastikan username valid.")
    
#    try:
        # Mendapatkan user dari username
        #user = await context.bot.get_user_profile_photos(username)
        #with TelegramClient('anon', API_ID, API_HASH) as client:
#            user = client.get_entity(username)
#            print(f"User ID: {user.id}")

#            user_info = (
#                f"**Chat ID:** {user.id}\n"
#                f"**First Name:** {user.first_name}\n"
#                f"**Last Name:** {user.last_name if user.last_name else 'Tidak ada'}\n"
#                f"**Username:** {user.username if user.username else 'Tidak ada'}"
#            )
        
#        await update.message.reply_text(user_info)

#    except Exception as e:
#        await update.message.reply_text(f"Tidak dapat menemukan pengguna dengan username {username}. Pastikan username valid.")
# Handler menu bug"
async def menu_bug(update: Update, context: CallbackContext):
        # Membuat tombol inline
    keyboard = [
        [InlineKeyboardButton("ADD BUG", callback_data='add_bug')],
        [InlineKeyboardButton("LIST BUG", callback_data='list_bug')],
        [InlineKeyboardButton("HAPUS BUG", callback_data='hapus_bug')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Silakan pilih menu:", reply_markup=reply_markup)

# Fungsi saat user klik "Menu 1"
async def add_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    #meminta input bug
    await query.message.reply_text("Silakan masukan host bug atau ip bug\njika ingin membatalkan klik /cancel_add_bug")
    #global BUG
    return BUG

# Fungsi menangkap input nomor HP
async def handle_add_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    BUG = update.message.text
    user_id = update.message.from_user.id

    # Simpan ke file
    #file_path = "/root/bug.py"
    global file_pathbug
    # Baca isi file
    with open(file_pathbug, "r") as file:
        content = file.read()

    # Ganti teks
    content = content.replace("]", f', "{BUG}"]')

    # Tulis ulang ke file
    with open(file_pathbug, "w") as file:
        file.write(content)

    #print("Teks berhasil diganti!")

    sks = await update.message.reply_text(f"BUG {BUG} berhasil disimpan di{file_pathbug}!\nKetik /start untuk kembali ke menu.")
    
    # Tunggu 5 detik
    await asyncio.sleep(5)

        # Hapus pesan bot
    await sks.delete()

    return ConversationHandler.END  # Mengakhiri conversation
    


# Fungsi membatalkan input
async def cancel_add_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Input dibatalkan. Ketik /start untuk kembali ke menu.")
    return ConversationHandler.END


# Fungsi membatalkan input
async def cancel_hps_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Input dibatalkan. Ketik /start untuk kembali ke menu.")
    return ConversationHandler.END
    
 #Fungsi untuk menangani tombol yang diklik
async def button_callback(update: Update, context: CallbackContext):
    """Menangani klik tombol inline keyboard."""
    query = update.callback_query
    await query.answer()# Menandakan bahwa callback telah diterima
    
    # Mengetahui tombol mana yang diklik
    if query.data == 'list_bug':
        await lst_bug(update, context)
    #elif query.data == 'hapus_bug':
    #    await query.message.reply_text("Silakan Masukkan ip/host yang mau dihapus")
    #    global user_data
    #    context.user_data["awaiting_name"] = True
    #    await hps_bug(update, context)


async def hps_bug(update: Update, context: CallbackContext) -> None:
    """Meminta user untuk memasukkan ID member yang akan dihapus."""
    query = update.callback_query
    await query.answer()
    #await update.callback_query.message.reply_text("Silakan Masukkan ip/host yang mau dihapus")
    await query.message.reply_text("Silakan Masukkan ip/host yang mau dihapus.")
    return HPSBUG
async def handle_hps_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HPSBUG = update.message.text

    #print(HPSBUG)
    #context.user_data["awaiting_name"] = False
    #print("===========")
    global file_pathbug
    hapus = [update.message.text]

    i = 0
    while i < len(allbug):
        j = 0
        while j < len(hapus):
            if allbug[i] == hapus[j]:
                del allbug[i]  # Menghapus elemen langsung dari list data
                i -= 1  # Mundur satu langkah karena list berubah
                try:
                    with open(file_pathbug, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    # Hapus kata yang sesuai
                    updated_content = content.replace(f', "{HPSBUG}"', '')
                    print(updated_content)
                    with open(file_pathbug, 'w', encoding='utf-8') as file:
                        file.write(updated_content)
                    
                    print(f'Kata "{HPSBUG}" berhasil dihapus dari {file_pathbug}')
                except FileNotFoundError:
                    print(f'File "{file_pathbug}" tidak ditemukan.')
                except Exception as e:
                    print(f'Terjadi kesalahan: {e}')
                
                break
            j += 1
        i += 1

    #print(allbug)

    await update.message.reply_text(f"bug {HPSBUG} berhasil dihapus!\nKetik /start untuk kembali ke menu.")
    
    # Tunggu 5 detik
    #await asyncio.sleep(3)

        # Hapus pesan bot
    #await sks.delete()

    return ConversationHandler.END  # Mengakhiri conversation
    

# Fungsi saat user klik "listbug"
async def lst_bug(update: Update, context: CallbackContext):
#    global file_pathbug
#    try:
#        with open(file_pathbug, "r", encoding="utf-8") as file:
#            content = file.read()
#        
#        if len(content) > 4000:  # Telegram memiliki batasan 4096 karakter per pesan
#            await update.callback_query.message.reply_text("File terlalu besar, akan dikirim sebagai dokumen.")
#            await update.callback_query.message.reply_document(document=open(file_pathbug, "rb"))
#        else:
            #await update.message.reply_text(f"📄 Isi file:\n\n{content}")
#            await update.callback_query.message.reply_text(f"📄 Isi file:\n\n{content}")

#    except Exception as e:
#        if update.message: #untuk commend
#            await update.message.reply_text(f"Terjadi kesalahan: {e}")
#        elif update.callback_query:  #untuk callback
#            await update.callback_query.message.reply_text(f"Terjadi kesalahan: {e}")
#        else:
#            await update.effective_message.reply_text(f"Terjadi kesalahan: {e}") #callback dan commend

    """Fungsi untuk menampilkan daftar member."""
    chat_id = update.effective_chat.id
    #print(f"DEBUG: daftar_members -> {allbug} (type: {type(allbug)})")

    daftar = "\n".join([f"{i+1}. {member}" for i, member in enumerate(allbug)])
    jumlah_bug = len(allbug)
    await context.bot.send_message(chat_id=chat_id, text=f"Daftar Member:\n{daftar}")
    await update.callback_query.message.reply_text(f"jumlah bug {jumlah_bug}")


async def ubah_file_txt(update: Update, context: CallbackContext):
    # Memeriksa apakah user mengirim file
    if update.message.document:
        file = await update.message.document.get_file()
        file_path = f"temp_{update.message.document.file_name}"
        
        # Mengunduh file
        await file.download_to_drive(file_path)

        # Membaca dan mengubah isi file
        with open(file_path, "r") as f:
            content = f.read()
        
         #   content = file_bytes.read().decode('utf-8')
    
    # Create a list to store modified contents for each duplication
        modified_contents = []

        #allbug= ["104.17.70.206", "104.17.72.206", "104.17.71.206", "104.17.73.206", "104.17.74.206", "172.64.153.235", "172.64.155.235", "104.16.112.133", "104.16.143.237", "162.159.128.79", "104.18.43.134", "104.16.242.118", "104.18.43.123", "104.18.40.22", "172.64.151.90", "104.18.21.37", "172.64.148.245", "162.159.135.91", "172.64.155.61", "104.18.32.195", "188.114.96.3", "162.159.153.4", "172.64.155.179", "172.67.37.55", "172.64.147.209", "162.159.135.91", "104.18.40.14", "104.18.33.162", "104.18.15.182", "172.66.47.13", "104.18.24.109", "104.18.29.127", "104.18.19.109", "104.18.28.127", "104.18.18.109", "162.159.130.11", "104.16.95.80", "104.18.41.18", "104.16.20.254", "104.18.36.212", "172.64.146.238", "172.64.151.106", "172.67.5.14", "04.22.5.240", "162.159.140.159"]

        for i in allbug :  # Loop dari 1 sampai 10
            modified_content = content.replace('server: ""', f"server: {i}")  # Ganti "server" dengan "192.168.88.X"
            modified_contents.append(modified_content)  # Tambahkan hasil ke dalam list
        
        
         # Gabungkan semua duplicated content
        new_content = "".join(modified_contents)  # Pisahkan setiap isi dengan dua baris baru
        addtextproxy = "proxies:\n"
        new_content = addtextproxy + new_content
        # Mengubah isi file (contoh: menambahkan "danibot" dan alamat)
        #new_content = content.replace("server:", "server: danibot")

        #new_content += "\nalamat : Jl. Sukarta\nkota : Depok"

        # Menyimpan file yang sudah diubah
        new_file_path = f"modified_{update.message.document.file_name}"
        with open(new_file_path, "w") as f:
            f.write(new_content)

        # Mengirim file yang sudah diubah ke user
        await update.message.reply_document(document=open(new_file_path, "rb"))

        # Menghapus file sementara
        os.remove(file_path)
        os.remove(new_file_path)
    else:
        await update.message.reply_text('Silakan kirim file .txt untuk diubah. text yang diubah server: ""')

# Handler untuk memproses pesan teks

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    # Memproses pesan berdasarkan menu yang dipilih
    if text == "CEK ID USERNAME":
        await cek_chat_id_username(update, context)
    elif text == "KIRIMI KAMI PESAN":
        await update.message.reply_text("Silakan Masukan pesan yang ingan anda sampaikan ke Developer")
    elif text == "GENERATE BUG":
        await update.message.reply_text('Kirim file .txt untuk diubah server: "" jadi bug')
    elif text == "MENU BUG":
        await menu_bug(update, context)
    else:
        await kirim_pesan_kedeveloper(update, context)

# Fungsi utama untuk menjalankan bot
async def handle_media(update: Update, context: CallbackContext):
    """Tangkap semua media (foto, video, dokumen, dll.) dan simpan ke direktori downloads."""
    message = update.message

    if message.photo:  # Jika pengguna mengirim foto
        file = message.photo[-1].file_id
        file_ext = ".jpg"
            # Unduh file
        file_obj = await context.bot.get_file(file)
        getfile = await message.photo[-1].get_file()
        file_path = os.path.join(PHOTO_DIR, f"{file}{file_ext}")
        await file_obj.download_to_drive(file_path)
        await message.reply_text(f"File berhasil disimpan: {file_path}")
        chat_id = 5867172791
        global TOKEN 
        user_name_penggirim = message.from_user.first_name if message.from_user.first_name else "-"
        last_name_penggirim = message.from_user.last_name if message.from_user.last_name else "-"
        chat_id_penggirim = message.chat_id
        username_penggirim = message.from_user.username
        current_time_penggirim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tampikan_id = f"========================\n {user_name_penggirim} : menggirim 📷 Gambar\n👤 first name :{user_name_penggirim}\n👤 last name :{last_name_penggirim}\n🆔 User ID   : {chat_id_penggirim}\n🌐 UserName: @{username_penggirim}\nwaktu: 📅 {current_time_penggirim}\n========================\n"
        caption = message.caption if message.caption else f"📷 Gambar diterima dari @{username_penggirim }"
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': tampikan_id,
            'parse_mode': 'HTML'  # atau 'Markdown'
        }
        
        response = requests.post(url, json=payload)
        await context.bot.send_photo(chat_id, getfile.file_id, caption=caption)
        return response.json()

    elif message.video:  # Jika pengguna mengirim video
        file = message.video.file_id
        file_ext = ".mp4"
            # Unduh file
        file_obj = await context.bot.get_file(file)
        file_path = os.path.join(VIDEO_DIR, f"{file}{file_ext}")
        await file_obj.download_to_drive(file_path)
        await message.reply_text(f"File berhasil disimpan: {file_path}")
        getfile = await message.video.get_file()
        chat_id = 5867172791
        global TOKEN 
        user_name_penggirim = message.from_user.first_name
        last_name_penggirim = message.from_user.last_name
        chat_id_penggirim = message.chat_id
        username_penggirim = message.from_user.username
        current_time_penggirim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tampikan_id = f"========================\n {user_name_penggirim} : menggirim 🎬 video\n👤 first name :{user_name_penggirim}\n👤 last name :{last_name_penggirim}\n 🆔 User ID   : {chat_id_penggirim}\n🌐 UserName: @{username_penggirim}\nwaktu: {current_time_penggirim}\n========================\n"
        caption = message.caption if message.caption else f"🎬 video diterima dari @{username_penggirim}"
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': tampikan_id,
            'parse_mode': 'HTML'  # atau 'Markdown'
        }
        
        response = requests.post(url, json=payload)
        await context.bot.send_video(chat_id, getfile.file_id, caption=caption)
        return response.json()

    elif message.document:  # Jika pengguna mengirim dokumen
        file = message.document.file_id
        file_ext = message.document.file_name.split(".")[-1]
            # Unduh file
        file_obj = await context.bot.get_file(file)
        file_path = os.path.join(DOCU_DIR, f"{file}.{file_ext}")
        await file_obj.download_to_drive(file_path)
        await message.reply_text(f"File berhasil disimpan: {file_path}")
        getfile = await message.document.get_file()
        chat_id = 5867172791
        global TOKEN 
        user_name_penggirim = message.from_user.first_name
        last_name_penggirim = message.from_user.last_name
        chat_id_penggirim = message.chat_id
        username_penggirim = message.from_user.username
        current_time_penggirim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tampikan_id = f"========================\n {user_name_penggirim} : menggirim 🗂️ document\n👤 first name :{user_name_penggirim}\n👤 last name :{last_name_penggirim}\n 🆔 User ID   : {chat_id_penggirim}\n🌐 UserName: @{username_penggirim}\nwaktu: {current_time_penggirim}\n========================\n"
        caption = message.caption if message.caption else f"🗂️ document diterima dari @{username_penggirim}"
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': tampikan_id,
            'parse_mode': 'HTML'  # atau 'Markdown'
        }
        
        response = requests.post(url, json=payload)
        await context.bot.send_document(chat_id, getfile.file_id, caption=caption)
        return response.json()
    elif message.audio:  # Jika pengguna mengirim audio
        file = message.audio.file_id
        file_ext = ".mp3"
            # Unduh file
        file_obj = await context.bot.get_file(file)
        file_path = os.path.join(MP3_DIR, f"{file}{file_ext}")
        await file_obj.download_to_drive(file_path)
        await message.reply_text(f"File berhasil disimpan: {file_path}")
        getfile = await message.audio.get_file()
        chat_id = 5867172791
        global TOKEN
        user_name_penggirim = message.from_user.first_name
        last_name_penggirim = message.from_user.last_name
        chat_id_penggirim = message.chat_id
        username_penggirim = message.from_user.username
        current_time_penggirim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tampikan_id = f"========================\n {user_name_penggirim} : menggirim ▶️ audio\n👤 first name :{user_name_penggirim}\n👤 last name :{last_name_penggirim}\n 🆔 User ID   : {chat_id_penggirim}\n🌐 UserName: @{username_penggirim}\nwaktu: {current_time_penggirim}\n========================\n"
        caption = message.caption if message.caption else f"▶️ audio diterima dari @{username_penggirim}"
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': tampikan_id,
            'parse_mode': 'HTML'  # atau 'Markdown'
        }
        
        response = requests.post(url, json=payload)
        await context.bot.send_audio(chat_id, getfile.file_id, caption=caption)
        return response.json()
    elif message.voice:  # Jika pengguna mengirim voice note
        file = message.voice.file_id
        file_ext = ".ogg"
            # Unduh file
        file_obj = await context.bot.get_file(file)
        file_path = os.path.join(OGG_DIR, f"{file}{file_ext}")
        await file_obj.download_to_drive(file_path)
        await message.reply_text(f"File berhasil disimpan: {file_path}")
        getfile = await message.voice.get_file()
        chat_id = 5867172791
        global TOKEN
        user_name_penggirim = message.from_user.first_name
        last_name_penggirim = message.from_user.last_name
        chat_id_penggirim = message.chat_id
        username_penggirim = message.from_user.username
        current_time_penggirim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tampikan_id = f"========================\n {user_name_penggirim} : menggirim 🎤 voice\n👤 first name :{user_name_penggirim}\n👤 last name :{last_name_penggirim}\n 🆔 User ID   : {chat_id_penggirim}\n🌐 UserName: @{username_penggirim}\nwaktu: {current_time_penggirim}\n========================\n"
        caption = message.caption if message.caption else f"🎤 voice diterima dari @{username_penggirim}"
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': tampikan_id,
            'parse_mode': 'HTML'  # atau 'Markdown'
        }
        
        response = requests.post(url, json=payload)
        await context.bot.send_voice(chat_id, getfile.file_id, caption=caption)
        return response.json()
    else:
        await message.reply_text("Format file tidak dikenali.\nFormat yang dikenali mp3,mp4,.jpg,ogg/voice,document")
        return

def main():
    # Membuat aplikasi bot
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_bug, pattern="^add_bug$")],
        states={BUG: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_add_bug)]},
        fallbacks=[CommandHandler("cancel_add_bug", cancel_add_bug)]
    )

    application.add_handler(conv_handler)

    handler_hps = ConversationHandler(
        entry_points=[CallbackQueryHandler(hps_bug, pattern="^hapus_bug$")],
        states={BUG: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hps_bug)]},
        fallbacks=[CommandHandler("cancel_hps_bug", cancel_hps_bug)]
    )


    application.add_handler(handler_hps)

    # Menambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Menambahkan handler untuk perintah /kirim chat_id
    application.add_handler(CommandHandler("kirim", kirim))
    
    #Menambahkan Handler untuk perintah /help
    application.add_handler(CommandHandler('help', help_command))
 
    #Menambahkan Handler untuk perintah /id @username
    application.add_handler(CommandHandler('id', id_command))

    #application.add_handler(CallbackQueryHandler(hps_bug, pattern="^hapus_bug$"))

    #menu bug
    application.add_handler(CallbackQueryHandler(button_callback))

    #application.add_handler(MessageHandler(None, konfirmasi_hapus))
    #@bot.on(events.NewMessage(incoming=True))
    #application.add_handler(MessageHandler(filters.PHOTO, handle_Photo))

    # Menambahkan handler untuk pesan teks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Handler untuk semua jenis file dan media
    application.add_handler(MessageHandler(filters.ALL & ~filters.TEXT, handle_media))

    # Menambahkan handler untuk file dokumen
    application.add_handler(MessageHandler(filters.Document.FileExtension("txt"), ubah_file_txt))

    # Menjalankan bot
    print("✅ Bot berjalan... Tekan CTRL+C untuk berhenti.")
    application.run_polling()

if __name__ == "__main__":
    main()
