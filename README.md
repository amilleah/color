# color

This is a set of scripts to extract color palettes + color weights to images using mean
-shift clustering. Here are some references to get started if you're unfamiliar with the method:

[GneissName on YouTube](https://www.youtube.com/watch?v%3DHuW9qJbL0xM&) \
[Mean Shift clustering](https://spin.atomicobject.com/mean-shift-clustering/) \
[CIELAB color space (Wikipedia)](https://en.wikipedia.org/wiki/CIELAB_color_space)

## examples

<table>
  <tr>
    <td rowspan="2"><img src="https://github.com/user-attachments/assets/56c7e7a4-4875-486a-acc1-97519a1210ae" alt="red-flowers" /></td>
    <td><img src="https://github.com/user-attachments/assets/ef31c4a0-5efa-4516-9b33-a154ecd4cec3" alt="palette" /></td>
  </tr>
  <tr>
    <td><pre>{
  "red-flowers.png": {
    "colors_lab": [
      [37.42, -12.30, 17.46],
      [64.07,  -1.00,  3.15],
      [37.01,   3.28,  2.75],
      [99.48,  -0.71, -0.16],
      [25.03,  32.09,  5.86]
    ],
    "weights": [0.5016, 0.1601, 0.144, 0.0881, 0.0493]
  }
}</pre></td>
  </tr>
</table>

I use an adapted form of this script to index the Princeton Art Museum's (free) online archive: [PUAM API on GitHub](https://github.com/Princeton-University-Art-Museum/puam-api-docs)

You can find this project on [color.amilleah.com](https://color.amilleah.com)

or on Are.na: [amilleah/hexcode](https://are.na/amilleah/hexcode)

## install uv

I used [UV](https://docs.astral.sh) for this project.

```
uv sync
```

## how to use

Extract palettes from every photo in a folder. Writes `<name>.palette.png` next to each image and a `palettes.json` index.

```
uv run python run.py PATH/TO/PHOTOS
uv run python run.py PATH/TO/PHOTOS --colors 8
```

## files

- `colors.py`               RGB ↔ CIELAB conversion
- `images.py`               palette extraction (mean-shift) and swatch rendering
- `run.py`                  folder loop, writes sidecars + index
- `README.md`               this document :)
- `pyproject.toml`          uv environment
