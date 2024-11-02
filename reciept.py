from PIL import Image, ImageDraw, ImageFont


def create_receipt():
    # マージンの設定
    MARGIN = 10
    WIDTH = 400

    # ロゴの設定
    logo = Image.open("logo.png")
    logo_size = 100
    logo = logo.resize((logo_size, logo_size))

    # フォントの設定
    font_path = "DotGothic16-Regular.ttf"
    title_font = ImageFont.truetype(font_path, 32)
    body_font = ImageFont.truetype(font_path, 20)

    # テキストの準備
    title_text = "来場証"
    body_text = """2024年11月03日（日）
池袋サンシャインシティ店

この度は sie; Lab を見ていただき
ありがとうございます。"""

    # テキストのサイズ計算
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1), "white"))
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    body_bbox = draw.textbbox((0, 0), body_text, font=body_font)

    # 画像の高さを計算
    height = (
        MARGIN * 2
        + logo_size
        + 20  # ロゴと題字の間隔
        + (title_bbox[3] - title_bbox[1])
        + 20  # 題字と本文の間隔
        + (body_bbox[3] - body_bbox[1])
        + MARGIN
    )

    # 画像を作成
    image = Image.new("RGB", (WIDTH, height), "white")
    draw = ImageDraw.Draw(image)

    # ロゴを配置
    logo_x = (WIDTH - logo_size) // 2
    current_y = MARGIN
    image.paste(logo, (logo_x, current_y))
    current_y += logo_size + 20

    # タイトルを配置
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_width) // 2
    draw.text((title_x, current_y), title_text, font=title_font, fill="black")
    current_y += (title_bbox[3] - title_bbox[1]) + 20

    # 本文を配置
    draw.text((MARGIN, current_y), body_text, font=body_font, fill="black")

    # 画像を保存
    image.save("receipt.png")


if __name__ == "__main__":
    create_receipt()
