# 🖼️ Image Combiner

An elegant, lightweight Python GUI utility built with Tkinter and Pillow that allows you to easily combine multiple images into a single, perfectly proportioned, custom-resolution canvas. 

The application is engineered with a **smart layout engine** that automatically structures a grid based on your target aspect ratio and image count. It uses a **center-crop scale** to fit images cleanly without unsightly black bars or empty spaces.

---

## ✨ Features

* **📷 Multi-Format Image Support:** Upload standard formats including PNG, JPG, JPEG, BMP, WEBP, and TIFF.
* **🔄 Easy Reordering:** Order is everything! Move images up and down with simple button controls to prioritize which image takes key positions.
* **📐 Smart Grid Distribution:** 
  * Automatically calculates the ideal rows and columns according to your target dimensions to ensure cell aspect ratios are as balanced (square-like) as possible.
  * Dynamically handles **odd numbers of images** by making specific cells larger so there are no empty gaps.
* **✂️ Intelligent Crop-to-Fit:** Center-crops all source images to perfectly fill their respective grid cells. No squishing, stretching, or letterboxing!
* **🎛️ Dynamic Borders / Gaps:** 
  * Adjust spacing between images (and the outer canvas borders) using an interactive slider (0 to 80 pixels).
  * Customize the gap color instantly using a built-in visual color picker.
* **⚡ Preconfigured Presets:** Use popular target size resolutions directly:
  * `1024 × 1024` (Square)
  * `1024 × 2048` (Portrait 1:2)
  * `2048 × 1024` (Landscape 2:1)
  * `1024 × 1536` (Portrait 2:3)
  * `1536 × 1024` (Landscape 3:2)
  * ...or define your own **Custom** dimensions!
* **👁️ Interactive Preview:** Real-time generation of scaled previews in the application before saving.

---

## 🛠️ Installation & Setup

Ensure you have **Python 3.10+** installed on your system.

1. Clone or navigate to the project directory:
   ```bash
   cd "c:\Projeler\ImageCombine"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application:
   ```bash
   python main.py
   ```

---

## 🚀 How to Use

1. **Add Images:** Click **Add Images** to load your photos. They will populate the list with indices.
2. **Arrange the Order:** Select an item in the list and use the **▲ Up** and **▼ Down** buttons to organize them.
3. **Configure Canvas:**
   * Select a resolution preset or set a custom width/height.
   * Fine-tune the **Gap / Border** slider.
   * Click the color swatch next to **Gap Colour** to choose a custom background border color.
4. **Generate & Preview:** Click the **🔄 Preview** button to verify the layout distribution and cropping.
5. **Save:** When satisfied, click **💾 Combine & Save** to export the result in your format of choice (PNG, JPEG, WEBP, BMP).

---

## 📂 Project Structure

```
c:\Projeler\ImageCombine\
├── main.py              # Main entry point for the application
├── gui.py               # Tkinter user interface & event handling
├── layout_engine.py     # Grid math & pixel-perfect coordinate distribution
├── combiner.py          # Image resizing, cropping, & PIL canvas compositing
├── requirements.txt     # Python package dependencies (Pillow)
└── README.md            # You are here!
```

---

## 🎨 Layout Distribution Logic

```
For Even Counts (e.g., 4 Images)         For Odd Counts (e.g., 3 Images)
┌───────────┬───────────┐                ┌───────────────────────┐
│           │           │                │                       │
│  Image 1  │  Image 2  │                │        Image 1        │
│           │           │                │                       │
├───────────┼───────────┤                ├───────────┬───────────┤
│           │           │                │           │           │
│  Image 3  │  Image 4  │                │  Image 2  │  Image 3  │
│           │           │                │           │           │
└───────────┴───────────┘                └───────────┴───────────┘
```
The algorithm evaluates layout factorizations to minimize distortions while ensuring a solid edge-to-edge finish. The **first item** in the list gets prioritized with larger real estate during odd splits.
