import json, os, time

DATA_DIR = "data"
TEKS_FILE = os.path.join(DATA_DIR, "teks.json")
PREMIUM_FILE = os.path.join(DATA_DIR, "premium.json")
GROUP_FILE = os.path.join(DATA_DIR, "groups.json")

os.makedirs(DATA_DIR, exist_ok=True)

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def add_teks(teks):
    data = load_json(TEKS_FILE)
    idx = str(len(data) + 1)
    data[idx] = teks
    save_json(TEKS_FILE, data)
    return idx

def get_teks(idx):
    data = load_json(TEKS_FILE)
    return data.get(str(idx))

def list_teks():
    return load_json(TEKS_FILE)

def add_premium(user_id, durasi=2*24*3600):
    data = load_json(PREMIUM_FILE)
    data[str(user_id)] = int(time.time()) + durasi
    save_json(PREMIUM_FILE, data)

def del_premium(user_id):
    data = load_json(PREMIUM_FILE)
    if str(user_id) in data:
        del data[str(user_id)]
        save_json(PREMIUM_FILE, data)

def is_premium(user_id):
    data = load_json(PREMIUM_FILE)
    exp = data.get(str(user_id))
    if exp and exp > time.time():
        return True
    return False

def expired_premiums():
    data = load_json(PREMIUM_FILE)
    now = time.time()
    expired = [uid for uid, exp in data.items() if exp <= now]
    for uid in expired:
        del data[uid]
    save_json(PREMIUM_FILE, data)
    return expired

def add_group(group_id, group_name):
    data = load_json(GROUP_FILE)
    data[str(group_id)] = group_name
    save_json(GROUP_FILE, data)

def list_groups():
    return load_json(GROUP_FILE)
