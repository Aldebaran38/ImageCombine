# Image Combiner

A lightweight Python GUI tool built with Tkinter and Pillow for combining multiple images into a single, custom-resolution canvas.

It uses a grid layout algorithm that automatically arranges images based on your target aspect ratio and image count, utilizing center-cropping to fit each image cleanly without distortion or empty gaps.

---

## Features

* **Broad Format Support:** Works with PNG, JPG, JPEG, BMP, WEBP, and TIFF.
* **Easy Reordering:** Arrange image order with Up and Down buttons to control where each image is placed in the grid.
* **Smart Grid Distribution:**
  * Calculates the optimal rows and columns based on target canvas dimensions to keep cell ratios balanced.
  * Handles odd numbers of images cleanly by scaling specific cells to prevent empty gaps.
* **Intelligent Center-Cropping:** Automatically center-crops images to fill their grid cell without stretching or distorting.
* **Adjustable Borders & Gaps:**
  * Add spacing between images (0 to 80px border/gap size) via a slider.
  * Pick any background/gap color with a color picker.
* **Canvas Presets & Custom Sizes:** Pre-configured sizes (Square, Portrait, Landscape) and full support for custom width/height inputs.
* **Real-time Preview:** Generate and inspect a scaled layout preview before exporting.

---

## Installation & Setup

Requires **Python 3.10+**.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Aldebaran38/ImageCombine.git
   cd ImageCombine
   ```

2. **Install dependencies:**
   *(Optional if using the start scripts, which install dependencies automatically)*
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start Scripts
The project includes startup scripts that verify Python, check/install dependencies, and start the app:

* **Windows:** Double-click `start.bat` or run:
  ```cmd
  start.bat
  ```
* **Linux / macOS:** Make `start.sh` executable and run it:
  ```bash
  chmod +x start.sh
  ./start.sh
  ```

You can also run the app manually:
```bash
python main.py
```

---

## How to Use

1. **Add Images:** Click **Add Images** to load your files.
2. **Arrange Order:** Select an image from the list and use the **▲ Up** and **▼ Down** buttons to position it.
3. **Configure Canvas:**
   * Choose a resolution preset or enter custom dimensions.
   * Adjust the spacing between images using the **Gap / Border** slider.
   * Click the color box next to **Gap Colour** to change the background border color.
4. **Preview:** Click **Preview** to generate a scaled layout preview.
5. **Save:** Click **Combine & Save** to export the final image (supports PNG, JPEG, WEBP, and BMP).



<img width="640" height="494" alt="Image Combiner UI" src="https://github.com/user-attachments/assets/1af0e9e3-6d72-429f-912c-59348e338318" />

---

## Building Standalone Executables

You can compile the application into a single portable executable that runs without a Python installation. 

*Note: You must build on the target OS (e.g. build on Windows for `.exe`, Linux for the Linux binary).*

* **Windows:** Run `build.bat` (or double-click it):
  ```cmd
  build.bat
  ```
  Output: `dist\ImageCombiner.exe`

* **Linux:** Run `build.sh`:
  ```bash
  chmod +x build.sh
  ./build.sh
  ```
  Output: `dist/ImageCombiner`

The build scripts automatically check for and install `PyInstaller` and `Pillow` if needed.

---

## Project Structure

```
ImageCombine/
├── main.py              # Main entry point for the application
├── gui.py               # Tkinter user interface & event handling
├── layout_engine.py     # Grid math & pixel-perfect coordinate distribution
├── combiner.py          # Image resizing, cropping, & PIL canvas compositing
├── icon.png             # Application icon (embedded in the .exe)
├── requirements.txt     # Python package dependencies (Pillow)
├── start.bat            # Windows dev startup script (with console for debugging)
├── start.sh             # Linux dev startup script
├── build.bat            # Windows build script → produces dist\ImageCombiner.exe
├── build.sh             # Linux build script   → produces dist/ImageCombiner
├── .gitignore           # Ignores build outputs, caches, etc.
└── README.md            # You are here!
```

---

## Layout Distribution Logic

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
The grid algorithm calculates factor combinations to minimize layout distortion. For odd counts, the first image is given a larger layout share to keep the layout complete and balanced.
