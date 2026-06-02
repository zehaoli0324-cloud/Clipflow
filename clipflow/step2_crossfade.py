"""
步骤 2: 将 6 段通过交叉淡入淡出合并为一条粗剪。
"""

import subprocess
import json
from config import TMP, ROUGH, FADE_DURATION, MERGE_CRF


def get_duration(path):
    r = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
                        "-show_format", str(path)],
                       capture_output=True, text=True, timeout=15)
    return float(json.loads(r.stdout)["format"]["duration"])


def run(cut_files: list) -> float:
    """返回粗剪时长（秒）。"""
    if len(cut_files) == 0:
        raise ValueError("No segments to merge")

    durs = [get_duration(f) for f in cut_files]
    inputs = []
    for f in cut_files:
        inputs.extend(["-i", str(f)])

    # 构建 xfade 滤镜链
    filter_chains = []
    cv, ca = "0:v", "0:a"
    cum = durs[0]

    for i in range(1, len(cut_files)):
        vlab, alab = f"v{i}", f"a{i}"
        off = max(0.0, cum - FADE_DURATION)
        filter_chains.append(
            f"[{cv}][{i}:v]xfade=transition=fade:"
            f"duration={FADE_DURATION}:offset={off}[{vlab}];"
            f"[{ca}][{i}:a]acrossfade=d={FADE_DURATION}[{alab}];"
        )
        cv, ca = vlab, alab
        cum = max(0.0, cum + durs[i] - FADE_DURATION)

    last_idx = len(cut_files) - 1
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", "".join(filter_chains),
        "-map", f"[v{last_idx}]", "-map", f"[a{last_idx}]",
        "-c:v", "libx264", "-preset", "fast", "-crf", MERGE_CRF,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(ROUGH),
    ]

    print(f"  Merging {len(cut_files)} segments with crossfade={FADE_DURATION}s...")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if r.returncode != 0 or not ROUGH.exists():
        raise RuntimeError(f"Step 2 failed: {r.stderr[:300]}")

    dur = get_duration(ROUGH)
    print(f"  ✅ Rough cut: {dur:.0f}s ({dur/60:.1f}min), "
          f"{ROUGH.stat().st_size / 1024 / 1024:.1f} MB")
    return dur


if __name__ == "__main__":
    from step1_cut import run as cut
    files = cut()
    run(files)
