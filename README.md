# color

This is a set of scripts to extract color palettes + color weights to images using mena-shift clustering. Here are some references to get started if you're unfamiliar with the method:

[GneissName on YouTube](https://www.youtube.com/watch?v%3DHuW9qJbL0xM&)
[Mean Shift clustering](https://spin.atomicobject.com/mean-shift-clustering/)
[CIELAB color space (Wikipedia)](https://en.wikipedia.org/wiki/CIELAB_color_space)

## examples

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
python run.py PATH/TO/PHOTOS
python run.py PATH/TO/PHOTOS --colors 8
```

## files

- `colors.py`               RGB ↔ CIELAB conversion
- `images.py`               palette extraction (mean-shift) and swatch rendering
- `run.py`                  folder loop, writes sidecars + index
- `README.md`               this document :)
- `pyproject.toml`          uv environment
