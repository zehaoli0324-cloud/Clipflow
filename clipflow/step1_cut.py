"""
步骤 1: 从原片裁剪 6 段 — 高画质 + B站水印黑框遮盖。
"""

import subprocess
from config import VIDEO, TMP, SEGMENTS, CUT_PRESET, CUT_CRF, AUDIO_BITRATE


def run() -> list:
    """返回切割后的文件路径列表。"""
    TMP.mkdir(parents=True, exist_ok=True)
    cut_files = []

    for i, (start, end, label) in enumerate(SEGMENTS):
        duration = end - start
        out = TMP / f"seg-{i:02d}.mp4"
        print(f"  [{i+1}/{len(SEGMENTS)}] {label} ({duration:.0f}s)...")

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-i", str(VIDEO),
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", CUT_PRESET,
            "-crf", CUT_CRF,
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", AUDIO_BITRATE,
            "-vf", (
                "scale=1920:1080:force_original_aspect_ratio=decrease,"
                "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
                "drawbox=x=0:y=0:w=160:h=50:color=black@1.0:t=fill"
            ),
            "-movflags", "+faststart",
            str(out),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and out.exists():
            cut_files.append(out)
            print(f"    ✅ {out.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print(f"    ❌ Failed: {r.stderr[:200]}")
            raise RuntimeError(f"Step 1 failed at segment {i}")

    print(f"  ✅ 共 {len(cut_files)} 段")
    return cut_files


if __name__ == "__main__":
    run()
