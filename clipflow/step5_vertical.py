"""
步骤 5: 最终合成 — 横向→竖版 + 背景模糊 + 水印 boxblur + 叠 Overlay。
"""

import subprocess
from config import TMP, HORIZONTAL, OVERLAY, FINAL, \
    FINAL_PRESET, FINAL_CRF, AUDIO_BITRATE, \
    WM_X, WM_Y, WM_W, WM_H


def run():
    """执行竖版转换 + 水印模糊 + Overlay 叠加，输出 final-v4.mp4。"""
    TMP.mkdir(parents=True, exist_ok=True)

    if not HORIZONTAL.exists():
        raise FileNotFoundError(f"Horizontal video not found: {HORIZONTAL}")
    if not OVERLAY.exists():
        raise FileNotFoundError(f"Overlay not found: {OVERLAY}")

    print("  Vertical conversion + watermark blur + overlay...")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(HORIZONTAL),
        "-i", str(OVERLAY),
        "-filter_complex", (
            "[0:v]split[fg][bg];"
            "[bg]scale=1920:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "boxblur=20:10,eq=brightness=-0.4[bg];"
            "[fg]scale=1080:-2:force_original_aspect_ratio=decrease[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2[vid];"
            "[vid]split[vid_main][vid_wm];"
            f"[vid_wm]crop={WM_W}:{WM_H}:{WM_X}:{WM_Y}[wm];"
            f"[wm]boxblur=10:5[wmblur];"
            f"[vid_main][wmblur]overlay={WM_X}:{WM_Y}[vid2];"
            "[vid2][1:v]overlay=0:0"
        ),
        "-c:v", "libx264", "-preset", FINAL_PRESET,
        "-crf", FINAL_CRF, "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", AUDIO_BITRATE,
        "-movflags", "+faststart",
        str(FINAL),
    ]

    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0 or not FINAL.exists():
        raise RuntimeError(f"Step 5 failed:\n{r.stderr[:500]}")

    # 验证
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(FINAL)],
        capture_output=True, text=True, timeout=10).stdout.strip())
    mb = FINAL.stat().st_size / 1024 / 1024
    print(f"  ✅ 完成: {dur:.0f}s ({dur/60:.1f}分), {mb:.1f} MB")


if __name__ == "__main__":
    run()
