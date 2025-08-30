import telebot, time, threading
from telebot import types
from config import TOKEN, OWNER_ID, CHANNEL_ADMIN, DEVELOPER
import utils

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# 🔄 Cek expired premium setiap menit
def premium_checker():
    while True:
        expired = utils.expired_premiums()
        for uid in expired:
            try:
                bot.send_message(OWNER_ID, f"⚠️ Premium user <code>{uid}</code> sudah expired!")
            except: pass
        time.sleep(60)

threading.Thread(target=premium_checker, daemon=True).start()

# Start command
@bot.message_handler(commands=['start'])
def start(msg):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📜 ALL MENU", callback_data="menu"))
    kb.add(types.InlineKeyboardButton("➕ ADD ME TO ROOM PUBLIC", url="https://t.me/"+bot.get_me().username+"?startgroup=true"))
    text = f"""
👋 Halo <b>{msg.from_user.first_name}</b>!
Bot ini khusus untuk Jasa Share / Promosi.

📌 Developer: <b>{DEVELOPER}</b>
📢 Channel: {CHANNEL_ADMIN}
"""
    bot.send_message(msg.chat.id, text, reply_markup=kb)

# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "menu":
        menu = """
<b>📜 ALL MENU</b>

/setteks (reply teks)
/jasher (reply pesan)
/jasher2 (id teks)
/addprem
/delprem
/listprem
/listgroup
"""
        bot.edit_message_text(menu, call.message.chat.id, call.message.id)

# Simpan teks
@bot.message_handler(commands=['setteks'])
def setteks(msg):
    if not msg.reply_to_message:
        return bot.reply_to(msg, "⚠️ Reply ke teks yang ingin disimpan!")
    idx = utils.add_teks(msg.reply_to_message.text)
    bot.reply_to(msg, f"✅ Teks berhasil disimpan dengan ID <b>{idx}</b>")

# Jasher dengan reply
@bot.message_handler(commands=['jasher'])
def jasher(msg):
    if not utils.is_premium(msg.from_user.id):
        return bot.reply_to(msg, "⚠️ Kamu bukan premium!")
    if not msg.reply_to_message:
        return bot.reply_to(msg, "⚠️ Reply ke pesan yang mau dishare!")

    teks = msg.reply_to_message.text
    groups = utils.list_groups()
    total = len(groups)
    bot.reply_to(msg, f"🚀 PROSES JASHER KE {total} GRUP PUBLIK, HARAP SABAR")

    for gid, gname in groups.items():
        try:
            bot.send_message(int(gid), teks)
        except: pass
    bot.send_message(msg.chat.id, "✅ JASHER SELESAI!")

# Jasher pakai ID teks
@bot.message_handler(commands=['jasher2'])
def jasher2(msg):
    if not utils.is_premium(msg.from_user.id):
        return bot.reply_to(msg, "⚠️ Kamu bukan premium!")
    args = msg.text.split()
    if len(args) < 2: return bot.reply_to(msg, "⚠️ Format: /jasher2 id_teks")
    teks = utils.get_teks(args[1])
    if not teks: return bot.reply_to(msg, "⚠️ ID teks tidak ditemukan!")

    groups = utils.list_groups()
    total = len(groups)
    bot.reply_to(msg, f"🚀 PROSES JASHER KE {total} GRUP PUBLIK, HARAP SABAR")

    for gid, gname in groups.items():
        try:
            bot.send_message(int(gid), teks)
        except: pass
    bot.send_message(msg.chat.id, "✅ JASHER SELESAI!")

# Premium control
@bot.message_handler(commands=['addprem'])
def addprem(msg):
    if msg.from_user.id != OWNER_ID: return
    args = msg.text.split()
    if len(args) < 2: return bot.reply_to(msg, "⚠️ Format: /addprem user_id")
    utils.add_premium(args[1])
    bot.reply_to(msg, f"✅ User {args[1]} ditambahkan ke premium")

@bot.message_handler(commands=['delprem'])
def delprem(msg):
    if msg.from_user.id != OWNER_ID: return
    args = msg.text.split()
    if len(args) < 2: return bot.reply_to(msg, "⚠️ Format: /delprem user_id")
    utils.del_premium(args[1])
    bot.reply_to(msg, f"✅ User {args[1]} dihapus dari premium")

@bot.message_handler(commands=['listprem'])
def listprem(msg):
    data = utils.load_json(utils.PREMIUM_FILE)
    if not data: return bot.reply_to(msg, "⚠️ Tidak ada premium")
    teks = "👑 <b>LIST PREMIUM</b>\n"
    for uid, exp in data.items():
        sisa = int(exp - time.time()) // 3600
        teks += f"- {uid} (sisa {sisa} jam)\n"
    bot.reply_to(msg, teks)

@bot.message_handler(commands=['listgroup'])
def listgroup(msg):
    groups = utils.list_groups()
    if not groups: return bot.reply_to(msg, "⚠️ Bot belum masuk grup")
    teks = "📂 <b>LIST GRUP</b>\n"
    for gid, gname in groups.items():
        teks += f"- {gname} ({gid})\n"
    bot.reply_to(msg, teks)

# Detect join grup
@bot.my_chat_member_handler()
def new_group(event):
    if event.new_chat_member.status in ["member", "administrator"]:
        if event.chat.type in ["group", "supergroup"]:
            utils.add_group(event.chat.id, event.chat.title)
            bot.send_message(OWNER_ID, f"✅ Bot ditambahkan ke grup: <b>{event.chat.title}</b> ({event.chat.id})")

print("🤖 VIANZZ-JASHER Bot sedang berjalan...")
bot.infinity_polling()
