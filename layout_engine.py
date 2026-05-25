"""
Layout Engine — calculates grid cell positions for N images
within a target canvas, including gap/border support.
"""


def calculate_layout(n_images, target_width, target_height, gap=0):
    """
    Calculate cell rectangles for n_images within a canvas.

    Args:
        n_images:      Number of images to place.
        target_width:  Canvas width in pixels.
        target_height: Canvas height in pixels.
        gap:           Gap size in pixels (between images AND at edges).

    Returns:
        List of (x, y, width, height) tuples — one per image.
    """
    if n_images <= 0:
        return []

    if n_images == 1:
        return [(gap, gap,
                 target_width - 2 * gap,
                 target_height - 2 * gap)]

    dist = _find_best_distribution(n_images, target_width, target_height)
    num_rows = len(dist)

    # Pixel-perfect row heights
    total_h_gap = gap * (num_rows + 1)
    avail_h = max(target_height - total_h_gap, num_rows)
    row_heights = _distribute_pixels(avail_h, num_rows)

    cells = []
    y = gap
    for row_idx in range(num_rows):
        cols = dist[row_idx]
        rh = row_heights[row_idx]

        total_w_gap = gap * (cols + 1)
        avail_w = max(target_width - total_w_gap, cols)
        col_widths = _distribute_pixels(avail_w, cols)

        x = gap
        for col_idx in range(cols):
            cw = col_widths[col_idx]
            cells.append((x, y, cw, rh))
            x += cw + gap

        y += rh + gap

    return cells


def _find_best_distribution(n, width, height):
    """
    Find the best row distribution for *n* images.

    Returns a list of ints — each int is the number of columns in that row.
    The distribution that yields cell aspect ratios closest to 1:1 wins.
    """
    best_score = float('inf')
    best_dist = None

    for num_rows in range(1, min(n, 10) + 1):
        base = n // num_rows
        extra = n % num_rows

        if base == 0:
            continue

        # Rows with fewer cols first, rows with more cols later
        dist = [base] * (num_rows - extra) + [base + 1] * extra

        # Score: sum-of-squares deviation of cell aspect ratio from 1.0
        row_h = height / num_rows
        score = 0.0
        for cols in dist:
            cell_w = width / cols
            ratio = cell_w / row_h
            score += (ratio - 1.0) ** 2

        if score < best_score:
            best_score = score
            best_dist = dist

    return best_dist


def _distribute_pixels(total, count):
    """Distribute *total* pixels into *count* parts as evenly as possible."""
    if count <= 0:
        return []
    base = total // count
    remainder = total % count
    # Last `remainder` items get one extra pixel
    return [base] * (count - remainder) + [base + 1] * remainder
