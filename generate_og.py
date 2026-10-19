import os
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

font_dir = "C:/Windows/Fonts"
f_bold = os.path.join(font_dir, "segoeuib.ttf")
f_regular = os.path.join(font_dir, "segoeui.ttf")
f_semibold = os.path.join(font_dir, "seguisb.ttf") if os.path.exists(os.path.join(font_dir, "seguisb.ttf")) else f_bold

font_badge = ImageFont.truetype(f_bold, 16)
font_brand = ImageFont.truetype(f_bold, 20)
font_title_large = ImageFont.truetype(f_bold, 56)
font_title_sub = ImageFont.truetype(f_bold, 36)
font_desc1 = ImageFont.truetype(f_regular, 20)
font_desc2 = ImageFont.truetype(f_bold, 20)
font_pill = ImageFont.truetype(f_bold, 15)
font_footer = ImageFont.truetype(f_regular, 16)
font_footer_bold = ImageFont.truetype(f_bold, 17)
font_card_head = ImageFont.truetype(f_bold, 18)
font_card_sub = ImageFont.truetype(f_regular, 14)

# Canvas
img = Image.new("RGBA", (W, H), (9, 9, 11, 255))

# Gradient atmosphere
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g_draw = ImageDraw.Draw(glow)

# 1. Warm coral/orange glow (top-left)
for r in range(350, 0, -5):
    a = int(36 * (1 - r / 350))
    g_draw.ellipse([80 - r, 60 - r, 80 + r, 60 + r], fill=(224, 107, 57, a))

# 2. Violet/Purple glow (top-right/center)
for r in range(400, 0, -6):
    a = int(30 * (1 - r / 400))
    g_draw.ellipse([780 - r, 100 - r, 780 + r, 100 + r], fill=(155, 124, 240, a))

# 3. Cyan glow behind the right logo card
for r in range(320, 0, -5):
    a = int(35 * (1 - r / 320))
    g_draw.ellipse([980 - r, 280 - r, 980 + r, 280 + r], fill=(56, 189, 248, a))

# 4. Amber bottom glow
for r in range(260, 0, -5):
    a = int(22 * (1 - r / 260))
    g_draw.ellipse([260 - r, 540 - r, 260 + r, 540 + r], fill=(239, 164, 47, a))

img = Image.alpha_composite(img, glow)
draw = ImageDraw.Draw(img)

# Background dot matrix (only at edges/corners, avoiding text center)
for x in range(36, W, 36):
    for y in range(36, H, 36):
        # Skip center text area for clean contrast
        if (60 < x < 740 and 100 < y < 510) or (780 < x < 1140 and 60 < y < 520):
            continue
        draw.ellipse([x, y, x + 1.2, y + 1.2], fill=(255, 255, 255, 15))

# Outer subtle border frame
draw.rounded_rectangle([20, 20, W - 20, H - 20], radius=24, outline=(38, 38, 51, 255), width=1)
draw.rounded_rectangle([21, 21, W - 21, H - 21], radius=23, outline=(255, 255, 255, 10), width=1)
draw.line([(45, 550), (W - 45, 550)], fill=(38, 38, 51, 180), width=1)

# Helper function to draw checkmarks
def draw_check(d, cx, cy, col=(52, 211, 153, 255)):
    # Draws a neat vector checkmark centered around cx, cy
    points = [(cx - 6, cy), (cx - 2, cy + 5), (cx + 6, cy - 5)]
    d.line(points, fill=col, width=2)

# ---------------- LEFT COLUMN: TEXT CONTENT ----------------
left_x = 70

# 1. Top Badge: Admissions Open
badge_text = "ADMISSIONS OPEN · BATCH STARTS 26 OCT 2026"
badge_w = 445
badge_h = 34
badge_y = 56
draw.rounded_rectangle([left_x, badge_y, left_x + badge_w, badge_y + badge_h], radius=17,
                       fill=(21, 21, 28, 240), outline=(51, 51, 74, 255), width=1)
# Green pulse dot with glow
draw.ellipse([left_x + 12, badge_y + 10, left_x + 24, badge_y + 22], fill=(52, 211, 153, 60))
draw.ellipse([left_x + 14, badge_y + 12, left_x + 22, badge_y + 20], fill=(52, 211, 153, 255))
draw.text((left_x + 34, badge_y + 7), badge_text, font=font_badge, fill=(245, 245, 247, 240))

# 2. Company Brand Line
draw.text((left_x, 116), "MAXBRAIN TECHNOLOGIES", font=font_brand, fill=(239, 164, 47, 255))

# 3. Main Program Headline
draw.text((left_x, 152), "AI & ML ENGINEER", font=font_title_large, fill=(251, 146, 60, 255))
draw.text((left_x, 224), "Training + Live Internship Program", font=font_title_sub, fill=(196, 181, 253, 255))

# 4. Program Key Details
draw.text((left_x, 285), "12 Weeks (288 Hours) · Classroom in Jaipur & Live Online All India",
          font=font_desc2, fill=(255, 255, 255, 240))
draw.text((left_x, 318), "Learn Python, Deep Learning, PyTorch, LLMs, RAG & Autonomous Agents",
          font=font_desc1, fill=(175, 175, 190, 255))
draw.text((left_x, 348), "Phase 3: Work directly with product mentors on live AI applications",
          font=font_desc1, fill=(175, 175, 190, 255))

# 5. Key Highlights / Badges
pills = [
    ("Live AI Products", (194, 96, 58, 45), (224, 107, 57, 180), (253, 186, 116, 255)),
    ("Verifiable Certificates", (155, 124, 240, 45), (155, 124, 240, 180), (216, 180, 254, 255)),
    ("DPIIT-Recognised Startup", (52, 211, 153, 40), (52, 211, 153, 160), (110, 231, 183, 255)),
]

pill_x = left_x
pill_y = 405
for text, bg_col, border_col, txt_col in pills:
    bbox = font_pill.getbbox(text)
    pw = (bbox[2] - bbox[0]) + 28
    ph = 36
    draw.rounded_rectangle([pill_x, pill_y, pill_x + pw, pill_y + ph], radius=18,
                           fill=bg_col, outline=border_col, width=1)
    draw.text((pill_x + 14, pill_y + 8), text, font=font_pill, fill=txt_col)
    pill_x += pw + 12

# Feature points with neat vector checks
f_y = 468
# Feature 1
draw_check(draw, left_x + 8, f_y + 9)
draw.text((left_x + 22, f_y), "1:1 Mentorship", font=font_badge, fill=(220, 220, 230, 255))

# Feature 2
f2_x = left_x + 165
draw_check(draw, f2_x + 8, f_y + 9)
draw.text((f2_x + 22, f_y), "GPU & Cloud Credits", font=font_badge, fill=(220, 220, 230, 255))

# Feature 3
f3_x = left_x + 360
draw_check(draw, f3_x + 8, f_y + 9)
draw.text((f3_x + 22, f_y), "6-Month Placement Support", font=font_badge, fill=(220, 220, 230, 255))


# ---------------- RIGHT COLUMN: LOGO SHOWCASE CARD ----------------
card_w = 350
card_h = 440
card_x = 790
card_y = 60

# Glassmorphism Card
card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
card_draw = ImageDraw.Draw(card)

# Card background & border
card_draw.rounded_rectangle([0, 0, card_w - 1, card_h - 1], radius=22,
                            fill=(19, 19, 26, 235), outline=(51, 51, 74, 255), width=1)
# Top edge glow
card_draw.line([(24, 1), (card_w - 24, 1)], fill=(255, 255, 255, 50), width=1)

# Subtle inner card badge at top
card_badge = "OFFICIAL TRAINING DIVISION"
cb_bbox = font_card_sub.getbbox(card_badge)
cb_w = (cb_bbox[2] - cb_bbox[0]) + 20
cb_x = (card_w - cb_w) // 2
card_draw.rounded_rectangle([cb_x, 16, cb_x + cb_w, 38], radius=11,
                            fill=(26, 26, 36, 200), outline=(42, 42, 60, 255), width=1)
card_draw.text((card_w // 2, 27), card_badge, font=font_card_sub, fill=(163, 163, 178, 255), anchor="mm")

# Load and place MaxBrain 3D logo
logo_img = Image.open("logo.png").convert("RGBA")
logo_size = 230
logo_resized = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

# Paste logo centered horizontally in the card
logo_pos_x = (card_w - logo_size) // 2
logo_pos_y = 52
card.paste(logo_resized, (logo_pos_x, logo_pos_y), logo_resized)

# Divider line inside card
card_draw.line([(30, 305), (card_w - 30, 305)], fill=(36, 36, 50, 255), width=1)

# Card lower features
card_draw.text((card_w // 2, 332), "Classroom & Live Online", font=font_card_head,
               fill=(245, 245, 247, 255), anchor="mm")
card_draw.text((card_w // 2, 360), "Jaipur Office · Pan-India Remote Squads", font=font_card_sub,
               fill=(163, 163, 178, 255), anchor="mm")

# Govt Recognition Tag
rec_tag = "DPIIT-Recognised AI Startup · Govt. of India"
card_draw.text((card_w // 2, 400), rec_tag, font=font_card_sub,
               fill=(239, 164, 47, 255), anchor="mm")

# Composite card onto canvas
img.paste(card, (card_x, card_y), card)


# ---------------- BOTTOM FOOTER BAR ----------------
foot_y = 576
draw.text((left_x, foot_y), "https://training.maxbraintech.com", font=font_footer_bold, fill=(251, 146, 60, 255))
draw.text((left_x + 300, foot_y + 1), "•", font=font_footer, fill=(163, 163, 178, 180))
draw.text((left_x + 320, foot_y + 1), "MaxBrain Technologies Pvt. Ltd. · Jaipur, Rajasthan", font=font_footer, fill=(163, 163, 178, 255))

draw.text((W - 70, foot_y + 1), "info@maxbraintech.com", font=font_footer,
          fill=(212, 212, 222, 240), anchor="ra")

# Save as PNG (optimized) and JPG
final_rgb = img.convert("RGB")
final_rgb.save("og-image.png", "PNG", optimize=True)
final_rgb.save("og-image.jpg", "JPEG", quality=92, optimize=True)
print("Updated og-image.png and og-image.jpg successfully!")
