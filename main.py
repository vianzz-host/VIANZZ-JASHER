from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, json, time, asyncio
from config import TOKEN, OWNER_ID, CHANNEL_ADMIN

# ========== Helper JSON ==========
def load_json(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# File data
TEKS_FILE = "data/teks.json"
PREM_FILE = "data/premium.json"
GROUP_FILE = "data/groups.json"

# Bot client
app = Client("jasher", bot_token=TOKEN)

# ========== START MENU ==========
@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("📢 JASHER", callback_data="jasher"),
         InlineKeyboardButton("📝 SET TEKS", callback_data="setteks")],
        [InlineKeyboardButton("📋 LIST TEKS", callback_data="listteks")],
        [InlineKeyboardButton("👑 PREMIUM MENU", callback_data="premmenu")],
        [InlineKeyboardButton("📊 LIST GROUP", callback_data="listgroup")],
        [InlineKeyboardButton("ℹ️ INFO", callback_data="info")]
    ]
    
    if os.path.exists("menu.jpg"):
        await message.reply_photo(
            "menu.jpg",
            caption="👋 Selamat datang di **VIANZZ-JASHER BOT**\n\nGunakan tombol di bawah untuk navigasi:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_text(
            "👋 Selamat datang di **VIANZZ-JASHER BOT**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# ========== SET TEKS ==========
@app.on_message(filters.command("setteks") & filters.reply)
async def set_teks(client, message):
    teks_data = load_json(TEKS_FILE)
    new_id = str(len(teks_data) + 1)
    teks_data[new_id] = message.reply_to_message.text
    save_json(TEKS_FILE, teks_data)
    await message.reply_text(f"✅ Teks disimpan dengan ID {new_id}")

# ========== LIST TEKS ==========
@app.on_message(filters.command("listteks"))
async def list_teks(client, message):
    teks_data = load_json(TEKS_FILE)
    if not teks_data:
        await message.reply_text("⚠️ Belum ada teks yang disimpan.")
        return
    msg = "📋 **List Teks Tersimpan:**\n\n"
    for tid, teks in teks_data.items():
        preview = teks if len(teks) <= 50 else teks[:50] + "..."
        msg += f"**ID {tid}:** {preview}\n"
    await message.reply_text(msg)

# ========== CEK PREMIUM ==========
async def check_premium(user_id):
    prem_data = load_json(PREM_FILE)
    if str(user_id) in prem_data:
        if time.time() > prem_data[str(user_id)]["expire"]:
            del prem_data[str(user_id)]
            save_json(PREM_FILE, prem_data)
            # notif ke owner
            await app.send_message(OWNER_ID, f"⏰ Premium user {user_id} sudah expired.")
            return False
        return True
    return False

# ========== DETEKSI BOT MASUK GRUP ==========
@app.on_chat_member_updated()
async def on_group_added(client, event):
    if event.new_chat_member and event.new_chat_member.user.id == (await app.get_me()).id:
        groups = load_json(GROUP_FILE)
        groups[str(event.chat.id)] = event.chat.title
        save_json(GROUP_FILE, groups)
        await app.send_message(OWNER_ID, f"✅ Bot ditambahkan ke grup: {event.chat.title}")

# ========== AUTO PREMIUM ==========
async def auto_premium(user_id):
    groups = await app.get_common_chats(user_id)
    if len(groups) >= 2:
        try:
            member = await app.get_chat_member(CHANNEL_ADMIN, user_id)
            if member.status in ["member", "administrator", "creator"]:
                prem_data = load_json(PREM_FILE)
                prem_data[str(user_id)] = {"expire": time.time() + 2*24*60*60}
                save_json(PREM_FILE, prem_data)
                await app.send_message(user_id, "🎉 Kamu otomatis jadi PREMIUM selama 2 hari!")
                await app.send_message(OWNER_ID, f"👑 User {user_id} auto-premium 2 hari.")
        except:
            pass

# ========== LIST GROUP ==========
@app.on_message(filters.command("listgroup"))
async def list_group(client, message):
    groups = load_json(GROUP_FILE)
    if not groups:
        await message.reply_text("⚠️ Bot belum masuk grup manapun.")
        return
    msg = "📊 **Daftar Grup yang dimasuki bot:**\n\n"
    for gid, gname in groups.items():
        msg += f"- {gname} (`{gid}`)\n"
    await message.reply_text(msg)

# ========== BACKGROUND TASK CEK PREMIUM ==========
async def premium_checker():
    while True:
        prem_data = load_json(PREM_FILE)
        changed = False
        for uid, info in list(prem_data.items()):
            if time.time() > info["expire"]:
                del prem_data[uid]
                changed = True
                await app.send_message(OWNER_ID, f"⏰ Premium user {uid} sudah expired.")
        if changed:
            save_json(PREM_FILE, prem_data)
        await asyncio.sleep(3600)  # cek tiap 1 jam

# ========== RUN ==========
async def main():
    await app.start()
    asyncio.create_task(premium_checker())
    print("✅ VIANZZ-JASHER BOT berjalan...")
    await idle()

if __name__ == "__main__":
    from pyrogram import idle
    asyncio.run(main())
