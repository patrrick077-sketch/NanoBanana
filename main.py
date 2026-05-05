import telebot, requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

z1 = '8733400839:AAExD28i7DpnC7DWc4C2wGTks5cDGighqOk' # Your token

z2 = 'https://t.me/NanoBanana_MM/2' # Image link 
z3 = 'https://zecora0.serv00.net/ai/NanoBanana.php' # Do not change
z4 = 'CAACAgIAAxkBAAERGrpp6qpwhZeU1z7ksy3kgUrtPadzwAACQgEAAs0bMAgEAoCtK287vjsE' # Loading sticker 

# Channel Chat IDs (Required for membership checking)
CH1 = '@Myid_AllHacking_Methods'
CH2 = '@NanoBanana_MM'

zeco = telebot.TeleBot(z1, parse_mode='HTML')
zmem = {}

# ================== UI TEXT TEMPLATES ==================

AUTH_TEXT = (
    "<b>⚠️ Access Restricted</b>\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "You must join our official channels to use the AI generation features.\n\n"
    "<i>Join both channels below, then click '✅ I've Joined'.</i> 👇"
)

START_CAPTION = (
    "<b>Welcome to NanoBanana 👋</b>\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "I provide advanced AI image generation and editing with the highest quality standards. <tg-emoji emoji-id=\"6003330781827570462\">✨</tg-emoji>\n\n"
    "<blockquote expandable=\"⚠️ Guidelines & Restrictions\">\n"
    "• Strictly no rights violations or protected material.\n"
    "• Precise requests may require multiple adjustment experiments.</blockquote>\n"
    "<i>Select an option below to get started.</i> <tg-emoji emoji-id=\"6003492753634237241\">👇</tg-emoji>"
)

SELECT_MODEL_TEXT = (
    "<b>⚙️ Select AI Model</b>\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "Choose the engine that best fits your vision <tg-emoji emoji-id=\"6003492753634237241\">😘</tg-emoji>"
)

SELECT_RATIO_TEXT = (
    "<b>📐 Select Aspect Ratio</b>\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "Define the dimensions of your canvas <tg-emoji emoji-id=\"6003330781827570462\">👀</tg-emoji>"
)

SELECT_RES_TEXT = (
    "<b>🎞️ Select Resolution</b>\n"
    "━━━━━━━━━━━━━━━━━━━\n"
    "Higher resolution yields more detail <tg-emoji emoji-id=\"6003675891039738414\">😅</tg-emoji>"
)

ERROR_TEXT = "<b>⚠️ Process Failed</b>\n<i>An error occurred during generation. Please try again.</i> <tg-emoji emoji-id=\"6001087142451748852\">😔</tg-emoji>"
NO_IMAGE_TEXT = "<b>⚠️ Invalid Input</b>\n<i>Please send a valid image file to proceed.</i>"
IMAGE_RECEIVED_TEXT = "<b>✅ Image Received</b>\n<i>Now send the text instructions for editing...</i> <tg-emoji emoji-id=\"6003646513463434273\">😀</tg-emoji>"
RANDOM_TEXT_MSG = "<b>👋 Hey there!</b>\n<i>Please use the main menu below to start creating.</i>"

# ================== MEMBERSHIP CHECK LOGIC ==================

def zcheck(zuid, zcid, zmid=None):
    """Checks if user is in both channels. Returns True if joined, False if not."""
    try:
        u1 = zeco.get_chat_member(CH1, zuid).status
        u2 = zeco.get_chat_member(CH2, zuid).status
        
        if u1 in ['member', 'administrator', 'creator'] and u2 in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Membership check failed (Ensure bot is admin in both channels): {e}")
        
    try:
        if zmid:
            zeco.delete_message(zcid, zmid) 
    except:
        pass
        
    zkb = InlineKeyboardMarkup(row_width=2)
    zkb.add(
        InlineKeyboardButton("🌐 Main Channel", url=f"https://t.me/{CH1[1:]}"),
        InlineKeyboardButton("🍌 Nano Banana", url=f"https://t.me/{CH2[1:]}")
    )
    zkb.add(InlineKeyboardButton("✅ I've Joined", callback_data='zcheck'))
    
    zeco.send_message(zcid, AUTH_TEXT, reply_markup=zkb)
    return False

# ================== BOT LOGIC ==================

@zeco.message_handler(commands=['start'])
def zstart(zmsg):
    zuid = zmsg.from_user.id
    zcid = zmsg.chat.id
    
    if not zcheck(zuid, zcid, zmsg.message_id):
        return
        
    zmem.pop(zuid, None)
    zkb = InlineKeyboardMarkup(row_width=2)
    zkb.add(
        InlineKeyboardButton("🎨 Create Image", callback_data='za'), 
        InlineKeyboardButton("✏️ Edit Image", callback_data='zb')
    )
    zeco.send_photo(zcid, z2, caption=START_CAPTION, reply_markup=zkb, has_spoiler=True)

def zapi(zdata):
    try:
        zr = requests.post(z3, data=zdata, timeout=120)
        return zr.json() if zr.status_code == 200 else None
    except:
        return None

@zeco.callback_query_handler(func=lambda zc: True)
def zcb(zc):
    zeco.answer_callback_query(zc.id)
    zcid = zc.message.chat.id
    zmid = zc.message.message_id
    zuid = zc.from_user.id
    zdata = zc.data

    if zdata == 'zcheck':
        if zcheck(zuid, zcid, zmid):
            try:
                zeco.delete_message(zcid, zmid)
            except:
                pass
            zmem.pop(zuid, None)
            zkb = InlineKeyboardMarkup(row_width=2)
            zkb.add(
                InlineKeyboardButton("🎨 Create Image", callback_data='za'), 
                InlineKeyboardButton("✏️ Edit Image", callback_data='zb')
            )
            zeco.send_photo(zcid, z2, caption=START_CAPTION, reply_markup=zkb, has_spoiler=True)
        return

    if not zcheck(zuid, zcid, zmid):
        return

    if zdata == 'zz':
        zmem.pop(zuid, None)
        zeco.delete_message(zcid, zmid)
        zkb = InlineKeyboardMarkup(row_width=2)
        zkb.add(
            InlineKeyboardButton("🎨 Create Image", callback_data='za'), 
            InlineKeyboardButton("✏️ Edit Image", callback_data='zb')
        )
        zeco.send_photo(zcid, z2, caption=START_CAPTION, reply_markup=zkb, has_spoiler=True)
        return

    if zdata in ('za', 'zb'):
        zmem[zuid] = {'zm': 'create' if zdata == 'za' else 'edit'}
        zkb = InlineKeyboardMarkup(row_width=1)
        for zmod in ['NanoBanana', 'NanoBanana2', 'NanoBananaPro']:
            zkb.add(InlineKeyboardButton(f"➤ {zmod}", callback_data=f'zc|{zmod}'))
        zkb.add(InlineKeyboardButton("◀️ Back", callback_data='zz'))
        try:
            zeco.edit_message_caption(chat_id=zcid, message_id=zmid, caption=SELECT_MODEL_TEXT, reply_markup=zkb)
        except:
            pass
        return

    if zdata.startswith('zc|'):
        zmod = zdata.split('|')[1]
        zmem[zuid]['zmod'] = zmod
        zkb = InlineKeyboardMarkup(row_width=3)
        for zrat in ['1:1','1:4','1:8','2:3','3:2','3:4','4:1','4:3','4:5','5:4','8:1','9:16','16:9','21:9','auto']:
            zkb.add(InlineKeyboardButton(zrat, callback_data=f'zd|{zrat}'))
        zkb.add(InlineKeyboardButton("◀️ Back", callback_data='zz'))
        try:
            zeco.edit_message_caption(chat_id=zcid, message_id=zmid, caption=SELECT_RATIO_TEXT, reply_markup=zkb)
        except:
            pass
        return

    if zdata.startswith('zd|'):
        zrat = zdata.split('|')[1]
        zmem[zuid]['zrat'] = zrat
        zkb = InlineKeyboardMarkup(row_width=3)
        for zres in ['1K','2K','4K']:
            zkb.add(InlineKeyboardButton(f"⚙ {zres}", callback_data=f'ze|{zres}'))
        zkb.add(InlineKeyboardButton("◀️ Back", callback_data='zz'))
        try:
            zeco.edit_message_caption(chat_id=zcid, message_id=zmid, caption=SELECT_RES_TEXT, reply_markup=zkb)
        except:
            pass
        return

    if zdata.startswith('ze|'):
        zres = zdata.split('|')[1]
        zst = zmem[zuid]
        zst['zres'] = zres
        if 'zrat' not in zst: zst['zrat'] = '1:1'
        if 'zmod' not in zst: zst['zmod'] = 'NanoBanana2'
        
        zmode = zst['zm']
        zmoddisp = zst['zmod']
        if zmoddisp == 'NanoBanana2': zmoddisp = 'NanoBanana 2'
        elif zmoddisp == 'NanoBananaPro': zmoddisp = 'NanoBanana Pro'
        
        zemj = '<tg-emoji emoji-id="6001051949489724852">🌹</tg-emoji>' if zmode == 'create' else '<tg-emoji emoji-id="6001102535614537900">🕺</tg-emoji>'
        zeac = '<tg-emoji emoji-id="6003470660322466579">👨‍💻</tg-emoji>' if zmode == 'create' else '<tg-emoji emoji-id="6001111189973639198">😀</tg-emoji>'
        zactxt = 'Send the text prompt to generate' if zmode == 'create' else 'Send the image you want to edit'
        
        znewcap = (
            f"<b>🎉 Ready to Generate</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<b>Model :</b> <code>{zmoddisp}</code> {zemj}\n"
            f"<b>Ratio :</b> <code>{zst['zrat']}</code> │ <b>Quality :</b> <code>{zres}</code>\n\n"
            f"<i>{zactxt} {zeac}</i>"
        )
        
        zkb = InlineKeyboardMarkup().add(InlineKeyboardButton("◀️ Back", callback_data='zz'))
        try:
            zeco.edit_message_caption(chat_id=zcid, message_id=zmid, caption=znewcap, reply_markup=zkb)
        except:
            pass
            
        if zmode == 'create':
            zeco.register_next_step_handler(zc.message, zezeze3, zuid)
        else:
            zeco.register_next_step_handler(zc.message, zezeze2, zuid)
        return

@zeco.message_handler(func=lambda zx: True)
def zother(zx):
    if zx.text and zx.text != '/start':
        if not zmem.get(zx.from_user.id):
            zkb = InlineKeyboardMarkup().add(InlineKeyboardButton("🚀 Open Menu", callback_data='zz'))
            zeco.send_message(zx.chat.id, RANDOM_TEXT_MSG, reply_markup=zkb)

def zezeze3(zmsg, zuid):
    zst = zmem.pop(zuid, None)
    if not zst:
        return
    zcid = zmsg.chat.id
    
    if not zcheck(zuid, zcid, zmsg.message_id):
        return
        
    zsticker = zeco.send_sticker(zcid, z4)
    zsid = zsticker.message_id
    
    zmod = zst['zmod']
    zrat = zst['zrat']
    zres = zst['zres']
    zapim = 'NanoBanana2' if zmod == 'NanoBananaPro' else zmod
    
    # --- STEALTH WATERMARK LOGIC FOR CREATION ---
    # It tells the AI to blend it into the background naturally
    zfinaltext = f"{zmsg.text}, subtly include the text 'NightMare' blending naturally into the background"
    
    zresp = zapi({'text': zfinaltext, 'model': zapim, 'ratio': zrat, 'res': zres})
    try:
        zeco.delete_message(zcid, zsid)
    except:
        pass
        
    zkb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔄 New Image", callback_data='zz'))
    
    if zresp and zresp.get('success') and zresp.get('url'):
        zcap = (
            f"<b>✨ Image Generated Successfully</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<code>{zmod}</code> <tg-emoji emoji-id=\"6001051949489724852\">🌹</tg-emoji> │ "
            f"<code>{zrat}</code> │ "
            f"<code>{zresp.get('resolution', zres)}</code>"
        )
        zeco.send_photo(zcid, zresp['url'], caption=zcap, has_spoiler=True, reply_markup=zkb)
    else:
        zeco.send_message(zcid, ERROR_TEXT, reply_markup=zkb)

def zezeze2(zmsg, zuid):
    if not zcheck(zuid, zmsg.chat.id, zmsg.message_id):
        return
        
    if not zmsg.photo:
        zeco.send_message(zmsg.chat.id, NO_IMAGE_TEXT)
        zeco.register_next_step_handler(zmsg, zezeze2, zuid)
        return
    zst = zmem.get(zuid)
    if not zst:
        return
    zcid = zmsg.chat.id
    zfid = zmsg.photo[-1].file_id
    zfinfo = zeco.get_file(zfid)
    zimgurl = f"https://api.telegram.org/file/bot{z1}/{zfinfo.file_path}"
    zst['zimg'] = zimgurl
    zeco.send_message(zcid, IMAGE_RECEIVED_TEXT)
    zeco.register_next_step_handler(zmsg, zezeze1, zuid)

def zezeze1(zmsg, zuid):
    zst = zmem.pop(zuid, None)
    if not zst or 'zimg' not in zst:
        return
    zcid = zmsg.chat.id
    
    if not zcheck(zuid, zcid, zmsg.message_id):
        return
        
    zsticker = zeco.send_sticker(zcid, z4)
    zsid = zsticker.message_id
    
    zmod = zst['zmod']
    zrat = zst['zrat']
    zres = zst['zres']
    zimg = zst['zimg']
    zapim = 'NanoBanana2' if zmod == 'NanoBananaPro' else zmod
    
    # --- STEALTH WATERMARK LOGIC FOR EDITING ---
    zfinaltext = f"{zmsg.text}, subtly include the text 'NightMare' blending naturally into the background"
    
    zresp = zapi({'text': zfinaltext, 'model': zapim, 'links': zimg, 'ratio': zrat, 'res': zres})
    try:
        zeco.delete_message(zcid, zsid)
    except:
        pass
        
    zkb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔄 New Image", callback_data='zz'))
    
    if zresp and zresp.get('success') and zresp.get('url'):
        zcap = (
            f"<b>✨ Image Edited Successfully</b>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"<code>{zmod}</code> <tg-emoji emoji-id=\"6001051949489724852\">🌹</tg-emoji> │ "
            f"<code>{zrat}</code> │ "
            f"<code>{zresp.get('resolution', zres)}</code>"
        )
        zeco.send_photo(zcid, zresp['url'], caption=zcap, has_spoiler=True, reply_markup=zkb)
    else:
        zeco.send_message(zcid, ERROR_TEXT, reply_markup=zkb)

zeco.infinity_polling()