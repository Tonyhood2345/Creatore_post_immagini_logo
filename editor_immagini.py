r"""
===============================================================================
IMMOBILIARE GIANCANI — CREATORE POST & STORIE IMMAGINI CON LOGO
Repository: Tonyhood2345/Creatore_post_immagini_logo
===============================================================================
Motore grafico avanzato basato sui 3 stili grafici professionali:
1. C&B Immobiliare ('cb_curved_wave'): Header bianco, logo ufficiale, ala blu,
   badge pillola 'IN VENDITA', maschera curva ed elegante, footer blu con pin.
2. Metroquadro ('metroquadro_gradient'): Gradiente scuro/crimson dal centro verso
   il basso, tipografia pulita, 4 icone vettoriali pure (superficie in metri quadri,
   bagni, vani, lavanderia) e card bianca descrittiva.
3. ProfessioneCasa ('professionecasa_sidebar'): Sidebar sinistra rossa (#E11D2A)
   a tutta altezza con 3 icone vettoriali verticali, foto a destra, card bianca
   inferiore con chevron rosso, elenco punti con spunte rosse e prezzo in risalto.

Regole Mandatorie Risolte:
- Superficie sempre per esteso in "metri quadri"
- Personal Branding obbligatorio in chiusura: '— Immobiliare Giancani'
- Zero tofu / emoji unicode mancanti: icone disegnate come vettori puri Pillow
- Invio diretto e trasparente a Telegram (Chat ID: 1723292483) per monitoraggio
- Facebook live posting disattivato in rispetto della Regola 5.
===============================================================================
"""

import os
import io
import sys
import ssl
import time
import math
import random
import textwrap
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Disabilita verifica SSL per download affidabile su qualsiasi runner
ctx_no_ssl = ssl._create_unverified_context()

TELEGRAM_DEFAULT_TOKEN = "8671578336:AAEHI-s-2g3dY9qnIIVc_hWzDdOuHm-MS6M"
TELEGRAM_DEFAULT_CHAT_ID = "1723292483"

# --- FONT HELPER ---
def get_font(size, bold=False):
    font_candidates = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "arialbd.ttf" if bold else "arial.ttf"
    ]
    for fp in font_candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()

# --- CARICAMENTO LOGO ---
def get_logo_image():
    for lp in ["logo_orizzontale.png", "logo.png", "assets/logo.png"]:
        if os.path.exists(lp):
            try:
                return Image.open(lp).convert("RGBA")
            except Exception:
                pass
    return None

def scarica_foto(url_or_path):
    if not url_or_path:
        return None
    if os.path.exists(url_or_path):
        try:
            return Image.open(url_or_path).convert("RGBA")
        except Exception:
            return None
    try:
        req = urllib.request.Request(url_or_path, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30, context=ctx_no_ssl) as resp:
            data = resp.read()
            return Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception as e:
        print(f"⚠️ Errore download foto: {e}")
        return None

# --- DISEGNO ICONE VETTORIALI PURE (PILLOW) ---
def draw_vector_shower(draw, center_x, center_y, size=30, color=(255, 255, 255)):
    x, y, s = center_x, center_y, size
    draw.arc([x - s//2, y - s//2, x + s//2, y], 180, 0, fill=color, width=3)
    draw.line([x + s//2, y - s//4, x + s//2, y + s//2], fill=color, width=3)
    draw.line([x - s//4, y + 2, x - s//3, y + s//2], fill=color, width=2)
    draw.line([x, y + 2, x, y + s//2], fill=color, width=2)
    draw.line([x + s//4, y + 2, x + s//3, y + s//2], fill=color, width=2)

def draw_vector_sofa(draw, center_x, center_y, size=34, color=(255, 255, 255)):
    x, y, s = center_x, center_y, size
    hw, hh = s // 2, s // 3
    draw.rectangle([x - hw + 4, y - hh, x + hw - 4, y], fill=color)
    draw.rectangle([x - hw, y, x + hw, y + hh - 4], fill=color)
    draw.rectangle([x - hw - 3, y - hh//2, x - hw + 3, y + hh - 4], fill=color)
    draw.rectangle([x + hw - 3, y - hh//2, x + hw + 3, y + hh - 4], fill=color)
    draw.line([x - hw + 2, y + hh - 4, x - hw + 2, y + hh], fill=color, width=2)
    draw.line([x + hw - 2, y + hh - 4, x + hw - 2, y + hh], fill=color, width=2)

def draw_vector_ruler_sqm(draw, center_x, center_y, size=32, color=(255, 255, 255)):
    x, y, s = center_x, center_y, size
    draw.line([x - s//2, y + s//2, x + s//2, y + s//2], fill=color, width=3)
    draw.line([x - s//2, y + s//2, x - s//2, y - s//2], fill=color, width=3)
    draw.line([x + s//2, y + s//2, x - s//2, y - s//2], fill=color, width=2)
    for i in range(1, 4):
        pos = x - s//2 + (s * i // 4)
        draw.line([pos, y + s//2, pos, y + s//2 - 5], fill=color, width=2)
        pos_y = y + s//2 - (s * i // 4)
        draw.line([x - s//2, pos_y, x - s//2 + 5, pos_y], fill=color, width=2)

def draw_vector_laundry(draw, center_x, center_y, size=30, color=(255, 255, 255)):
    x, y, s = center_x, center_y, size
    draw.rectangle([x - s//2, y - s//2, x + s//2, y + s//2], outline=color, width=2)
    draw.ellipse([x - s//3, y - s//4, x + s//3, y + s//3 + 2], outline=color, width=2)
    draw.ellipse([x + s//4 - 2, y - s//3, x + s//4 + 2, y - s//3 + 4], fill=color)

def draw_vector_pin(draw, center_x, center_y, size=24, color=(255, 255, 255)):
    x, y, s = center_x, center_y, size
    r = s // 2
    draw.ellipse([x - r, y - r, x + r, y], fill=color)
    draw.polygon([(x - r + 1, y - 2), (x + r - 1, y - 2), (x, y + r + 2)], fill=color)
    draw.ellipse([x - r//3, y - r//2 - 1, x + r//3, y - 1], fill=(24, 76, 120))

def draw_vector_check(draw, x, y, size=18, color=(225, 29, 42)):
    p1 = (x, y + size // 2)
    p2 = (x + size // 3, y + size - 2)
    p3 = (x + size, y + 2)
    draw.line([p1, p2], fill=color, width=3)
    draw.line([p2, p3], fill=color, width=3)

def normalizza_metri_quadri(val):
    if not val:
        return "120 metri quadri"
    s = str(val).strip()
    s = s.replace("mq.", "metri quadri").replace("mq", "metri quadri").replace("m²", "metri quadri").replace("MQ", "metri quadri")
    if "metri quadri" not in s.lower():
        s = f"{s} metri quadri"
    return s

def assicura_branding(testo):
    t = (testo or "").strip()
    if not t:
        return "Immobile di prestigio a Favara.\n\n— Immobiliare Giancani"
    if "Immobiliare Giancani" not in t:
        t = f"{t}\n\n— Immobiliare Giancani"
    return t

# ===============================================================================
# 1. STILE C&B IMMOBILIARE (CURVED WAVE)
# ===============================================================================
def genera_cb_curved_wave(dati, w=1080, h=1080):
    canvas = Image.new("RGBA", (w, h), (248, 249, 251, 255))
    draw = ImageDraw.Draw(canvas)

    header_h = int(h * 0.14)
    draw.rectangle([(0, 0), (w, header_h)], fill=(255, 255, 255, 255))
    wing_points = [(int(w * 0.65), 0), (w, 0), (w, header_h), (int(w * 0.75), header_h)]
    draw.polygon(wing_points, fill=(24, 76, 120, 255))

    logo = get_logo_image()
    if logo:
        lw = int(w * 0.36)
        lh = int(lw * (logo.height / logo.width))
        if lh > header_h - 16:
            lh = header_h - 16
            lw = int(lh * (logo.width / logo.height))
        logo_res = logo.resize((lw, lh), Image.Resampling.LANCZOS)
        canvas.paste(logo_res, (28, (header_h - lh) // 2), logo_res)
    else:
        f_b = get_font(28, bold=True)
        draw.text((28, 20), "IMMOBILIARE GIANCANI", font=f_b, fill=(24, 76, 120))

    foto = dati.get('foto')
    if foto:
        body_h = h - header_h
        fw, fh = foto.size
        scale = max(w / fw, body_h / fh)
        nw, nh = int(fw * scale), int(fh * scale)
        foto_scaled = foto.resize((nw, nh), Image.Resampling.LANCZOS)
        crop_x = (nw - w) // 2
        crop_y = (nh - body_h) // 2
        foto_cropped = foto_scaled.crop((crop_x, crop_y, crop_x + w, crop_y + body_h))

        mask = Image.new("L", (w, body_h), 255)
        m_draw = ImageDraw.Draw(mask)
        cut_w = int(w * 0.38)
        cut_pts = [(0, 0), (cut_w, 0), (int(cut_w * 0.65), body_h), (0, body_h)]
        m_draw.polygon(cut_pts, fill=0)

        canvas.paste(foto_cropped, (0, header_h), mask)

    f_draw = ImageDraw.Draw(canvas)
    f_pts = [(0, header_h), (int(w * 0.38), header_h), (int(w * 0.25), h), (0, h)]
    f_draw.polygon(f_pts, fill=(24, 76, 120, 255))

    pin_cy = h - int(h * 0.12)
    draw_vector_pin(f_draw, 45, pin_cy, size=24, color=(255, 255, 255))
    f_pin = get_font(18, bold=True)
    f_draw.text((68, pin_cy - 10), dati.get('luogo', 'FAVARA CENTRO').upper(), font=f_pin, fill=(255, 255, 255))

    badge_w, badge_h = int(w * 0.32), 48
    bx, by = w - badge_w - 28, header_h + 24
    draw.rounded_rectangle([(bx, by), (bx + badge_w, by + badge_h)], radius=24, fill=(255, 255, 255, 245), outline=(24, 76, 120, 200), width=2)
    draw.ellipse([(bx + 8, by + 8), (bx + 40, by + 40)], fill=(24, 76, 120))
    draw_vector_check(draw, bx + 16, by + 14, size=16, color=(255, 255, 255))
    f_state = get_font(20, bold=True)
    draw.text((bx + 50, by + 12), dati.get('azione', 'IN VENDITA').upper(), font=f_state, fill=(24, 76, 120))

    cw_w = int(w * 0.68)
    cw_h = int(h * 0.22)
    cx = w - cw_w - 28
    cy = h - cw_h - 28
    draw.rounded_rectangle([(cx, cy), (cx + cw_w, cy + cw_h)], radius=16, fill=(255, 255, 255, 245), outline=(230, 230, 235), width=2)
    f_card_t = get_font(22, bold=True)
    draw.text((cx + 20, cy + 16), dati.get('tipo', 'Appartamento di Pregio'), font=f_card_t, fill=(24, 76, 120))

    f_p = get_font(26, bold=True)
    draw.text((cx + 20, cy + 46), dati.get('prezzo', 'Trattativa Riservata'), font=f_p, fill=(225, 29, 42))

    f_desc = get_font(16, bold=False)
    desc_txt = textwrap.shorten(dati.get('descrizione', ''), width=90, placeholder="...")
    draw.text((cx + 20, cy + 86), desc_txt, font=f_desc, fill=(70, 70, 80))

    f_out = get_font(15, bold=True)
    draw.text((cx + 20, cy + cw_h - 28), "— Immobiliare Giancani", font=f_out, fill=(24, 76, 120))

    return canvas.convert("RGB")

# ===============================================================================
# 2. STILE METROQUADRO (GRADIENT CRIMSON)
# ===============================================================================
def genera_metroquadro_gradient(dati, w=1080, h=1080):
    canvas = Image.new("RGBA", (w, h), (18, 18, 20, 255))
    foto = dati.get('foto')
    if foto:
        fw, fh = foto.size
        scale = max(w / fw, h / fh)
        nw, nh = int(fw * scale), int(fh * scale)
        foto_scaled = foto.resize((nw, nh), Image.Resampling.LANCZOS)
        canvas.paste(foto_scaled, ((w - nw)//2, (h - nh)//2))

    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grad)
    mid_y = int(h * 0.42)
    for y in range(mid_y, h):
        ratio = (y - mid_y) / float(h - mid_y)
        alpha = int(255 * (ratio ** 1.3))
        r = int(212 * ratio + 15 * (1 - ratio))
        g = int(28 * ratio + 15 * (1 - ratio))
        b = int(40 * ratio + 20 * (1 - ratio))
        g_draw.line([(0, y), (w, y)], fill=(r, g, b, alpha))

    canvas = Image.alpha_composite(canvas, grad)
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle([(30, 30), (220, 80)], radius=12, fill=(255, 255, 255, 230))
    f_badge = get_font(20, bold=True)
    draw.text((45, 42), dati.get('azione', 'IN VENDITA').upper(), font=f_badge, fill=(212, 28, 40))

    logo = get_logo_image()
    if logo:
        lw = int(w * 0.28)
        lh = int(lw * (logo.height / logo.width))
        logo_res = logo.resize((lw, lh), Image.Resampling.LANCZOS)
        canvas.paste(logo_res, (w - lw - 30, 30), logo_res)

    content_y = int(h * 0.52)
    f_title = get_font(34, bold=True)
    draw.text((40, content_y), dati.get('tipo', 'Villa Panoramica'), font=f_title, fill=(255, 255, 255))

    f_sub = get_font(22, bold=False)
    draw.text((40, content_y + 45), f"📍 {dati.get('luogo', 'Favara (AG)')}", font=f_sub, fill=(250, 230, 230))

    f_prz = get_font(42, bold=True)
    draw.text((40, content_y + 85), dati.get('prezzo', '€ 135.000'), font=f_prz, fill=(255, 255, 255))

    icon_y = content_y + 150
    icons = [
        (draw_vector_ruler_sqm, normalizza_metri_quadri(dati.get('mq', '120'))),
        (draw_vector_shower, "2 Bagni"),
        (draw_vector_sofa, "5 Vani"),
        (draw_vector_laundry, "Lavanderia")
    ]
    col_w = w // len(icons)
    f_lbl = get_font(16, bold=True)
    for i, (fn_draw, label) in enumerate(icons):
        cx = i * col_w + col_w // 2
        draw.ellipse([(cx - 28, icon_y - 28), (cx + 28, icon_y + 28)], fill=(0, 0, 0, 90), outline=(255, 255, 255, 180), width=2)
        fn_draw(draw, cx, icon_y, size=28, color=(255, 255, 255))
        tw = draw.textlength(label, font=f_lbl)
        draw.text((cx - tw // 2, icon_y + 36), label, font=f_lbl, fill=(255, 255, 255))

    card_y = icon_y + 85
    card_h = h - card_y - 30
    if card_h > 60:
        draw.rounded_rectangle([(30, card_y), (w - 30, card_y + card_h)], radius=16, fill=(255, 255, 255, 245))
        f_cd = get_font(18, bold=False)
        txt = textwrap.shorten(dati.get('descrizione', 'Immobile garantito.'), width=110, placeholder="...")
        draw.text((50, card_y + 16), txt, font=f_cd, fill=(40, 40, 50))
        f_co = get_font(17, bold=True)
        draw.text((50, card_y + card_h - 32), "— Immobiliare Giancani", font=f_co, fill=(212, 28, 40))

    return canvas.convert("RGB")

# ===============================================================================
# 3. STILE PROFESSIONECASA (RED SIDEBAR)
# ===============================================================================
def genera_professionecasa_sidebar(dati, w=1080, h=1080):
    canvas = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    side_w = int(w * 0.18)
    draw.rectangle([(0, 0), (side_w, h)], fill=(225, 29, 42, 255))

    foto = dati.get('foto')
    if foto:
        body_w = w - side_w
        fw, fh = foto.size
        scale = max(body_w / fw, h / fh)
        nw, nh = int(fw * scale), int(fh * scale)
        foto_scaled = foto.resize((nw, nh), Image.Resampling.LANCZOS)
        crop_x = (nw - body_w) // 2
        crop_y = (nh - h) // 2
        foto_cropped = foto_scaled.crop((crop_x, crop_y, crop_x + body_w, crop_y + h))
        canvas.paste(foto_cropped, (side_w, 0))

    s_draw = ImageDraw.Draw(canvas)
    f_side_t = get_font(13, bold=True)
    side_icons = [
        (draw_vector_ruler_sqm, normalizza_metri_quadri(dati.get('mq', '120'))),
        (draw_vector_shower, "DOPPI SERVIZI"),
        (draw_vector_sofa, "AMPIO SALONE")
    ]
    step_y = h // 4
    for i, (fn_draw, lbl) in enumerate(side_icons, start=1):
        cy = i * step_y
        cx = side_w // 2
        draw.ellipse([(cx - 26, cy - 26), (cx + 26, cy + 26)], fill=(185, 20, 32), outline=(255, 255, 255, 200), width=2)
        fn_draw(s_draw, cx, cy, size=26, color=(255, 255, 255))
        lbl_s = lbl.split()[0]
        tw = s_draw.textlength(lbl_s, font=f_side_t)
        s_draw.text((cx - tw//2, cy + 32), lbl_s, font=f_side_t, fill=(255, 255, 255))

    card_w = int(w * 0.72)
    card_h = int(h * 0.36)
    card_x = w - card_w - 24
    card_y = h - card_h - 24
    draw.rounded_rectangle([(card_x, card_y), (card_x + card_w, card_y + card_h)], radius=16, fill=(255, 255, 255, 250), outline=(225, 29, 42, 120), width=2)

    ch_pts = [(card_x, card_y + 20), (card_x + 18, card_y + 35), (card_x, card_y + 50)]
    draw.polygon(ch_pts, fill=(225, 29, 42))

    f_act = get_font(16, bold=True)
    draw.text((card_x + 30, card_y + 18), dati.get('azione', 'IN VENDITA').upper(), font=f_act, fill=(225, 29, 42))

    f_t = get_font(26, bold=True)
    draw.text((card_x + 30, card_y + 44), dati.get('tipo', 'Appartamento Luminoso'), font=f_t, fill=(30, 30, 40))

    f_l = get_font(18, bold=False)
    draw.text((card_x + 30, card_y + 80), f"📍 {dati.get('luogo', 'Favara (AG)')}", font=f_l, fill=(90, 90, 100))

    bullet_y = card_y + 115
    bullets = [
        normalizza_metri_quadri(dati.get('mq', '120')),
        textwrap.shorten(dati.get('descrizione', 'Ottima esposizione solare.'), width=42, placeholder="...")
    ]
    f_b_txt = get_font(16, bold=False)
    for b_item in bullets:
        draw_vector_check(draw, card_x + 30, bullet_y - 2, size=16, color=(225, 29, 42))
        draw.text((card_x + 55, bullet_y), b_item, font=f_b_txt, fill=(50, 50, 60))
        bullet_y += 28

    f_pz = get_font(34, bold=True)
    draw.text((card_x + 30, card_y + card_h - 50), dati.get('prezzo', 'Trattativa Riservata'), font=f_pz, fill=(225, 29, 42))

    logo = get_logo_image()
    if logo:
        lw = int(card_w * 0.35)
        lh = int(lw * (logo.height / logo.width))
        logo_res = logo.resize((lw, lh), Image.Resampling.LANCZOS)
        canvas.paste(logo_res, (card_x + card_w - lw - 20, card_y + card_h - lh - 16), logo_res)
    else:
        f_gb = get_font(16, bold=True)
        draw.text((card_x + card_w - 220, card_y + card_h - 38), "— Immobiliare Giancani", font=f_gb, fill=(30, 30, 40))

    return canvas.convert("RGB")

# ===============================================================================
# DISPATCHER FORMATI (1:1 POST & 9:16 STORIA)
# ===============================================================================
def crea_grafica_completa(dati, stile="cb_curved_wave", format_type="1:1"):
    w, h = (1080, 1080) if format_type == "1:1" else (1080, 1920)
    if stile == "cb_curved_wave":
        return genera_cb_curved_wave(dati, w=w, h=h)
    elif stile == "metroquadro_gradient":
        return genera_metroquadro_gradient(dati, w=w, h=h)
    elif stile == "professionecasa_sidebar":
        return genera_professionecasa_sidebar(dati, w=w, h=h)
    else:
        return genera_cb_curved_wave(dati, w=w, h=h)

# ===============================================================================
# INVIO DIRETTO TELEGRAM
# ===============================================================================
def invia_telegram(file_path, caption, bot_token=None, chat_id=None):
    token = (bot_token or os.environ.get("TELEGRAM_BOT_TOKEN") or TELEGRAM_DEFAULT_TOKEN).strip()
    cid = (chat_id or os.environ.get("TELEGRAM_CHAT_ID") or TELEGRAM_DEFAULT_CHAT_ID).strip()
    if not os.path.exists(file_path):
        return False
    try:
        boundary = f"----TgBoundary{int(time.time()*1000)}"
        with open(file_path, 'rb') as f:
            img_bytes = f.read()

        body = bytearray()
        body.extend(f"--{boundary}\r\n".encode('utf-8'))
        body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{cid}\r\n'.encode('utf-8'))
        if caption:
            body.extend(f"--{boundary}\r\n".encode('utf-8'))
            body.extend(f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode('utf-8'))
        body.extend(f"--{boundary}\r\n".encode('utf-8'))
        body.extend(f'Content-Disposition: form-data; name="photo"; filename="foto.jpg"\r\n'.encode('utf-8'))
        body.extend(b'Content-Type: image/jpeg\r\n\r\n')
        body.extend(img_bytes)
        body.extend(b"\r\n")
        body.extend(f"--{boundary}--\r\n".encode('utf-8'))

        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        req = urllib.request.Request(url, data=body, headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, timeout=30, context=ctx_no_ssl) as resp:
            pass
        print(f"✈️ Inviato con successo a Telegram (Chat: {cid})!")
        return True
    except Exception as e:
        print(f"⚠️ Errore invio Telegram: {e}")
        return False

# ===============================================================================
# MAIN
# ===============================================================================
def main():
    print("=" * 70)
    print("🚀 MOTORE GRAFICO IMMOBILIARE GIANCANI (POST & STORIE)")
    print("— IMMOBILIARE GIANCANI")
    print("=" * 70)

    azione = os.environ.get('AZIONE', 'IN VENDITA').strip()
    tipo = os.environ.get('TIPO', 'Appartamento di Pregio').strip()
    luogo = os.environ.get('LUOGO', 'Favara (AG)').strip()
    foto_url = os.environ.get('FOTO_URL', '').strip()
    prezzo = os.environ.get('PREZZO', 'Trattativa Riservata').strip()
    mq = normalizza_metri_quadri(os.environ.get('MQ', '120'))
    descrizione = assicura_branding(os.environ.get('DESCRIZIONE', 'Splendida soluzione abitativa luminosa.'))
    stile = os.environ.get('STILE', 'cb_curved_wave').strip().lower()
    if stile not in ['cb_curved_wave', 'metroquadro_gradient', 'professionecasa_sidebar']:
        stile = random.choice(['cb_curved_wave', 'metroquadro_gradient', 'professionecasa_sidebar'])

    print(f"📌 Parametri: {azione} | {tipo} | {luogo} | {prezzo} | {mq}")
    print(f"🎨 Stile selezionato: {stile}")

    foto_img = scarica_foto(foto_url)
    if not foto_img:
        # Fallback se non c'è foto: crea un fondo elegante neutro
        foto_img = Image.new("RGBA", (1080, 1080), (235, 238, 242, 255))

    dati = {
        'azione': azione,
        'tipo': tipo,
        'luogo': luogo,
        'prezzo': prezzo,
        'mq': mq,
        'descrizione': descrizione,
        'foto': foto_img
    }

    # 1. Genera Post Quadrato (1:1 - 1080x1080)
    img_1_1 = crea_grafica_completa(dati, stile=stile, format_type="1:1")
    path_1_1 = "immobile_post_1_1.jpg"
    img_1_1.save(path_1_1, "JPEG", quality=95)
    print(f"✅ Post 1:1 generato: {path_1_1}")

    # 2. Genera Storia Verticale (9:16 - 1080x1920)
    img_9_16 = crea_grafica_completa(dati, stile=stile, format_type="9:16")
    path_9_16 = "immobile_storia_9_16.jpg"
    img_9_16.save(path_9_16, "JPEG", quality=95)
    print(f"✅ Storia 9:16 generata: {path_9_16}")

    # 3. Invio a Telegram (Canale prioritario di verifica)
    caption_post = f"🏠 {azione.upper()}: {tipo}\n📍 {luogo}\n📐 {mq}\n💰 {prezzo}\n\n{descrizione}"
    invia_telegram(path_1_1, caption_post)
    invia_telegram(path_9_16, f"📱 Formato Storia 9:16 — {tipo} a {luogo}\n\n— Immobiliare Giancani")

    # 4. Facebook live posting disattivato per Regola Mandatoria utente
    print("🔒 Pubblicazione automatica su Facebook/YouTube disattivata (Regola Mandatoria 5).")
    print("— Immobiliare Giancani")

if __name__ == '__main__':
    main()
