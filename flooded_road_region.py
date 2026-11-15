"""Reproduce the FM116 flooded-road figure.

Install dependencies with: python -m pip install numpy matplotlib
Run with: python flooded_road_region.py
The transparent PNG is saved next to this script.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

ink = "#202c37"
muted = "#55636f"
road = "#dce0e3"
edge = "#727d87"
blue = "#186ca4"
water = "#87c9ed"
red = "#ac3c38"
h = .05
a = np.sqrt(h / .00025)
b = 3.5 * np.sqrt(1 - h / .07)

def z(x, y):
    return .00025*x*x + .07*(1-y*y/12.25)

def projection(x, y, elevation):
    return x - .50*y, .165*x + .72*y + 10*elevation

plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"text.color":ink,"axes.labelcolor":ink,
                     "axes.edgecolor":edge,"xtick.color":muted,"ytick.color":muted,"mathtext.fontset":"dejavusans"})
fig = plt.figure(figsize=(8,6.3))
p = fig.add_axes([.055,.405,.89,.47])
s = fig.add_axes([.12,.135,.81,.215])
fig.text(.055,.958,"Flooded road at the 5 cm target",fontsize=22,weight="bold",va="top")
fig.text(.055,.889,"(a)  Oblique view",fontsize=11,weight="bold")
fig.text(.945,.889,"Vertical scale exaggerated",fontsize=8.5,ha="right",color=muted)

x = np.linspace(-20,20,281)
ys = np.linspace(-3.5,3.5,111)
cmap = LinearSegmentedColormap.from_list("pavement",["#aab2b9","#edf0f2"])
strips, colors = [], []
for lo, hi in zip(ys[:-1],ys[1:]):
    upper = np.column_stack(projection(x,hi,z(x,hi)))
    lower = np.column_stack(projection(x[::-1],lo,z(x[::-1],lo)))
    strips.append(np.vstack([upper,lower]))
    colors.append(cmap(.26+.74*(1-abs((hi+lo)/7))**.64))
for y in [-3.5,3.5]:
    sx, sy = projection(x,y,z(x,y))
    p.fill_between(sx,sy-.18,sy,color="#939da6",edgecolor=edge,lw=.5)
sx, sy = projection(-20,ys,z(-20,ys))
p.fill_between(sx,sy-.18,sy,color="#9ca6af",edgecolor=edge,lw=.5)
p.add_collection(PolyCollection(strips,facecolors=colors,edgecolors=colors,linewidths=.35))
for y in [-3.5,3.5]:
    p.plot(*projection(x,y,z(x,y)),color=edge,lw=.85)
for xx in [-20,20]:
    p.plot(*projection(xx,ys,z(xx,ys)),color=edge,lw=.85)
p.plot(*projection(x,0,z(x,0)),color="#747f88",lw=.8,dashes=(4,4))
xx = np.linspace(-a,a,1001)
y0 = 3.5*np.sqrt(1-(h-.00025*xx**2)/.07)
assert np.allclose(z(xx,y0),h)
for sign in [1,-1]:
    sx1,sy1 = projection(xx,sign*y0,h)
    sx2,sy2 = projection(xx[::-1],sign*3.5,h)
    p.fill(np.r_[sx1,sx2],np.r_[sy1,sy2],facecolor=water,edgecolor=blue,lw=1.15,zorder=4)
    if sign == -1:
        sx, lower = projection(xx, -3.5, z(xx,-3.5))
        _, upper = projection(xx, -3.5, h)
        p.fill_between(sx, lower, upper, color="#6fb2da", edgecolor=blue, lw=.7, zorder=4)
    jx,jy = projection(0,sign*3.5,0)
    p.scatter(jx,jy,s=31,c=red,marker="s",edgecolor="white",linewidth=.7,zorder=6)
    p.text(jx-.55,jy+(.57 if sign>0 else -.52),"B" if sign>0 else "A",
           color=red,weight="bold",ha="right",va="center",zorder=6)
p.plot(*projection(np.zeros_like(ys),ys,np.maximum(h,z(0,ys))),color=muted,ls=":",lw=1,zorder=5)
p.annotate("Road crown",xy=projection(-11,0,z(-11,0)),xytext=(-15,3.2),ha="center",fontsize=9,
           arrowprops={"arrowstyle":"-","lw":.75,"color":muted,"shrinkB":3})
p.annotate("Section at $x=0$",xy=projection(0,2.56,h),xytext=(.2,5.15),fontsize=9,zorder=7,
           arrowprops={"arrowstyle":"-","lw":.75,"color":muted,"shrinkB":3})
p.annotate("$x=-14.142$ m",xy=projection(-a,-3.5,h),xytext=(-16.5,-5.83),ha="center",fontsize=9,
           arrowprops={"arrowstyle":"-","lw":.75,"color":blue,"shrinkB":2})
p.annotate("$x=14.142$ m",xy=projection(a,-3.5,h),xytext=(17,-2.1),ha="center",fontsize=9,
           arrowprops={"arrowstyle":"-","lw":.75,"color":blue,"shrinkB":2})
p.set(xlim=(-23,23),ylim=(-6.7,7.65))
p.axis("off")
fig.legend(handles=[Patch(facecolor=water,edgecolor=blue,label="Flooded region"),
                    Line2D([],[],marker="s",ls="",color=red,label="Existing inlet",markersize=5)],
           loc="center",bbox_to_anchor=(.55,.45),ncol=2,frameon=False,fontsize=9,
           handlelength=1.65,columnspacing=2.5)
fig.add_artist(Line2D([.055,.945],[.416,.416],transform=fig.transFigure,color="#cbd2d8",lw=.8))
fig.text(.055,.38,"(b)  Transverse section at $x=0$",fontsize=11,weight="bold")
fig.text(.945,.38,"Vertical scale exaggerated",fontsize=8.5,ha="right",color=muted)
y = np.linspace(-3.5,3.5,801)
s.fill_between(y,0,100*z(0,y),color=road)
s.plot(y,100*z(0,y),color=edge,lw=1.65)
for lo,hi in [(-3.5,-b),(b,3.5)]:
    w = np.linspace(lo,hi,481)
    s.fill_between(w,100*z(0,w),5,color=water)
    s.plot([lo,hi],[5,5],color=blue,lw=1.8)
s.plot([-b,b],[5,5],color=blue,ls=":",lw=1)
s.text(0,4.54,"Water level $h=5$ cm",ha="center",va="top",color=blue,fontsize=9)
s.text(0,1.3,"Road elevation $z(0,y)$",ha="center",color=muted,fontsize=9)
s.annotate("",xy=(3.64,5),xytext=(3.64,0),
           arrowprops={"arrowstyle":"<->","color":blue,"lw":1.1,"shrinkA":0,"shrinkB":0})
s.text(3.78,2.5,"5 cm\nmax. depth",va="center",color=blue,fontsize=8.5)
s.set(xlim=(-3.72,4.65),ylim=(-.05,7.6),xticks=[-3.5,-b,0,b,3.5],yticks=[0,2,5,7],
      xlabel="Transverse position $y$ (m)",ylabel="Elevation (cm)")
s.set_xticklabels(["−3.5","−1.871","0","1.871","3.5"])
s.spines[["top","right"]].set_visible(False)
s.tick_params(length=3,labelsize=8.5)
output_path = Path(__file__).resolve().with_name("FM116_Flooded_Region.png")
fig.savefig(output_path, dpi=400, transparent=True, bbox_inches="tight", pad_inches=.16)
plt.close(fig)
print(f"Saved {output_path}")
