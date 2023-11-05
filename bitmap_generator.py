from collections import namedtuple

from PIL import Image, ImageFont, ImageDraw, ImageOps

from PhomemoM02Pro_constants import DOT_PER_LINE

BitmapData = namedtuple("BitmapData", ["bitmap", "width", "height"])


def text_to_bitmap(text: str, fontsize: int) -> BitmapData:
    font = ImageFont.load_default(size=fontsize)
    image_width = DOT_PER_LINE
    image_height = int(fontsize * 1.5)

    # create image
    img = Image.new('1', (image_width, image_height), 0)
    draw = ImageDraw.Draw(img)

    # draw text
    draw.text((0, 0), text, font=font, fill=1)

    return BitmapData(img.tobytes(), image_width, image_height)


def img_to_bitmap(img_path: str) -> BitmapData:
    img = Image.open(img_path)

    # image width is fixed to 576dots
    # calculate image height to keep aspect ratio
    image_width = DOT_PER_LINE
    image_height = int(image_width / img.width * img.height)

    # resize & dithering
    img = img.resize((image_width, image_height))
    img = img.convert('1', dither=Image.FLOYDSTEINBERG)

    # invert image, because printer prints 1 as black
    img = ImageOps.invert(img)

    return BitmapData(img.tobytes(), image_width, image_height)
