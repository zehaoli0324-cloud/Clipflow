"""
渲染 Remotion 动画卡。
从 config.py 读取 ANIMATION_DATA 进行渲染。

前置条件:
    - Node.js + Remotion 已安装
    - REMOTION_DIR 项目存在且已 npm install
    - src/NvidiaCard/ 组件存在
"""

import json
import subprocess
import sys
from pathlib import Path

from config import REMOTION_DIR, OUTPUT_DIR, ANIMATION_DATA

ANIM_DIR = OUTPUT_DIR / "animations"
ANIM_DIR.mkdir(parents=True, exist_ok=True)


def run():
    """渲染全部动画卡。"""
    if not (REMOTION_DIR / "node_modules").exists():
        print(f"⚠️  Remotion 项目未安装依赖，运行: cd {REMOTION_DIR} && npm install")
        return

    for i, anim in enumerate(ANIMATION_DATA, 1):
        out = ANIM_DIR / f"anim-ch-{i:02d}.mp4"
        props = json.dumps(anim, ensure_ascii=False)

        print(f"  [{i}/{len(ANIMATION_DATA)}] {anim['title']}...")
        r = subprocess.run([
            "npx", "remotion", "render",
            "src/index.ts", "NvidiaCard", str(out),
            "--props", props, "--log", "error",
        ], cwd=str(REMOTION_DIR), capture_output=True, text=True, timeout=600)

        if r.returncode == 0 and out.exists():
            print(f"    ✅ {out.name} ({out.stat().st_size / 1024 / 1024:.1f} MB)")
        else:
            print(f"    ❌ 失败: {r.stderr[:300]}")
            return

    print(f"  ✅ 全部 {len(ANIMATION_DATA)} 张动画卡已渲染")


if __name__ == "__main__":
    run()
