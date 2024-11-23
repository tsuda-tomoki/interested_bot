from PIL import Image, ImageDraw, ImageFont

def createpicture():
    imagecustom = Image.new("RGB", (512, 512), (256, 256, 256))
    imagedraw = ImageDraw.Draw(imagecustom)
    fontSize = ImageFont.truetype()