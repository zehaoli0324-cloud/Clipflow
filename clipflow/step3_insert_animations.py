"""
步骤 3: 将 8 张动画卡穿插到粗剪中 → 横向 16:9 完成版。
"""

import subprocess
from config import TMP, ROUGH, HORIZONTAL, ANIMATIONS, \
    INSERTION_POINTS, ANIM_FILES, ANIM_CRF, MERGE_CRF


def get_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of",
                        "default=noprint_wrappers=1:nokey=1", str(path)],
                       capture_output=True, text=True, timeout=10)
    return float(r.stdout.strip())


def run(rough_dur: float = None) -> float:
    """返回横向版时长。"""
    TMP.mkdir(parents=True, exist_ok=True)

    if rough_dur is None:
        rough_dur = get_duration(ROUGH)

    # 重编码动画卡 → 统一CRF
    aconv = []
    print(f"  Re-encoding {len(ANIM_FILES)} animations...")
    for i, aname in enumerate(ANIM_FILES):
        src = ANIMATIONS / aname
        dst = TMP / f"anim-{i:02d}.mp4"
        if not src.exists():
            raise FileNotFoundError(f"Animation not found: {src}")
        subprocess.run([
            "ffmpeg", "-y", "-i", str(src),
            "-c:v", "libx264", "-preset", "fast", "-crf", ANIM_CRF,
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", str(dst),
        ], capture_output=True, timeout=60)
        aconv.append(dst)

    # 在粗剪的插入点切割
    ups = sorted(set(INSERTION_POINTS))
    sps = [0.0] + ups + [rough_dur]  # 0.0, 39.0, 60.5, 76.0, 101.5, 122.0, rough_dur
    parts = []
    for i in range(len(sps) - 1):
        seg_len = sps[i + 1] - sps[i]
        if seg_len <= 0:
            continue
        dst = TMP / f"rp-{i:02d}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sps[i]), "-i", str(ROUGH),
            "-t", str(seg_len), "-c", "copy", str(dst),
        ], capture_output=True, timeout=60)
        parts.append(dst)

    # 映射：每个插入点对应的动画索引
    abp = {}
    for i, pt in enumerate(INSERTION_POINTS):
        pi = min(range(len(ups)), key=lambda j: abs(ups[j] - pt))
        abp.setdefault(pi, []).append(i)

    # 生成 concat 列表：part → (anim × N) → part → (anim × N) → ...
    concat_file = TMP / "concat.txt"
    with open(concat_file, "w") as f:
        for pi in range(len(parts)):
            f.write(f"file '{parts[pi].resolve()}'\n")
            if pi in abp:
                for ai in abp[pi]:
                    f.write(f"file '{aconv[ai].resolve()}'\n")

    # 合并
    print("  Concatenating rough cut + animations...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "fast", "-crf", MERGE_CRF,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(HORIZONTAL),
    ], capture_output=True, timeout=600)

    dur = get_duration(HORIZONTAL)
    print(f"  ✅ With animations: {dur:.0f}s ({dur/60:.1f}min), "
          f"{HORIZONTAL.stat().st_size / 1024 / 1024:.1f} MB")
    return dur


if __name__ == "__main__":
    run()
