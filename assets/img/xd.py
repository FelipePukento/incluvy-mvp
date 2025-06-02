import qrcode
from PIL import Image, ImageDraw
import os

# URL del proyecto
url = "https://felipepukento.github.io/incluvy-mvp/"

# Configurar QR con corrección alta
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # hasta 30% de daño tolerado
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Generar QR base
qr_img = qr.make_image(fill_color="navy", back_color="white").convert("RGB")
qr_width, qr_height = qr_img.size

# Ruta al logo
logo_path = "assets/img/logo.png"
if not os.path.exists(logo_path):
    raise FileNotFoundError(f"No se encontró el logo en {logo_path}")

logo = Image.open(logo_path)

# Redimensionar logo
factor = 5  # más alto = logo más pequeño
logo_size = qr_width // factor
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# Crear un "hueco blanco" en el centro del QR
hole = Image.new("RGB", (logo_size, logo_size), "white")
hole_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
qr_img.paste(hole, hole_pos)

# Pegar el logo encima del hueco
if logo.mode in ("RGBA", "LA"):
    qr_img.paste(logo, hole_pos, mask=logo)
else:
    qr_img.paste(logo, hole_pos)

# Guardar resultado
output_file = "qr_incluvy_logo_clean.png"
qr_img.save(output_file)
print(f"✅ Código QR generado y guardado como: {output_file}")
