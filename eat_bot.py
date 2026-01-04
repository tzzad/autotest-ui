cat << '_EOF_' > eat_bot.py
# -*- coding: utf-8 -*-
import logging, asyncio, sqlite3, random, string
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# --- CONFIG ---


# Используем английские ключи для стабильности
C_MAP = {"Завтрак": "breakfast", "Гарнир": "side", "Мясо": "meat", "Ужин": "dinner"}
R_MAP = {v: k for k, v in C_MAP.items()}

class AddDish(StatesGroup): name = State(); cat = State(); sweet = State(); ingr = State()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN); dp = Dispatcher(storage=MemoryStorage())

# --- DB ---
def get_db():
    conn = sqlite3.connect(DB_NAME); conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS families (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, token TEXT UNIQUE, head_id INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, family_id INTEGER)")
        c.execute("CREATE TABLE IF NOT EXISTS dishes (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, is_sweet INTEGER, owner_id INTEGER, owner_type TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS dish_ingredients (id INTEGER PRIMARY KEY AUTOINCREMENT, dish_id INTEGER, ingredient_name TEXT, amount REAL, unit TEXT, FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE)")
        conn.commit()

def get_ctx(uid):
    with get_db() as conn:
        u = conn.execute("SELECT * FROM users WHERE user_id = ?", (uid,)).fetchone()
        if u and u['family_id']: return u['family_id'], 'family'
        return uid, 'user'

def get_dish_count(oid, otyp):
    with get_db() as conn:
        res = conn.execute("SELECT COUNT(*) FROM dishes WHERE owner_id = ? AND owner_type = ?", (oid, otyp)).fetchone()
        return res[0]

# --- KEYBOARDS ---

def cancel_kb():
    return types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="❌ Отмена")]], resize_keyboard=True)

# --- GLOBAL HANDLERS ---
@dp.message(Command("cancel"))
@dp.message(F.text == "❌ Отмена")
async def global_cancel(m: types.Message, state: FSMContext):
    await state.clear()
    oid, otyp = get_ctx(m.from_user.id)
    await m.answer("Действие отменено.", reply_markup=main_kb(get_dish_count(oid, otyp)))

@dp.message(CommandStart())
async def start_cmd(m: types.Message, state: FSMContext):
    with get_db() as conn: conn.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (m.from_user.id, m.from_user.full_name))
    args = m.text.split()
    if len(args) > 1:
        await state.update_data(temp_token=args[1])
        return await start_join_proc(m, state, args[1])
    oid, otyp = get_ctx(m.from_user.id)
    await m.answer(f"Привет! Я бот @{BOT_USERNAME}.", reply_markup=main_kb(get_dish_count(oid, otyp)))

# --- JOIN FAMILY ---
@dp.message(FamilyState.confirming_join, F.text == "✅ Удалить мои блюда и вступить")
async def join_confirm(m: types.Message, state: FSMContext):
    dt = await state.get_data(); tk = dt.get('temp_token'); target_fam = None
    with get_db() as conn:
        target_fam = conn.execute("SELECT * FROM families WHERE token = ?", (tk,)).fetchone()
        if target_fam:
            conn.execute("DELETE FROM dishes WHERE owner_id = ? AND owner_type = 'user'", (m.from_user.id,))
            conn.commit()
    if target_fam: await do_join(m, state, target_fam['id'], target_fam['name'])


async def do_join(m, state, fid, fname):
    with get_db() as conn:
        conn.execute("UPDATE users SET family_id = ? WHERE user_id = ?", (fid, m.from_user.id))
        conn.commit()
    count = get_dish_count(fid, 'family')
    await m.answer(f"🏠 Добро пожаловать в семью {fname}!", reply_markup=main_kb(count))
    await state.clear()

# --- FAMILY ---
@dp.message(F.text == "🏠 Семья")
async def fam_menu(m: types.Message):
    with get_db() as conn:
        u = conn.execute("SELECT * FROM users WHERE user_id = ?", (m.from_user.id,)).fetchone()
        if not u or not u['family_id']:
            kb = [[types.KeyboardButton(text="👨‍👩‍👧 Создать семью"), types.KeyboardButton(text="🔑 Вступить в семью")], [types.KeyboardButton(text="⬅️ В главное меню")]]
            return await m.answer("Вы в одиночном режиме.", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
        f = conn.execute("SELECT * FROM families WHERE id = ?", (u['family_id'],)).fetchone()
        kb = [[types.KeyboardButton(text="👥 Члены семьи")]]
        if f['head_id'] == m.from_user.id:
            kb.append([types.KeyboardButton(text="✉️ Пригласить в семью"), types.KeyboardButton(text="⚙️ Управление семьей")])
            kb.append([types.KeyboardButton(text="🗑 Удалить семью")])
        else: kb.append([types.KeyboardButton(text="🚪 Уйти из семьи")])
        kb.append([types.KeyboardButton(text="⬅️ В главное меню")])
        await m.answer(f"🏠 Семья: <b>{f['name']}</b>", parse_mode="HTML", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text == "👨‍👩‍👧 Создать семью")
async def fam_c1(m: types.Message, state: FSMContext):
    await m.answer("Введите название семьи:", reply_markup=cancel_kb()); await state.set_state(FamilyState.creating)


@dp.message(F.text == "👥 Члены семьи")
async def fam_members(m: types.Message):
    with get_db() as conn:
        u = conn.execute("SELECT family_id FROM users WHERE user_id = ?", (m.from_user.id,)).fetchone()
        if not u or not u['family_id']: return
        f = conn.execute("SELECT name FROM families WHERE id = ?", (u['family_id'],)).fetchone()
        mems = conn.execute("SELECT username FROM users WHERE family_id = ?", (u['family_id'],)).fetchall()
        res = f"👨‍👩‍👧 <b>Семья: {f['name']}</b>\n\n<b>Участники:</b>\n"
        for i, r in enumerate(mems, 1): res += f"{i}. {r['username']}\n"
        await m.answer(res, parse_mode="HTML")

@dp.message(F.text == "✉️ Пригласить в семью")
async def fam_invite(m: types.Message):
    with get_db() as conn:
        u = conn.execute("SELECT family_id FROM users WHERE user_id = ?", (m.from_user.id,)).fetchone()
        f = conn.execute("SELECT * FROM families WHERE id = ?", (u['family_id'],)).fetchone()
        link = f"https://t.me/{BOT_USERNAME}?start={f['token']}"
        await m.answer(f"🌟 <b>{m.from_user.full_name}</b> приглашает в семью <b>{f['name']}</b>!\n\n🔗 {link}\n\nТокен: <code>{f['token']}</code>", parse_mode="HTML")

@dp.message(F.text == "🗑 Удалить семью")
async def fam_del_q(m: types.Message, state: FSMContext):
    with get_db() as conn:
        u = conn.execute("SELECT family_id FROM users WHERE user_id = ?", (m.from_user.id,)).fetchone()
        f = conn.execute("SELECT name FROM families WHERE id = ?", (u['family_id'],)).fetchone()
        await m.answer(f"Удалить семью {f['name']}? ВСЕ блюда будут стерты!", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="💀 Да, удалить всё"), types.KeyboardButton(text="❌ Отмена")]], resize_keyboard=True))
        await state.set_state(FamilyState.deleting)


@dp.message(F.text == "🚪 Уйти из семьи")
async def fam_leave_q(m: types.Message):
    with get_db() as conn:
        u = conn.execute("SELECT family_id FROM users WHERE user_id = ?", (m.from_user.id,)).fetchone()
        f = conn.execute("SELECT name FROM families WHERE id = ?", (u['family_id'],)).fetchone()
        kb = [[types.KeyboardButton(text="🥲 Да, уйти"), types.KeyboardButton(text="❌ Нет, остаться")]]
        await m.answer(f"Покинуть семью {f['name']}?", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text == "🥲 Да, уйти")
async def fam_leave_yes(m: types.Message):
    with get_db() as conn:
        u = conn.execute("SELECT family_id FROM users WHERE user_id = ?", (m.from_user.id,)).fetchone()
        f = conn.execute("SELECT head_id FROM families WHERE id = ?", (u['family_id'],)).fetchone()
        conn.execute("UPDATE users SET family_id = NULL WHERE user_id = ?", (m.from_user.id,))
        try: await bot.send_message(f['head_id'], f"🥲 {m.from_user.full_name} ушел из семьи...")
        except: pass
    await m.answer("Вы вышли.", reply_markup=main_kb(get_dish_count(m.from_user.id, 'user')))

# --- DISH LOGIC ---
@dp.message(F.text == "📜 Список всех блюд")
async def list_dishes(m: types.Message):
    oid, otyp = get_ctx(m.from_user.id); count = get_dish_count(oid, otyp)
    if count == 0: return await m.answer("Пусто.", reply_markup=main_kb(0))
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM dishes WHERE owner_id = ? AND owner_type = ?", (oid, otyp)).fetchall()
        res = "📋 <b>Список:</b>\n\n"
        for r in rows: res += f"#{r['id']} {r['name']} {'🍭' if r['is_sweet'] else '🥩'} ({R_MAP.get(r['category'])})\n"
        await m.answer(res, parse_mode="HTML", reply_markup=main_kb(count))

@dp.message(F.text == "🔍 Просмотр состава")
async def v1(m: types.Message, state: FSMContext):
    await m.answer("Введите ID:", reply_markup=cancel_kb()); await state.set_state(ViewDish.dish_id)

@dp.message(ViewDish.dish_id)
async def v2(m: types.Message, state: FSMContext):
    if not m.text.isdigit(): return
    oid, otyp = get_ctx(m.from_user.id)
    with get_db() as conn:
        dish = conn.execute("SELECT * FROM dishes WHERE id = ? AND owner_id = ? AND owner_type = ?", (int(m.text), oid, otyp)).fetchone()
        if not dish: return await m.answer("Не найдено.")
        ings = conn.execute("SELECT * FROM dish_ingredients WHERE dish_id = ?", (dish['id'],)).fetchall()
        res = f"🍲 <b>#{dish['id']} {dish['name']}</b>\n🛒 <b>Состав:</b>\n"
        for i in ings: res += f"▫️ {i['ingredient_name']} {i['amount']:g} {i['unit']}\n"
        await m.answer(res, parse_mode="HTML", reply_markup=main_kb(get_dish_count(oid, otyp))); await state.clear()

@dp.message(F.text == "🍽 Генерация меню")
async def gen_menu(m: types.Message):
    oid, otyp = get_ctx(m.from_user.id)
    with get_db() as conn:
        all_d = [dict(r) for r in conn.execute("SELECT * FROM dishes WHERE owner_id = ? AND owner_type = ?", (oid, otyp)).fetchall()]
        all_i = [dict(r) for r in conn.execute("SELECT dish_id, ingredient_name, amount, unit FROM dish_ingredients").fetchall()]
    if len(all_d) < 4: return await m.answer("Мало блюд!")
    menu = []; used = set()
    for _ in range(3):
        day = {}; has_s = False
        for c in ["breakfast", "side", "meat", "dinner"]:
            cand = [d for d in all_d if d['category'] == c and d['id'] not in used]
            if has_s: cand = [d for d in cand if d['is_sweet'] == 0]
            if not cand: return await m.answer("Ошибка генерации.")
            ch = random.choice(cand); used.add(ch['id']); day[c] = ch
            if ch['is_sweet']: has_s = True
        menu.append(day)
    msg = "📋 <b>Меню на 3 дня:</b>\n\n"; shop = {}
    for i, d_p in enumerate(menu, 1):
        msg += f"📅 <b>День {i}:</b>\n"
        for ck in ["breakfast", "side", "meat", "dinner"]:
            dish = d_p[ck]; msg += f"{R_MAP[ck]}: #{dish['id']} {dish['name']}{' 🍭' if dish['is_sweet'] else ''}\n"
            for it in [ing for ing in all_i if ing['dish_id'] == dish['id']]:
                k = (it['ingredient_name'].lower().strip(), it['unit'].lower().strip())
                if k not in shop: shop[k] = {'t': 0, 's': 0}
                shop[k]['t'] += it['amount'];
                if dish['is_sweet']: shop[k]['s'] += it['amount']
        msg += "—"*12 + "\n"
    msg += "\n🛒 <b>ИТОГО:</b>\n"
    for (n,u), data in shop.items():
        msg += f"▫️ {n}: {data['t']:g} {u}" + (f" ({data['s']:g} 🍭)\n" if data['s'] > 0 else "\n")
    await m.answer(msg, parse_mode="HTML")

@dp.message(F.text == "➕ Добавить блюдо")
async def add1(m: types.Message, state: FSMContext):
    await m.answer("Название:", reply_markup=cancel_kb()); await state.set_state(AddDish.name)

@dp.message(AddDish.name)
async def add2(m: types.Message, state: FSMContext):
    await state.update_data(n=m.text); kb = [[types.KeyboardButton(text=k)] for k in C_MAP.keys()]; kb.append([types.KeyboardButton(text="❌ Отмена")])
    await m.answer("Категория:", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)); await state.set_state(AddDish.cat)

@dp.message(AddDish.cat)
async def add3(m: types.Message, state: FSMContext):
    if m.text not in C_MAP: return
    await state.update_data(c=C_MAP[m.text]); kb = [[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")], [types.KeyboardButton(text="❌ Отмена")]]
    await m.answer("Сладкое?", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)); await state.set_state(AddDish.sweet)

@dp.message(AddDish.sweet)
async def add4(m: types.Message, state: FSMContext):
    await state.update_data(s=1 if m.text.lower()=="да" else 0); await m.answer("Состав (Название Количество Ед):", reply_markup=cancel_kb()); await state.set_state(AddDish.ingr)

@dp.message(AddDish.ingr)
async def add5(m: types.Message, state: FSMContext):
    dt = await state.get_data(); oid, otyp = get_ctx(m.from_user.id)
    try:
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO dishes (name, category, is_sweet, owner_id, owner_type) VALUES (?, ?, ?, ?, ?)", (dt['n'], dt['c'], dt['s'], oid, otyp))
            did = cur.lastrowid
            for line in m.text.split('\n'):
                p = line.strip().split()
                if len(p) >= 3: cur.execute("INSERT INTO dish_ingredients (dish_id, ingredient_name, amount, unit) VALUES (?, ?, ?, ?)", (did, " ".join(p[:-2]), float(p[-2].replace(',','.')), p[-1]))
            conn.commit()
        await m.answer("✅ Добавлено!", reply_markup=main_kb(get_dish_count(oid, otyp))); await state.clear()
    except Exception as e: await m.answer(f"Ошибка: {e}")

@dp.message(F.text == "✏️ Отредактировать")
async def edit1(m: types.Message, state: FSMContext):
    await m.answer("Введите ID блюда:", reply_markup=cancel_kb()); await state.set_state(EditDish.dish_id)

@dp.message(EditDish.dish_id)
async def edit2(m: types.Message, state: FSMContext):
    if not m.text.isdigit(): return
    await state.update_data(did=int(m.text))
    kb = [[types.KeyboardButton(text=x)] for x in ["Название", "Категория", "Сладкое", "Состав"]]; kb.append([types.KeyboardButton(text="❌ Отмена")])
    await m.answer("Что меняем?", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)); await state.set_state(EditDish.field)

@dp.message(EditDish.field)
async def edit3(m: types.Message, state: FSMContext):
    if m.text not in ["Название", "Категория", "Сладкое", "Состав"]: return
    await state.update_data(f=m.text)
    if m.text == "Категория":
        kb = [[types.KeyboardButton(text=k)] for k in C_MAP.keys()]; kb.append([types.KeyboardButton(text="❌ Отмена")])
        await m.answer("Новая категория:", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
    elif m.text == "Сладкое":
        kb = [[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")], [types.KeyboardButton(text="❌ Отмена")]]
        await m.answer("Сладкое?", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))
    else: await m.answer(f"Введите новое значение:", reply_markup=cancel_kb())
    await state.set_state(EditDish.value)

@dp.message(EditDish.value)
async def edit4(m: types.Message, state: FSMContext):
    d = await state.get_data(); did, field, val = d['did'], d['f'], m.text
    with get_db() as conn:
        cur = conn.cursor()
        if field == "Название": cur.execute("UPDATE dishes SET name=? WHERE id=?", (val, did))
        elif field == "Категория": cur.execute("UPDATE dishes SET category=? WHERE id=?", (C_MAP.get(val, "breakfast"), did))
        elif field == "Сладкое": cur.execute("UPDATE dishes SET is_sweet=? WHERE id=?", (1 if val.lower()=="да" else 0, did))
        elif field == "Состав":
            cur.execute("DELETE FROM dish_ingredients WHERE dish_id=?", (did,))
            for line in val.split('\n'):
                p = line.strip().split()
                if len(p) >= 3: cur.execute("INSERT INTO dish_ingredients (dish_id, ingredient_name, amount, unit) VALUES (?, ?, ?, ?)", (did, " ".join(p[:-2]), float(p[-2].replace(',','.')), p[-1]))
        conn.commit()
    oid, otyp = get_ctx(m.from_user.id)
    await m.answer("✅ Обновлено!", reply_markup=main_kb(get_dish_count(oid, otyp))); await state.clear()

@dp.message(F.text == "🗑 Удалить блюдо")
async def del1(m: types.Message, state: FSMContext):
    await m.answer("Введите ID:", reply_markup=cancel_kb()); await state.set_state(DelDish.dish_id)

@dp.message(DelDish.dish_id)
async def del2(m: types.Message, state: FSMContext):
    if not m.text.isdigit(): return
    with get_db() as conn: conn.execute("DELETE FROM dishes WHERE id = ?", (int(m.text),)); conn.commit()
    oid, otyp = get_ctx(m.from_user.id)
    await m.answer("Удалено.", reply_markup=main_kb(get_dish_count(oid, otyp))); await state.clear()

# --- UTILS ---
@dp.message(F.text == "⬅️ В главное меню")
@dp.message(F.text == "⬅️ В меню Семья")
async def back_h(m: types.Message, state: FSMContext):
    await state.clear()
    if m.text == "⬅️ В меню Семья": await fam_menu(m)
    else:
        oid, otyp = get_ctx(m.from_user.id)
        await m.answer("Меню:", reply_markup=main_kb(get_dish_count(oid, otyp)))

@dp.message(F.text.lower() == "что приготовить?")
async def easter_egg(m: types.Message): await m.answer("1. Лазанья\n2. Хачапури\n3. Сосиски в тесте")

@dp.message(F.text == "⚙️ Управление семьей")
async def fam_admin(m: types.Message):
    with get_db() as conn:
        u = conn.execute("SELECT family_id FROM users WHERE user_id = ?", (m.from_user.id,)).fetchone()
        mems = conn.execute("SELECT user_id, username FROM users WHERE family_id = ? AND user_id != ?", (u['family_id'], m.from_user.id)).fetchall()
        res = "👥 <b>Участники для изгнания:</b>\n"
        if not mems: res += "Никого нет."
        for row in mems: res += f"▫️ {row['username']} (ID: <code>{row['user_id']}</code>)\n"
        kb = [[types.KeyboardButton(text="🚷 Выгнать")], [types.KeyboardButton(text="⬅️ В меню Семья")]]
        await m.answer(res, parse_mode="HTML", reply_markup=types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True))

@dp.message(F.text == "🚷 Выгнать")
async def fam_kick_1(m: types.Message, state: FSMContext):
    await m.answer("Введите ID пользователя:", reply_markup=cancel_kb()); await state.set_state(FamilyState.expelling)

@dp.message(FamilyState.expelling)
async def fam_kick_2(m: types.Message, state: FSMContext):
    if not m.text.isdigit(): return
    target_id = int(m.text)
    with get_db() as conn:
        conn.execute("UPDATE users SET family_id = NULL WHERE user_id = ?", (target_id,))
        conn.commit()
        try: await bot.send_message(target_id, f"🚫 {m.from_user.full_name} изгнал тебя из семьи, хорошо, что есть вторая!")
        except: pass
    await m.answer("Выгнано.", reply_markup=main_kb(get_dish_count(*get_ctx(m.from_user.id)))); await state.clear()

async def main(): init_db(); await dp.start_polling(bot)
if __name__ == "__main__": asyncio.run(main())
_EOF_