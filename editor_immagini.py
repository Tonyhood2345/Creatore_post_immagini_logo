import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# 1. RECUPERO DATI DA DARIA (TRAMITE GITHUB ACTIONS)
azione = os.environ.get('AZIONE', '')
tipo = os.environ.get('TIPO', '')
luogo = os.environ.get('LUOGO', '')
foto_url = os.environ.get('FOTO_URL', '')
fb_token = os.environ.get('FB_TOKEN', '')

print(f"Avvio elaborazione per: {azione} {tipo} a {luogo}")

# 2. SCARICA L'IMMAGINE E IL LOGO
response_foto = requests.get(foto_url)
img = Image.open(BytesIO(response_foto.content)).convert("RGBA")

# (Assicurati di avere un file 'logo_orizzontale.png' nel tuo repository GitHub)
try:
    logo = Image.open('logo_orizzontale.png').convert("RGBA")
    # Ridimensiona il logo in modo che sia largo il 30% della foto
    logo_width = int(img.width * 0.30)
    logo_ratio = logo_width / float(logo.width)
    logo_height = int(float(logo.height) * float(logo_ratio))
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    
    # Posiziona il logo in alto a destra
    posizione_logo = (img.width - logo_width - 20, 20)
    img.paste(logo, posizione_logo, logo)
except Exception as e:
    print(f"Logo non trovato o errore: {e}")

# 3. SCRIVI I TESTI SULLA FOTO
draw = ImageDraw.Draw(img)
# Usa un font di default (se vuoi un font figo, carica un .ttf nel repo e usa ImageFont.truetype)
font = ImageFont.load_default() 

testo_finale = f"{azione} {tipo}\n{luogo}"
if testo_finale.strip():
    # Sfondo nero semitrasparente per far leggere bene la scritta
    sfondo_box = [20, 20, 400, 100] 
    draw.rectangle(sfondo_box, fill=(0, 0, 0, 150))
    draw.text((30, 30), testo_finale.strip(), fill=(255, 255, 255), font=font)

# Salva il risultato
nome_file_output = "immobile_pronto.png"
img_rgb = img.convert("RGB")
img_rgb.save(nome_file_output, "JPEG")
print("Immagine creata con successo!")

# ============================================================
# 4. PREDISPOSIZIONE PER FACEBOOK CATALOG E POST PROGRAMMATO
# ============================================================
# Quando Meta ti sblocca l'API, questa funzione uploaderà la foto 
# e creerà il Carosello per le 18:00.

def pubblica_su_facebook_catalogo():
    # ID del tuo Catalogo Business
    catalog_id = "IL_TUO_CATALOG_ID" 
    
    # 1. Caricamento Immagine su server/Meta
    # 2. Inserimento prodotto nel catalogo tramite Graph API:
    # url = f"https://graph.facebook.com/v21.0/{catalog_id}/products"
    # payload = { "name": f"{tipo} a {luogo}", "description": f"Splendido {tipo}...", "image_url": "URL_IMMAGINE_GENERATA" ... }
    
    # 3. Programmazione Post (Carosello)
    # page_id = "TUO_PAGE_ID"
    # L'orario (es. 18:00 di oggi) si calcola in UNIX Timestamp
    # schedule_url = f"https://graph.facebook.com/v21.0/{page_id}/feed"
    # schedule_payload = { "message": "Nuova Acquisizione!", "published": False, "scheduled_publish_time": TIMESTAMP_18_00 }
    pass

# Se vuoi, invia l'immagine creata di nuovo a Telegram per farti vedere il risultato!
def invia_anteprima_a_boss():
    bot_token = "IL_TUO_TOKEN_TELEGRAM_DI_PRIMA"
    chat_id = "1723292483"
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    with open(nome_file_output, 'rb') as f:
        requests.post(url, data={'chat_id': chat_id}, files={'photo': f})

invia_anteprima_a_boss()
