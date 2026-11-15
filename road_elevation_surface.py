from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection


VERTICAL_SCALE = 9
OUTPUT = Path(__file__).resolve().with_name("road_elevation_surface.png")


def elevation(x, y):
    return 0.00025 * x**2 + 0.07 * (1 - y**2 / 12.25)


def project(x, y, z):
    """Project 3D coordinates onto the page at a fixed viewing angle."""
    x, y, z = np.broadcast_arrays(x, y, z)
    azimuth = np.deg2rad(12)
    pitch = np.deg2rad(28)

    horizontal = np.cos(azimuth) * x + np.sin(azimuth) * y
    depth = -np.sin(azimuth) * x + np.cos(azimuth) * y
    vertical = np.sin(pitch) * depth + np.cos(pitch) * VERTICAL_SCALE * z
    return np.stack((horizontal, vertical), axis=-1)


fig, ax = plt.subplots(figsize=(8.4, 3.45), facecolor="white")
fig.subplots_adjust(left=0.045, right=0.965, top=0.86, bottom=0.14)
fig.suptitle("Road elevation surface", y=0.94, fontsize=14, weight="semibold")

ax.set_aspect("equal")
ax.set_xlim(-26, 25)
ax.set_ylim(-7.8, 7.6)
ax.set_frame_on(False)
ax.set_xticks([])
ax.set_yticks([])

# Calculate the road surface and project the mesh onto the page.
x = np.linspace(-20, 20, 101)
y = np.linspace(-3.5, 3.5, 31)
X, Y = np.meshgrid(x, y)
surface = project(X, Y, elevation(X, Y))

cells = np.stack(
    (surface[:-1, :-1], surface[:-1, 1:],
     surface[1:, 1:], surface[1:, :-1]),
    axis=2,
)

# Light shading across the width helps show the crown.
tone = 0.84 + 0.075 * np.cos(np.pi * Y[:-1, :-1] / 7)
colors = np.stack((tone - 0.025, tone - 0.010, tone + 0.006), axis=-1)
ax.add_collection(
    PolyCollection(
        cells.reshape(-1, 4, 2),
        facecolors=colors.reshape(-1, 3),
        edgecolors="face",
        linewidths=0.2,
        zorder=2,
    )
)


def draw_line(x, y, z, **style):
    ax.plot(*project(x, y, z).T, **style)


# Outline the gutters and road ends.
for gutter_y in (-3.5, 3.5):
    draw_line(x, gutter_y, elevation(x, gutter_y),
              color="#535e68", lw=1.15, zorder=3)

for end_x in (-20, 20):
    draw_line(end_x, y, elevation(end_x, y),
              color="#535e68", lw=1, zorder=3)

# The dashed centreline follows the sag. The cross-section shows the crown.
draw_line(x, 0, elevation(x, 0),
          color="#4b545c", ls="--", lw=1.05, zorder=4)
draw_line(0, y, elevation(0, y),
          color="#737c84", lw=0.85, zorder=4)

# Draw three coordinate scales around the surface.
axis_style = dict(color="#474d52", lw=0.8, zorder=5)
draw_line([-20, 20], -4.8, 0, **axis_style)
draw_line(21.2, [-3.5, 3.5], 0, **axis_style)
draw_line(-23, 0, [0, 0.17], **axis_style)


def draw_tick(point, tick_offset, label_offset, label, ha="center", va="center"):
    u, v = project(*point)
    du, dv = tick_offset
    ax.plot([u, u + du], [v, v + dv], **axis_style)
    ax.annotate(
        label, (u, v), xytext=label_offset, textcoords="offset points",
        ha=ha, va=va, fontsize=8.5, color="#30363a",
    )


for value in (-20, -10, 0, 10, 20):
    draw_tick((value, -4.8, 0), (0, -0.26), (0, -5.5),
              f"{value:g}".replace("-", "−"), va="top")

for value in (-3.5, 0, 3.5):
    draw_tick((21.2, value, 0), (0.28, 0), (5, 0),
              f"{value:g}".replace("-", "−"), ha="left")

for value in (0, 0.17):
    draw_tick((-23, 0, value), (-0.26, 0), (-5, 0),
              f"{value:.2f}", ha="right")

ax.text(-2.2, -6.6, "Road length, x (m)", ha="center", fontsize=9.5)
ax.text(21.7, 1.1, "Road width, y (m)", ha="center", fontsize=9.5)
ax.text(-23.4, 4.9, "Elevation, z (m)", ha="center", fontsize=9.5)

# Mark the saddle point and both inlet locations.
features = (
    ((0, 0, 0.07), "Saddle point\n(0, 0, 0.07)", (-6.3, 5.7), "#353d45"),
    ((0, -3.5, 0), "Gutter inlet\n(0, −3.5, 0)", (-10.9, -4.2), "#a53237"),
    ((0, 3.5, 0), "Gutter inlet\n(0, 3.5, 0)", (9.8, 4.5), "#a53237"),
)

for coordinates, label, position, color in features:
    u, v = project(*coordinates)
    ax.scatter(u, v, s=33, color=color, edgecolor="white", linewidth=0.7, zorder=7)
    ax.annotate(
        label, (u, v), xytext=position,
        ha="center", va="center", fontsize=9.5, zorder=8,
        arrowprops=dict(arrowstyle="-", color=color, lw=0.85, shrinkA=5, shrinkB=4),
    )

if VERTICAL_SCALE != 1:
    fig.text(
        0.5, 0.085,
        f"Vertical scale exaggerated for clarity ({VERTICAL_SCALE:g}×)",
        ha="center", fontsize=8.5, color="#535b63",
    )

fig.savefig(OUTPUT, dpi=300, bbox_inches="tight", pad_inches=0.15)
print(f"Saved to {OUTPUT}")
plt.close(fig)