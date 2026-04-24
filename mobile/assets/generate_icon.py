try:
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (1024, 1024), color='#0a0a1a')
    draw = ImageDraw.Draw(img)
    draw.ellipse([100,100,924,924], fill='#4f46e5')
    draw.text((512,512), "🏥", anchor="mm", fill="white")
    img.save('icon.png')
    img.resize((200,200)).save('splash-icon.png')
    img.resize((48,48)).save('favicon.png')
    print("✅ Icons created")
except:
    # بدون PIL — نسخ placeholder
    import urllib.request
    url = "https://via.placeholder.com/1024x1024/4f46e5/ffffff?text=AIHA"
    urllib.request.urlretrieve(url, "icon.png")
    urllib.request.urlretrieve(url, "splash-icon.png")
    print("✅ Icons downloaded")
