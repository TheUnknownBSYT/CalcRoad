# CalcRoad

Code used for the Advanced Calculus project by Siddhant Budhia. The two Python scripts generate figures for a model of a crowned road with a longitudinal sag and gutter inlets.

## Road model

Both figures use the elevation surface

```text
z(x, y) = 0.00025 x² + 0.07 (1 − y² / 12.25)
```

Here `x` is the longitudinal position, `y` is the transverse position, and `z` is elevation, all in metres. The plotted road extends from −20 to 20 m along its length and from −3.5 to 3.5 m across its width.

## Files

- `road_elevation_surface.py` plots the road surface, its saddle point, and the two gutter inlets. It writes `road_elevation_surface.png`.
- `flooded_road_region.py` plots the flooded regions and a transverse section for a water level of 0.05 m. It writes the transparent image `FM116_Flooded_Region.png`.
- `requirements.txt` lists the Python dependencies.

The scripts write their figures alongside the scripts. The vertical scale is exaggerated in the figures.

## Run

With Python 3 installed, run from this directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python road_elevation_surface.py
python flooded_road_region.py
```

On Windows, activate the environment with `.venv\Scripts\activate` instead. Generated figures are excluded from version control and can be reproduced by running the scripts.
