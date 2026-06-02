"""
clipflow — 通用竖版短视频剪辑工具
====================================

从任意长视频中提取精华片段，穿插动画卡，叠科技网格 Overlay，
输出 9:16 竖版短视频。全流程 Python + ffmpeg。

使用方法:
    1. 将源视频放到 downloads/ 目录
    2. 修改下方 SEGMENTS、TITLE_*、ANIMATIONS 为你自己的内容
    3. python make.py

所有路径都基于项目目录自动解析，开箱即用。
"""

from pathlib import Path

# ══════════════════════════════════════════════
# 项目目录（自动检测，不要改）
# ══════════════════════════════════════════════
PROJECT = Path(__file__).parent.resolve()
DOWNLOADS = PROJECT / "downloads"
OUTPUT = PROJECT / "output"
OUTPUT_DIR = OUTPUT  # 供 render_animations 使用
TMP = OUTPUT / ".tmp"
ANIMATIONS = OUTPUT / "animations"
SCRIPTS = PROJECT / "scripts"

# ══════════════════════════════════════════════
# ★ 你要改的配置从这里开始 ★
# ══════════════════════════════════════════════

# ── 源视频 ────────────────────────────────────
# 把视频放到 downloads/ 目录，改文件名即可
VIDEO = DOWNLOADS / "your_video.mp4"

# ── 裁剪片段 ──────────────────────────────────
# 格式: (开始秒数, 结束秒数, 描述文字)
# 示例: (120.0, 140.0, "演讲开场")
SEGMENTS = [
    (220.0, 235.0,   "片段 1"),
    (400.0, 425.0,   "片段 2"),
    (1513.0, 1535.0, "片段 3"),
    (2244.0, 2260.0, "片段 4"),
    (2832.0, 2858.0, "片段 5"),
    (5047.0, 5068.0, "片段 6"),
]

# ── 视频参数 ──────────────────────────────────
W, H = 1080, 1920           # 输出分辨率 9:16
VID_TOP = 656                # 视频区域上沿 (1080p 居中)
VID_BOT = 1264               # 视频区域下沿
FADE_DURATION = 0.5          # 片段间淡入淡出(秒)

# ── 动画卡插入位置 ────────────────────────────
# 在粗剪中的秒数位置。成对 = 该点连续插两张
INSERTION_POINTS = [39.0, 39.0, 60.5, 60.5, 76.0, 101.5, 101.5, 122.0]

# 动画卡文件名（按插入顺序，output/animations/ 下）
ANIM_FILES = [
    "anim-ch-01.mp4",
    "anim-ch-02.mp4",
    "anim-ch-04.mp4",
    "anim-ch-06.mp4",
    "anim-ch-05.mp4",
    "anim-ch-08.mp4",
    "anim-ch-03.mp4",
    "anim-ch-07.mp4",
]

# ── 编码品质 ──────────────────────────────────
CUT_PRESET = "fast"       # 切段编码速度
CUT_CRF = "20"            # 画质 (18=无损, 23=默认, 28=小文件)
ANIM_CRF = "18"           # 动画卡画质
MERGE_CRF = "20"          # 合并画质
FINAL_CRF = "20"          # 最终画质
FINAL_PRESET = "veryfast" # 最终编码速度（boxblur 慢，用 veryfast）
AUDIO_BITRATE = "128k"

# ── 输出文件名 ────────────────────────────────
FINAL = OUTPUT / "final-v4.mp4"
ROUGH = TMP / "rough.mp4"
HORIZONTAL = TMP / "horizontal.mp4"
OVERLAY = TMP / "overlay.png"

# ══════════════════════════════════════════════
# ★ Overlay 视觉参数（改这里控制标题和网格）
# ══════════════════════════════════════════════

# 中文字体路径（Windows 可改为 C:/Windows/Fonts/msyh.ttc）
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

# ── 三行标题 ──────────────────────────────────
TITLE1_TEXT = "主标题"          # 最大字，金色描边
TITLE1_FONT = 80               # 字号
TITLE1_Y = 460                 # Y 坐标（基线）
TITLE1_COLOR = (245, 166, 35, 255)  # 金色

TITLE2_TEXT = "副标题"          # 中等字，白色描边
TITLE2_FONT = 60
TITLE2_Y = 550
TITLE2_COLOR = (255, 255, 255, 255)

TITLE3_TEXT = "关键词一 · 关键词二 · 关键词三"
TITLE3_FONT = 44
TITLE3_Y = 620
TITLE3_COLOR = (255, 193, 69, 240)  # 亮金

BOTTOM_TEXT = ""                # 底部文字（留空则不显示）
BOTTOM_FONT = 26
BOTTOM_Y_OFFSET = 100

# ── 背景网格 ──────────────────────────────────
GRID_SPACING = 80
GRID_MAJOR_WIDTH = 5
GRID_MAJOR_OPACITY = 70
GRID_MINOR_WIDTH = 3
GRID_MINOR_OPACITY = 50
GRID_VERT_WIDTH = 2
GRID_VERT_OPACITY = 45

GRADIENT_HEIGHT = 280           # 顶部暗色渐变高度(px)
GRADIENT_MAX_ALPHA = 230        # 渐变最暗处不透明度

GOLD_ACCENT_WIDTH = 5           # 金色边线宽度
GOLD_ACCENT_OPACITY = 60

# ── 水印模糊 ──────────────────────────────────
WM_X = 0
WM_Y = 674
WM_W = 250
WM_H = 55

# ══════════════════════════════════════════════
# ★ 动画卡内容（用于 Remotion 重新渲染）
# ══════════════════════════════════════════════
REMOTION_DIR = Path.home() / "remotion-github"  # Remotion 项目路径
REMOTION_COMPOSITION = "NvidiaCard"
REMOTION_FPS = 30
REMOTION_DURATION_FRAMES = 150

# 每张卡的标题、副标题、高亮文案
ANIMATION_DATA = [
    {"title": "卡1",    "subtitle": "副标题1",      "accent": "高亮语1",     "label": "标签1",  "variant": "split"},
    {"title": "卡2",    "subtitle": "副标题2",      "accent": "高亮语2",     "label": "标签2",  "variant": "split"},
    {"title": "卡3",    "subtitle": "副标题3",      "accent": "高亮语3",     "label": "标签3",  "variant": "split"},
    {"title": "卡4",    "subtitle": "副标题4",      "accent": "高亮语4",     "label": "标签4",  "variant": "split"},
    {"title": "卡5",    "subtitle": "副标题5",      "accent": "高亮语5",     "label": "标签5",  "variant": "split"},
    {"title": "卡6",    "subtitle": "副标题6",      "accent": "高亮语6",     "label": "标签6",  "variant": "grid",
     "specs": ["参数1", "参数2", "参数3", "参数4", "参数5"]},
    {"title": "卡7",    "subtitle": "副标题7",      "accent": "高亮语7",     "label": "标签7",  "variant": "grid",
     "specs": ["参数1", "参数2", "参数3", "参数4", "参数5"]},
    {"title": "卡8",    "subtitle": "副标题8",      "accent": "高亮语8",     "label": "标签8",  "variant": "center"},
]
