---
layout: post
title: PNG Image Optimisation
tags:
  - png
  - image
  - optimise
---

Some tools that can be used to reduce PNG file sizes whilst maintaining good quality images. All those below can be installed and used within the WSL (Windows Subsystem for Linux).

### Sample Image:

A graphic with transparency is probably better suited for a PNG, but who doesn't love a bit of tilt shift?

**Original Size: 711KB**

![Original Image](/images/2017/sample-optim.png)

### PNG Crush (lossless)

Probably the most popular, but has a lot of options and you may need to know some compression details to get the best results out of the tool.

    > sudo apt-get install pngcrush

(also works on WSL)

    > pngcrush input.png output.png

    > pngcrush -brute input.png output.png

The `-brute` option will through 148 different reduction algorithms and chooses the best result.

    > pngcrush -brute -reduce -rem allb input.png output.png

The `-reduce` option counts the number of distinct colours and reduces the pixel depth to the smallest size that can contain the palette.

**Compressed size: 539KB (24% reduction)**

### Optipng (lossless)

Based on `pngcrush` but tries to figure out the best config options for you. In this case so suprise that we get the same results.

    > sudo apt-get install optipng

    > optipng -o7 -out outfile.png input.png

The `-o7` option specifies maximum optimisation but will take the longest to process.

**Compressed size: 539KB (24% reduction)**

### PNGQuant (lossy)

The conversion reduces file sizes significantly (often as much as 70%) and preserves full alpha transparency. It turns 24-bit RGB files into palettized 8-bit ones. You lose some color depth, but for small images it's often imperceptible.

    > sudo apt-get install pngquant

    > pngquant input.png

**Compressed size: 193KB (73% reduction)**

![Original Image](/images/2017/sample-quant.png)

If you look closely you can see some minor visual differences between this and the original image. However, the file size reduction is huge and the image quality remains very good. Definitely a great tool for the vast majority of images you find on the web.
