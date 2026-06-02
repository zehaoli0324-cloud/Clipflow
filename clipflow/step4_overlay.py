"""
步骤 4: 生成 Overlay — 白色科技网格 + 三行标题 + 金色边线 + 暗色渐变。
输出 1080×1920 RGBA PNG。
"""

from PIL import Image, ImageDraw, ImageFont
from config import (
    TMP, OVERLAY, FONT,
    W, H, VID_TOP, VID_BOT,
    TITLE1_TEXT, TITLE1_FONT, TITLE1_Y, TITLE1_COLOR,
    TITLE2_TEXT, TITLE2_FONT, TITLE2_Y, TITLE2_COLOR,
    TITLE3_TEXT, TITLE3_FONT, TITLE3_Y, TITLE3_COLOR,
    BOTTOM_TEXT, BOTTOM_FONT, BOTTOM_Y_OFFSET,
    GRID_SPACING, GRID_MAJOR_WIDTH, GRID_MAJOR_OPACITY,
    GRID_MINOR_WIDTH, GRID_MINOR_OPACITY,
    GRID_VERT_WIDTH, GRID_VERT_OPACITY,
    GRADIENT_HEIGHT, GRADIENT_MAX_ALPHA,
    GOLD_ACCENT_WIDTH, GOLD_ACCENT_OPACITY,
)

G = (245, 166, 35, 255)   # 金色
WHT = (255, 255, 255)


def bd(dr, xy, text, font, fill):
    """加粗描边——在 (x,y) 周围 ±2px 范围重复绘制。"""
    x, y = xy
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            dr.text((x + dx, y + dy), text, fill=fill, font=font)


def run():
    TMP.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)

    # ─── 字体 ───────────────────────────────
    ft1 = ImageFont.truetype(FONT, TITLE1_FONT)
    ft2 = ImageFont.truetype(FONT, TITLE2_FONT)
    ft3 = ImageFont.truetype(FONT, TITLE3_FONT)
    ft4 = ImageFont.truetype(FONT, BOTTOM_FONT)

    # ─── 网格（仅覆盖视频框外的上下区域） ────
    # 横线
    for y in range(0, VID_TOP, GRID_SPACING):
        is_major = y % (GRID_SPACING * 2) == 0
        w = GRID_MAJOR_WIDTH if is_major else GRID_MINOR_WIDTH
        opacity = GRID_MAJOR_OPACITY if is_major else GRID_MINOR_OPACITY
        dr.line([(0, y), (W, y)], fill=(*WHT, opacity), width=w)
    for y in range(VID_BOT, H, GRID_SPACING):
        offset = y - VID_BOT
        is_major = offset % (GRID_SPACING * 2) == 0
        w = GRID_MAJOR_WIDTH if is_major else GRID_MINOR_WIDTH
        opacity = GRID_MAJOR_OPACITY if is_major else GRID_MINOR_OPACITY
        dr.line([(0, y), (W, y)], fill=(*WHT, opacity), width=w)

    # 纵线
    for x in range(0, W, GRID_SPACING):
        dr.line([(x, 0), (x, VID_TOP)], fill=(*WHT, GRID_VERT_OPACITY), width=GRID_VERT_WIDTH)
        dr.line([(x, VID_BOT), (x, H)], fill=(*WHT, GRID_VERT_OPACITY), width=GRID_VERT_WIDTH)

    # ─── 暗色渐变（提高标题可读性） ──────────
    for y in range(GRADIENT_HEIGHT):
        a = int(GRADIENT_MAX_ALPHA * (1 - y / GRADIENT_HEIGHT))
        dr.rectangle([(0, VID_TOP - GRADIENT_HEIGHT + y),
                      (W, VID_TOP - GRADIENT_HEIGHT + y)], fill=(0, 0, 0, a))

    # ─── 金色边线 ───────────────────────────
    for lx, ly, lw, lh in [
        (3, 0, GOLD_ACCENT_WIDTH, VID_TOP),          # 左上竖条
        (W - GOLD_ACCENT_WIDTH - 3, 0, GOLD_ACCENT_WIDTH, VID_TOP),  # 右上竖条
        (3, VID_BOT, GOLD_ACCENT_WIDTH, H - VID_BOT),  # 左下竖条
        (W - GOLD_ACCENT_WIDTH - 3, VID_BOT, GOLD_ACCENT_WIDTH, H - VID_BOT),  # 右下竖条
    ]:
        dr.rectangle([(lx, ly), (lx + lw - 1, ly + lh - 1)], fill=(*G[:3], GOLD_ACCENT_OPACITY))

    # ─── 三行标题 ───────────────────────────
    b1 = dr.textbbox((0, 0), TITLE1_TEXT, font=ft1)
    bd(dr, ((W - (b1[2] - b1[0])) // 2, TITLE1_Y), TITLE1_TEXT, ft1, TITLE1_COLOR)

    b2 = dr.textbbox((0, 0), TITLE2_TEXT, font=ft2)
    bd(dr, ((W - (b2[2] - b2[0])) // 2, TITLE2_Y), TITLE2_TEXT, ft2, TITLE2_COLOR)

    b3 = dr.textbbox((0, 0), TITLE3_TEXT, font=ft3)
    dr.text(((W - (b3[2] - b3[0])) // 2, TITLE3_Y), TITLE3_TEXT,
            fill=TITLE3_COLOR, font=ft3)

    # ─── 底部文案 ───────────────────────────
    b4 = dr.textbbox((0, 0), BOTTOM_TEXT, font=ft4)
    dr.text(((W - (b4[2] - b4[0])) // 2, H - BOTTOM_Y_OFFSET),
            BOTTOM_TEXT, fill=(*WHT, 150), font=ft4)

    # ─── 保存 ───────────────────────────────
    img.save(str(OVERLAY))
    print(f"  ✅ Overlay: {OVERLAY.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    run()
