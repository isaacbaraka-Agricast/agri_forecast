from PIL import Image, ImageDraw
import os

print("Creating app icons...")

# App Icon (512x512)
size = 512
icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(icon)

draw.ellipse([20, 20, size-20, size-20],
             fill='#2E8B2E', outline='#1A5C1A', width=8)

cx, cy = size//2, size//2
draw.rectangle([cx-12, cy+30, cx+12, cy+120], fill='white')
draw.ellipse([cx-100, cy-40, cx+10, cy+60], fill='white')
draw.ellipse([cx-95, cy-35, cx+5, cy+55], fill='#2E8B2E')
draw.ellipse([cx-10, cy-60, cx+100, cy+40], fill='white')
draw.ellipse([cx-5, cy-55, cx+95, cy+35], fill='#2E8B2E')
draw.ellipse([cx-35, cy-35, cx+35, cy+35], fill='white')
draw.ellipse([cx-25, cy-25, cx+25, cy+25], fill='#1A5C1A')
draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill='white')

os.makedirs('agri_mobile/assets', exist_ok=True)
icon.save('agri_mobile/assets/icon.png')
print("✅ App icon created!")

# Splash Screen (1080x1920)
splash = Image.new('RGB', (1080, 1920), '#1A5C1A')
draw2  = ImageDraw.Draw(splash)

for i in range(1920):
    draw2.line([(0, i), (1080, i)], fill=(0, 80, 0))

cx, cy = 540, 800
draw2.ellipse([cx-180, cy-180, cx+180, cy+180],
              fill='white', outline='#c8e6c8', width=4)
draw2.rectangle([cx-15, cy+20, cx+15, cy+110], fill='#2E8B2E')
draw2.ellipse([cx-90, cy-50, cx+20, cy+50],    fill='#2E8B2E')
draw2.ellipse([cx-20, cy-70, cx+90, cy+30],    fill='#2E8B2E')
draw2.ellipse([cx-30, cy-30, cx+30, cy+30],    fill='white')

draw2.text((cx, cy+260), 'AGRI FORECAST',
           fill='white', anchor='mm')
draw2.text((cx, cy+330), 'Musanze District, Rwanda',
           fill='#c8e6c8', anchor='mm')

splash.save('agri_mobile/assets/splash.png')
print("✅ Splash screen created!")
print("Both images saved to agri_mobile/assets/")