# 🚀 Clip Forge

<div align="center">

### Turn Long Videos Into Viral Shorts

**2小时演讲 → 2分钟短视频**

无需 Premiere｜无需剪辑经验｜全自动工作流

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FFmpeg](https://img.shields.io/badge/FFmpeg-6.0+-green)
![License](https://img.shields.io/badge/License-MIT-orange)

</div>

---

## 🎬 What It Does

上传一段长视频：

* 黄仁勋发布会
* 播客访谈
* 在线课程
* 产品发布会
* 直播回放

Clip Forge 自动完成：

✅ 裁剪精华片段

✅ 转场衔接

✅ 插入动画信息卡

✅ 生成科技感标题

✅ 转换为 9:16 竖版

✅ 输出可直接发布的短视频

---

## ✨ Before vs After

### Input

```
2.5小时 Nvidia 发布会.mp4
```

↓

### Output

```
2分钟短视频.mp4

✔ 9:16 竖屏
✔ 动态标题
✔ 信息卡转场
✔ 平滑衔接
✔ 可直接发抖音/小红书
```

---

## 🔥 Example Workflow

```text
Long Video
    │
    ▼
┌─────────────┐
│  Clip Best  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Cross Fade  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ Anim Cards  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ AI Overlay  │
└─────────────┘
    │
    ▼
┌─────────────┐
│ 9:16 Short  │
└─────────────┘
```

---

## 🎯 Features

### Smart Highlight Assembly

从长视频中提取多个重点片段：

```python
SEGMENTS = [
    (120, 240, "AI Factory"),
    (800, 920, "Agent Future"),
    (1500, 1620, "Personal AI")
]
```

---

### Cinematic Transitions

自动添加：

* Crossfade
* Audio Fade
* Smooth Cut

无需手动调时间轴。

---

### Motion Information Cards

支持三种布局：

| Layout | 用途   |
| ------ | ---- |
| Split  | 金句强调 |
| Grid   | 参数展示 |
| Center | 核心观点 |

---

### Tech-style Overlay

自动生成：

* 科技网格
* 发光标题
* 边框设计
* 渐变背景

无需 PS。

---

### One-click Vertical Video

自动输出：

```text
1080 × 1920
30 FPS
H264
TikTok Ready
```

---

## ⚡ Quick Start

### Clone

```bash
git clone https://github.com/yourname/clipflow.git

cd clipflow
```

### Install

```bash
pip install Pillow

ffmpeg -version
```

### Configure

编辑：

```python
config.py
```

修改：

```python
SEGMENTS
TITLE1_TEXT
TITLE2_TEXT
TITLE3_TEXT
ANIMATION_DATA
```

### Run

```bash
python make.py
```

输出：

```text
output/final-v4.mp4
```

---

## 📂 Project Structure

```text
clipflow
│
├── config.py
├── make.py
│
├── step1_cut.py
├── step2_crossfade.py
├── step3_insert_animations.py
├── step4_overlay.py
├── step5_vertical.py
│
├── render_animations.py
│
├── downloads/
└── output/
```

---

## 🏗 Architecture

```text
Video
 │
 ▼
Cut Segments
 │
 ▼
Crossfade
 │
 ▼
Insert Animations
 │
 ▼
Generate Overlay
 │
 ▼
Vertical Render
 │
 ▼
Final Short Video
```

---

## 💡 Why I Built This

我发现很多人拥有：

* 播客内容
* 课程录屏
* 直播回放
* 发布会录像

但短视频剪辑耗时太长。

于是写了一个：

> **把长视频变成短视频流水线的自动化工具。**

整个项目：

* Python
* FFmpeg
* Pillow
* Remotion

没有 Premiere。

没有 AE。

没有复杂时间轴。

---

## ⭐ Roadmap

* [ ] Whisper 自动字幕
* [ ] GPT 自动生成标题
* [ ] AI 自动提取高光片段
* [ ] BGM 自动匹配
* [ ] 多模板主题
* [ ] TikTok 自动发布

---

## 🤝 Contributing

欢迎：

* PR
* Feature Request
* Bug Report

如果这个项目对你有帮助：

⭐ Star 一下仓库

---
