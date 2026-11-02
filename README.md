# Image Gallery

**Category:** Classes

## Problem

Create an image abstract class and then a class that inherits from it for each image type. Put them in a program which displays them in a gallery style format for viewing.

## Solution

`Image` is an ABC with metadata and thumbnail behavior; `PngImage`, `JpgImage` and `GifImage` subclass it. `Gallery` indexes a directory, prints each image's format/size/mode, and renders a self-contained HTML grid with base64 JPEG thumbnails (no external files needed). Requires Pillow.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --dir ./photos --output gallery.html
python3 main.py --demo
```

## Example

```text
indexed 3 images
GIF    forest.gif                320x240  P
JPEG   ocean.jpg                 320x240  RGB
PNG    sunset.png                320x240  RGB
html written: 5115 bytes, embedded thumbnails: 3
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.
