from dataclasses import dataclass
from typing import Tuple, List
from PIL import Image, ImageDraw, ImageFont
import random

# 定数の定義
@dataclass(frozen=True)
class ImageConfig:
    WIDTH: int = 400
    MARGIN: int = 10
    LOGO_SIZE: int = 128
    FONT_PATH: str = "DotGothic16-Regular.ttf"

@dataclass(frozen=True)
class FontSizes:
    TITLE: int = 32
    BODY: int = 20
    FORTUNE_TITLE: int = 20
    FORTUNE_RESULT: int = 40

# カスタム型の定義
Coordinate = Tuple[int, int]
BoundingBox = Tuple[int, int, int, int]

def load_fonts(font_path: str) -> Tuple[ImageFont.FreeTypeFont, ...]:
    """フォントの読み込み"""
    sizes = FontSizes()
    return (
        ImageFont.truetype(font_path, sizes.TITLE),
        ImageFont.truetype(font_path, sizes.BODY),
        ImageFont.truetype(font_path, sizes.FORTUNE_TITLE),
        ImageFont.truetype(font_path, sizes.FORTUNE_RESULT)
    )

def get_random_fortune() -> Tuple[str, str]:
    """おみくじの結果とラッキーアイテムをランダムに選択"""
    omikuji_results = ['大吉', '中吉', '吉', '小吉', '末吉']
    lucky_items = ['エビフライ', '中古車', 'ペンギン', '技術書']
    return random.choice(omikuji_results), random.choice(lucky_items)

def calculate_text_bbox(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont
) -> BoundingBox:
    """テキストの境界ボックスを計算"""
    return draw.textbbox((0, 0), text, font=font)

def get_centered_x(text_width: int, image_width: int) -> int:
    """テキストを中央揃えにするためのX座標を計算"""
    return (image_width - text_width) // 2

def draw_text_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    font: ImageFont.FreeTypeFont,
    image_width: int
) -> int:
    """中央揃えでテキストを描画し、次の Y 座標を返す"""
    bbox = calculate_text_bbox(draw, text, font)
    text_width = bbox[2] - bbox[0]
    x = get_centered_x(text_width, image_width)
    draw.text((x, y), text, font=font, fill="black")
    return y + (bbox[3] - bbox[1])

def create_receipt() -> None:
    """来場証の画像を生成"""
    config = ImageConfig()
    omikuji, lucky_item = get_random_fortune()
    
    # フォントの読み込み
    title_font, body_font, fortune_title_font, fortune_result_font = load_fonts(config.FONT_PATH)

    # テキストの準備
    texts = {
        'title': "来場証",
        'body': """2024年11月03日（日）
池袋サンシャインシティ店

この度は sie; Lab にご訪問いただき
ありがとうございます。""",
        'fortune_title': "☆ 今日の運勢 ☆",
        'lucky_item': f"ラッキーアイテム: {lucky_item}"
    }

    # テキストのサイズ計算用の一時的な描画オブジェクト
    temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1), "white"))
    
    # 各テキストの境界ボックスを計算
    bboxes = {
        'title': calculate_text_bbox(temp_draw, texts['title'], title_font),
        'body': calculate_text_bbox(temp_draw, texts['body'], body_font),
        'fortune_title': calculate_text_bbox(temp_draw, texts['fortune_title'], fortune_title_font),
        'fortune_result': calculate_text_bbox(temp_draw, omikuji, fortune_result_font),
        'lucky_item': calculate_text_bbox(temp_draw, texts['lucky_item'], body_font)
    }

    # 画像の高さを計算
    height = sum([
        config.MARGIN * 2,
        config.LOGO_SIZE,
        20,
        bboxes['title'][3] - bboxes['title'][1],
        20,
        bboxes['body'][3] - bboxes['body'][1],
        20,
        bboxes['fortune_title'][3] - bboxes['fortune_title'][1],
        10,
        bboxes['fortune_result'][3] - bboxes['fortune_result'][1],
        30,
        bboxes['lucky_item'][3] - bboxes['lucky_item'][1],
        config.MARGIN * 8
    ])

    # 画像の作成と描画
    image = Image.new("RGB", (config.WIDTH, height), "white")
    draw = ImageDraw.Draw(image)

    # ロゴの配置
    logo = Image.open("logo.png").resize((config.LOGO_SIZE, config.LOGO_SIZE))
    logo_x = get_centered_x(config.LOGO_SIZE, config.WIDTH)
    current_y = config.MARGIN
    image.paste(logo, (logo_x, current_y))
    current_y += config.LOGO_SIZE + 20

    # 各テキストの描画
    current_y = draw_text_centered(draw, texts['title'], current_y, title_font, config.WIDTH) + 20
    draw.text((config.MARGIN, current_y), texts['body'], font=body_font, fill="black")
    current_y += (bboxes['body'][3] - bboxes['body'][1]) + 20
    current_y = draw_text_centered(draw, texts['fortune_title'], current_y, fortune_title_font, config.WIDTH) + 10
    current_y = draw_text_centered(draw, omikuji, current_y, fortune_result_font, config.WIDTH) + 30
    draw.text((config.MARGIN, current_y), texts['lucky_item'], font=body_font, fill="black")

    # 画像の保存
    image.save("receipt.png")

if __name__ == "__main__":
    create_receipt()
