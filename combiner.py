"""
Combiner — crops, resizes and composites images onto a final canvas.
"""

from PIL import Image
from layout_engine import calculate_layout


def center_crop_fit(image, cell_width, cell_height):
    """
    Scale *image* to fully COVER the cell, then centre-crop to exact size.
    Guarantees no black bars — the image always fills the cell.
    """
    if cell_width <= 0 or cell_height <= 0:
        return Image.new("RGB", (max(cell_width, 1), max(cell_height, 1)))

    img_w, img_h = image.size

    # Scale factor so the image covers the cell in both dimensions
    scale = max(cell_width / img_w, cell_height / img_h)
    new_w = max(round(img_w * scale), 1)
    new_h = max(round(img_h * scale), 1)

    resized = image.resize((new_w, new_h), Image.LANCZOS)

    # Centre crop
    left = (new_w - cell_width) // 2
    top = (new_h - cell_height) // 2
    return resized.crop((left, top, left + cell_width, top + cell_height))


def combine_images(images, target_width, target_height,
                   gap=0, bg_color=(0, 0, 0)):
    """
    Combine a list of PIL Images into a single canvas.

    Args:
        images:        List of PIL.Image objects (in desired order).
        target_width:  Output width in pixels.
        target_height: Output height in pixels.
        gap:           Gap / border size in pixels.
        bg_color:      Background / gap colour as an RGB tuple.

    Returns:
        A new PIL.Image with all images composited.
    """
    layout = calculate_layout(len(images), target_width, target_height, gap)
    canvas = Image.new("RGB", (target_width, target_height), bg_color)

    for i, (x, y, w, h) in enumerate(layout):
        if i >= len(images):
            break

        img = images[i]
        if img.mode != "RGB":
            img = img.convert("RGB")

        fitted = center_crop_fit(img, w, h)
        canvas.paste(fitted, (x, y))

    return canvas
