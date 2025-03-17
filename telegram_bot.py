from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import datetime
import os

# Token bot Telegram Anda
TOKEN = "6862591374:AAHnO59rW7YPdIMgaf9H0lFueZpA2Hk76OA"

# Handler untuk perintah /start
async def start(update: Update, context: CallbackContext):
    # Membuat keyboard menu
    keyboard = [["Cek Chat ID dan Username"], ["Balas Salam"], ["GENERATE BUGS"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    # Mengirim pesan dengan menu
    await update.message.reply_text(
        "Pilih menu di bawah ini:",
        reply_markup=reply_markup
    )

# Handler untuk menu "Cek Chat ID dan Username"
async def cek_chat_id_username(update: Update, context: CallbackContext):
    user_name = update.message.from_user.first_name
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    #wktu = update.message.date
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Mengirim balasan dengan chat ID dan username
    await update.message.reply_text(
        f"Hello {user_name}\nChat ID Anda Adalah: {chat_id}\nUsername Anda adalah: @{username}\nwaktu: {current_time}"
    )

# Handler untuk menu "Balas Salam"
async def balas_salam(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    # Jika pesan adalah "assalamualaikum", balas dengan "walaikumsalam"
    if text == "assalamualaikum":
        await update.message.reply_text("walaikumsalam")

# Handler untuk menu "GENERATE BUGS
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

        allbug= ["104.17.70.206", "104.17.72.206", "104.17.71.206", "104.17.73.206", "104.17.74.206", "172.64.153.235", "172.64.155.235", "104.16.112.133", "104.16.143.237", "162.159.128.79", "104.18.43.134", "104.16.242.118", "104.18.43.123", "104.18.40.22", "172.64.151.90", "104.18.21.37", "172.64.148.245", "162.159.135.91", "172.64.155.61", "104.18.32.195", "188.114.96.3", "162.159.153.4", "172.64.155.179", "172.67.37.55", "172.64.147.209", "162.159.135.91", "104.18.40.14", "104.18.33.162", "104.18.15.182", "172.66.47.13", "104.18.24.109", "104.18.29.127", "104.18.19.109", "104.18.28.127", "104.18.18.109", "162.159.130.11", "104.16.95.80", "104.18.41.18", "104.16.20.254", "104.18.36.212", "172.64.146.238", "172.64.151.106", "172.67.5.14", "04.22.5.240", "162.159.140.159"]

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
    if text == "Cek Chat ID dan Username":
        await cek_chat_id_username(update, context)
    elif text == "Balas Salam":
        await update.message.reply_text("Kirim pesan 'assalamualaikum' untuk mendapatkan balasan.")
    elif text == "GENERATE BUGS":
        await update.message.reply_text('Kirim file .txt untuk diubah server: "" jadi bug')
    else:
        await balas_salam(update, context)

# Fungsi utama untuk menjalankan bot
def main():
    # Membuat aplikasi bot
    application = Application.builder().token(TOKEN).build()

    # Menambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Menambahkan handler untuk pesan teks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Menambahkan handler untuk file dokumen
    application.add_handler(MessageHandler(filters.Document.FileExtension("txt"), ubah_file_txt))

    # Menjalankan bot
    application.run_polling()

if __name__ == "__main__":
    main()