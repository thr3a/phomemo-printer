from collections import namedtuple

from PIL import Image, ImageFont, ImageDraw

BitmapData = namedtuple("BitmapData", ["bitmap", "width", "height"])


def text_to_bitmap(text: str, fontsize: int) -> BitmapData:
    font = ImageFont.load_default(size=fontsize)
    image_width = 576
    image_height = int(fontsize * 1.5)

    # create image
    img = Image.new('1', (image_width, image_height), 0)
    draw = ImageDraw.Draw(img)

    # draw text
    draw.text((0, 0), text, font=font, fill=1)

    return BitmapData(img.tobytes(), image_width, image_height)
