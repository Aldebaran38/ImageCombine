"""
Image Combiner — Tkinter GUI.
Upload images, reorder them, configure output settings, and combine.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox

from PIL import Image, ImageTk

from combiner import combine_images


def _resource_path(relative_path: str) -> str:
    """Get the absolute path to a resource, works for dev and PyInstaller."""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS          # PyInstaller temp folder
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)

# ── Resolution presets ────────────────────────────────────────────────
PRESETS = {
    "1024 × 1024  (Square)":        (1024, 1024),
    "1024 × 2048  (Portrait 1:2)":  (1024, 2048),
    "2048 × 1024  (Landscape 2:1)": (2048, 1024),
    "1024 × 1536  (Portrait 2:3)":  (1024, 1536),
    "1536 × 1024  (Landscape 3:2)": (1536, 1024),
    "Custom":                        None,
}

SUPPORTED_FORMATS = [
    ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.gif"),
    ("All files", "*.*"),
]


class ImageCombinerApp:
    """Main application window."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Image Combiner")
        self.root.geometry("920x760")

        # Set window icon
        try:
            icon = Image.open(_resource_path("icon.png"))
            self._icon_photo = ImageTk.PhotoImage(icon)
            self.root.iconphoto(True, self._icon_photo)
        except Exception:
            pass  # graceful fallback if icon missing
        self.root.minsize(760, 620)

        # ── State ─────────────────────────────────────────────────────
        self.images: list[tuple[str, Image.Image]] = []   # (path, PIL Image)
        self.gap_color = "#000000"
        self._preview_photo = None          # prevent GC of PhotoImage

        self._build_ui()

    # ── UI construction ───────────────────────────────────────────────
    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("vista")        # Windows-native look
        except tk.TclError:
            pass

        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)

        self._build_toolbar(main)
        self._build_middle(main)
        self._build_bottom(main)

    # ── Toolbar ───────────────────────────────────────────────────────
    def _build_toolbar(self, parent):
        bar = ttk.Frame(parent)
        bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Button(bar, text="Add Images",  command=self._add_images).pack(side=tk.LEFT, padx=2)
        ttk.Button(bar, text="Remove",       command=self._remove_image).pack(side=tk.LEFT, padx=2)
        ttk.Separator(bar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6)
        ttk.Button(bar, text="▲ Up",         command=self._move_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(bar, text="▼ Down",       command=self._move_down).pack(side=tk.LEFT, padx=2)
        ttk.Separator(bar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6)
        ttk.Button(bar, text="Clear All",    command=self._clear_all).pack(side=tk.LEFT, padx=2)

    # ── Middle: image list + settings ─────────────────────────────────
    def _build_middle(self, parent):
        mid = ttk.Frame(parent)
        mid.pack(fill=tk.BOTH, expand=False, pady=4)

        # Left — image list
        list_fr = ttk.LabelFrame(mid, text="Images (drag order with ▲▼)", padding=5)
        list_fr.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        self.listbox = tk.Listbox(list_fr, selectmode=tk.SINGLE,
                                  font=("Segoe UI", 10), height=8,
                                  activestyle="dotbox")
        sb = ttk.Scrollbar(list_fr, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=sb.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # Right — settings
        self._build_settings(mid)

    def _build_settings(self, parent):
        sf = ttk.LabelFrame(parent, text="Settings", padding=10)
        sf.pack(side=tk.RIGHT, fill=tk.Y, ipadx=8)

        # Preset
        ttk.Label(sf, text="Resolution Preset:").pack(anchor=tk.W)
        self.preset_var = tk.StringVar(value=list(PRESETS.keys())[0])
        cb = ttk.Combobox(sf, textvariable=self.preset_var,
                          values=list(PRESETS.keys()), state="readonly", width=28)
        cb.pack(anchor=tk.W, pady=(0, 8))
        cb.bind("<<ComboboxSelected>>", self._on_preset_change)

        # Width / Height
        dim_fr = ttk.Frame(sf)
        dim_fr.pack(anchor=tk.W, pady=(0, 8))

        ttk.Label(dim_fr, text="W:").grid(row=0, column=0, sticky=tk.W)
        self.width_var = tk.StringVar(value="1024")
        self.width_entry = ttk.Entry(dim_fr, textvariable=self.width_var, width=8)
        self.width_entry.grid(row=0, column=1, padx=(2, 10))

        ttk.Label(dim_fr, text="H:").grid(row=0, column=2, sticky=tk.W)
        self.height_var = tk.StringVar(value="1024")
        self.height_entry = ttk.Entry(dim_fr, textvariable=self.height_var, width=8)
        self.height_entry.grid(row=0, column=3, padx=2)

        self.width_entry.configure(state="disabled")
        self.height_entry.configure(state="disabled")

        # Gap slider
        ttk.Label(sf, text="Gap / Border:").pack(anchor=tk.W)
        self.gap_var = tk.IntVar(value=0)
        self.gap_label = ttk.Label(sf, text="0 px")
        gap_slider = ttk.Scale(sf, from_=0, to=80, variable=self.gap_var,
                               orient=tk.HORIZONTAL, command=self._on_gap_change)
        gap_slider.pack(anchor=tk.W, fill=tk.X, pady=(0, 1))
        self.gap_label.pack(anchor=tk.W, pady=(0, 8))

        # Gap colour
        col_fr = ttk.Frame(sf)
        col_fr.pack(anchor=tk.W, pady=(0, 4))
        ttk.Label(col_fr, text="Gap Colour:").pack(side=tk.LEFT)
        self.color_swatch = tk.Label(col_fr, bg=self.gap_color,
                                     width=3, relief=tk.SUNKEN, bd=2)
        self.color_swatch.pack(side=tk.LEFT, padx=6)
        ttk.Button(col_fr, text="Pick…", command=self._pick_color).pack(side=tk.LEFT)

    # ── Bottom: preview + action buttons ──────────────────────────────
    def _build_bottom(self, parent):
        bot = ttk.Frame(parent)
        bot.pack(fill=tk.BOTH, expand=True, pady=4)

        btn_fr = ttk.Frame(bot)
        btn_fr.pack(fill=tk.X, pady=(0, 4))
        ttk.Button(btn_fr, text="🔄 Preview",        command=self._preview).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_fr, text="💾 Combine & Save",  command=self._combine_and_save).pack(side=tk.RIGHT, padx=2)

        pf = ttk.LabelFrame(bot, text="Preview", padding=4)
        pf.pack(fill=tk.BOTH, expand=True)

        self.preview_canvas = tk.Canvas(pf, bg="#2b2b2b", highlightthickness=0)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)

    # ── Callbacks ─────────────────────────────────────────────────────
    def _add_images(self):
        paths = filedialog.askopenfilenames(title="Select Images",
                                            filetypes=SUPPORTED_FORMATS)
        for p in paths:
            try:
                img = Image.open(p)
                img.load()
                self.images.append((p, img))
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open:\n{p}\n\n{e}")
        self._refresh_listbox()

    def _remove_image(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.images.pop(idx)
        self._refresh_listbox()

    def _clear_all(self):
        self.images.clear()
        self._refresh_listbox()
        self.preview_canvas.delete("all")

    def _move_up(self):
        sel = self.listbox.curselection()
        if not sel or sel[0] == 0:
            return
        i = sel[0]
        self.images[i], self.images[i - 1] = self.images[i - 1], self.images[i]
        self._refresh_listbox()
        self.listbox.selection_set(i - 1)

    def _move_down(self):
        sel = self.listbox.curselection()
        if not sel or sel[0] >= len(self.images) - 1:
            return
        i = sel[0]
        self.images[i], self.images[i + 1] = self.images[i + 1], self.images[i]
        self._refresh_listbox()
        self.listbox.selection_set(i + 1)

    def _on_preset_change(self, _event=None):
        key = self.preset_var.get()
        dims = PRESETS.get(key)
        if dims is None:
            self.width_entry.configure(state="normal")
            self.height_entry.configure(state="normal")
        else:
            self.width_var.set(str(dims[0]))
            self.height_var.set(str(dims[1]))
            self.width_entry.configure(state="disabled")
            self.height_entry.configure(state="disabled")

    def _on_gap_change(self, val):
        self.gap_label.configure(text=f"{int(float(val))} px")

    def _pick_color(self):
        result = colorchooser.askcolor(color=self.gap_color, title="Gap Colour")
        if result and result[1]:
            self.gap_color = result[1]
            self.color_swatch.configure(bg=self.gap_color)

    # ── Helpers ───────────────────────────────────────────────────────
    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, (path, _img) in enumerate(self.images):
            name = os.path.basename(path)
            self.listbox.insert(tk.END, f"  {i + 1}.  {name}")

    def _get_dimensions(self):
        """Return (width, height) from current settings, or None on error."""
        try:
            w = int(self.width_var.get())
            h = int(self.height_var.get())
            if w < 16 or h < 16:
                raise ValueError
            return w, h
        except ValueError:
            messagebox.showerror("Invalid Size",
                                 "Width and Height must be integers ≥ 16.")
            return None

    def _hex_to_rgb(self, hex_color: str):
        h = hex_color.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _make_combined(self):
        """Build and return the combined PIL Image, or None on error."""
        if not self.images:
            messagebox.showinfo("No Images", "Add some images first.")
            return None

        dims = self._get_dimensions()
        if dims is None:
            return None
        w, h = dims

        gap = int(self.gap_var.get())
        bg = self._hex_to_rgb(self.gap_color)
        pil_images = [img for (_path, img) in self.images]

        return combine_images(pil_images, w, h, gap=gap, bg_color=bg)

    # ── Preview / Save ────────────────────────────────────────────────
    def _preview(self):
        combined = self._make_combined()
        if combined is None:
            return

        self.preview_canvas.update_idletasks()
        cw = self.preview_canvas.winfo_width()
        ch = self.preview_canvas.winfo_height()

        if cw < 10 or ch < 10:
            return

        # Scale to fit canvas while keeping aspect ratio
        img_w, img_h = combined.size
        scale = min(cw / img_w, ch / img_h, 1.0)
        display_w = max(int(img_w * scale), 1)
        display_h = max(int(img_h * scale), 1)

        thumb = combined.resize((display_w, display_h), Image.LANCZOS)
        self._preview_photo = ImageTk.PhotoImage(thumb)

        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(cw // 2, ch // 2,
                                         image=self._preview_photo,
                                         anchor=tk.CENTER)

    def _combine_and_save(self):
        combined = self._make_combined()
        if combined is None:
            return

        path = filedialog.asksaveasfilename(
            title="Save Combined Image",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"),
                       ("BMP", "*.bmp"), ("WEBP", "*.webp")],
        )
        if not path:
            return

        try:
            combined.save(path)
            messagebox.showinfo("Saved", f"Image saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
