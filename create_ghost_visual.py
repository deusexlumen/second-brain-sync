from PIL import Image, ImageDraw, ImageFilter, ImageFont
import qrcode
import random

# Create QR code with high error correction for stylization
qr = qrcode.QRCode(
    version=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction allows stylization
    box_size=10,
    border=2,
)
qr.add_data('https://youtube.com/@k.i-mit-intention?si=fqDzlXyRJMKxvbAu')
qr.make(fit=True)

# Create QR image
qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

# Create abstract cybernetic background
width, height = qr_img.size
bg = Image.new('RGBA', (width + 100, height + 100), (0, 0, 0, 255))
draw = ImageDraw.Draw(bg)

# Add glitch lines
for i in range(0, height + 100, 4):
    if random.random() > 0.7:
        color = (255, 0, 50, 100) if random.random() > 0.5 else (255, 255, 255, 50)
        draw.line([(0, i), (width + 100, i)], fill=color, width=2)

# Add abstract shapes
for _ in range(20):
    x = random.randint(0, width + 100)
    y = random.randint(0, height + 100)
    size = random.randint(10, 50)
    color = (255, 0, 50, 80) if random.random() > 0.5 else (0, 255, 255, 60)
    draw.rectangle([x, y, x+size, y+size], fill=color)

# Add noise/glitch pixels
for _ in range(1000):
    x = random.randint(0, width + 100)
    y = random.randint(0, height + 100)
    color = (255, 255, 255, 100)
    draw.point((x, y), fill=color)

# Paste QR with blend
qr_pos = (50, 50)
bg.paste(qr_img, qr_pos, qr_img)

# Apply subtle glitch to QR area
qr_area = bg.crop((qr_pos[0], qr_pos[1], qr_pos[0] + qr_img.width, qr_pos[1] + qr_img.height))

# Add scan lines over QR
for i in range(0, qr_img.height, 6):
    draw.rectangle([
        qr_pos[0], qr_pos[1] + i,
        qr_pos[0] + qr_img.width, qr_pos[1] + i + 1
    ], fill=(0, 0, 0, 100))

# Add "corrupted" pixels randomly on QR
for _ in range(50):
    x = qr_pos[0] + random.randint(0, qr_img.width - 1)
    y = qr_pos[1] + random.randint(0, qr_img.height - 1)
    draw.rectangle([x, y, x+8, y+8], fill=(255, 0, 50, 150))

# Add text overlay
# try:
#     font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
# except:
#     font = ImageFont.load_default()
# 
# draw.text((20, 20), "SYSTEM_ANOMALY", fill=(255, 0, 50, 200), font=font)
# draw.text((20, height + 80), "TRACE: UNKNOWN", fill=(255, 0, 50, 200), font=font)

# Save
bg.save('/root/.openclaw/workspace/kimi_ghost_visual.png')
print("Created: /root/.openclaw/workspace/kimi_ghost_visual.png")
