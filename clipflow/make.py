"""
一键构建入口 — 依次执行 1→2→3→4→5 或指定步骤。

用法:
    python make.py              # 全流程
    python make.py --steps 1-3  # 只执行 1~3 步
    python make.py --steps 4    # 只执行第 4 步（需要现有中间产物）
    python make.py --cleanup    # 构建完成后清理 .tmp
    python make.py --render     # 先渲染动画卡，再全流程
"""

import sys
import argparse
import shutil

from config import SEGMENTS, TMP, OVERLAY
from step1_cut import run as step1
from step2_crossfade import run as step2
from step3_insert_animations import run as step3
from step4_overlay import run as step4
from step5_vertical import run as step5

# 动画卡渲染（可选）
try:
    from render_animations import run as render_animations
    HAS_ANIM_RENDERER = True
except ImportError:
    HAS_ANIM_RENDERER = False


def parse_steps(steps_arg: str) -> list:
    """解析 '1-5' → [1,2,3,4,5]; '1,3' → [1,3]; '4' → [4]"""
    steps = []
    for part in steps_arg.split(","):
        if "-" in part:
            a, b = part.split("-")
            steps.extend(range(int(a), int(b) + 1))
        else:
            steps.append(int(part))
    return sorted(set(steps))


def main():
    parser = argparse.ArgumentParser(
        description="clipflow — 通用竖版视频构建工具")
    parser.add_argument("--steps", default="1-5",
                        help="步骤范围, e.g. 1-5, 1,3, 4")
    parser.add_argument("--cleanup", action="store_true",
                        help="构建完成后清理 .tmp 目录")
    parser.add_argument("--render-animations", action="store_true",
                        help="先渲染 Remotion 动画卡")
    args = parser.parse_args()

    steps_to_run = parse_steps(args.steps)

    # 可选：渲染动画卡
    if args.render_animations:
        if HAS_ANIM_RENDERER:
            print("═══ [渲染动画卡] ═══")
            render_animations()
        else:
            print("⚠️  render_animations.py 未找到，跳过")

    print(f"═══ clipflow ═══")
    print(f"视频源: {SEGMENTS[0][0]}s → {SEGMENTS[-1][1]}s, 共 {len(SEGMENTS)} 段")
    print(f"执行步骤: {steps_to_run}")
    print()

    output = None  # 上游输出传递

    if 1 in steps_to_run:
        print("═══ 步骤 1: 裁剪 6 段 ═══")
        output = step1()
        print()

    if 2 in steps_to_run:
        print("═══ 步骤 2: 交叉淡入淡出 ═══")
        step2(output)
        print()

    if 3 in steps_to_run:
        print("═══ 步骤 3: 插入动画卡 ═══")
        step3()
        print()

    if 4 in steps_to_run:
        print("═══ 步骤 4: 生成 Overlay ═══")
        step4()
        print()

    if 5 in steps_to_run:
        print("═══ 步骤 5: 竖版合成 ═══")
        step5()
        print()

    # 清理
    if args.cleanup and TMP.exists():
        shutil.rmtree(TMP)
        print("🧹 .tmp 已清理")

    print("✅ 全部完成")


if __name__ == "__main__":
    main()
