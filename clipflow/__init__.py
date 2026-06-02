"""
clipflow — 通用竖版短视频剪辑工具
====================================

从任意长视频中提取精华片段，穿插动画卡，叠科技网格 Overlay，
输出 9:16 竖版短视频。全流程 Python + ffmpeg。

使用方法:
    1. 把源视频放到 downloads/
    2. 修改 config.py 中的 SEGMENTS、TITLE_*、ANIMATION_DATA
    3. python make.py

依赖:
    - Python 3.10+ (Pillow)
    - ffmpeg 6.0+ (xfade, boxblur)
    - 中文字体（config.py 中 FONT 配置）
    - [可选] Node.js + Remotion（用于重新渲染动画卡）
"""
