# An overview of EnGlyph

The EnGlyph widget is designed to mix native terminal text with text based
graphics for data display and unique styling development.

## Deps

Englyph is a TUI tool that builds on Textual and Rich TUI capabilities by
constructing novel text+graphics via Pillow modern Unicode glyphis using
octant, sextant, quadrant and binant based pixels (glyxels).

1) https://github.com/Textualize/textual
2) https://github.com/Textualize/rich
3) https://python-pillow.github.io/
5) https://unicode.org/charts/nameslist/

## EnGlyphText based scalable text

To generate text with the EnGlyph tool use the textual_englyph module. To get to to the point
quicly let's just drop a simple but fully functional code example.

```python
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText

class Test(App):

    def compose(self) -> ComposeResult:
        yield EnGlyphText("From [red]EnGlyph,", text_size="x-small")
        yield EnGlyphText("Bonjour [dark_orange]Textual!", text_size="small")
        yield EnGlyphText("Olá [bright_yellow]Textual!", text_size="medium")
        yield EnGlyphText("Ciao [green]Textual!", text_size="large")
        yield EnGlyphText("Привiт [cornflower_blue]Textual!", text_size="x-large")
        yield EnGlyphText("Γειά σου [blue1]Textual!", text_size="xx-large")
        yield EnGlyphText("Dobrý deň [violet]Textual!", text_size="xxx-large")

if __name__ == "__main__":
    Test().run()
```

There are a few predefined sizes. The "x-xmall" size is the basline size of
standard terminal text. From there the characters are built from glyphs of a
cell partitioned into pixel like parts, called a glyxel in this document. The
default cell glyxels are 2 columns by 4 rows, but other partitions are
supported as well. This dependency on Unicode version 16 glyphs means that the
terminal native font must be quite recent to enable all partioning glyphs used.
Further, your platform must support the Pillow module to handle image and
bitmap font interpretation. 

It is also possible to use open fonts of your choice. Bitmap fonts are
recommended unless you are wanting to display very large text. Some fun choices
can be obtained from:

https://www.nerdfonts.com/font-downloads
https://www.dafont.com/bitmap.php

Use of your chosen font is made possible by following this example:
```python
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText


class Test(App):
    """Test console markup styling the englyph text use case"""

    def compose(self) -> ComposeResult:
        yield EnGlyphText("From EnGlyph, Hello [violet]Textual!", font_name="/tmp/Gohu/GohuFontuni11NerdFont-Regular.ttf", font_size=11)

if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
```
## EnGlyphImage based scalable text

To generate an image with EnGlyph use the EnGlyphImage widget. To get to the
point quickly here is a simple code example.

```python
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphImage


class Test(App):
    DEFAULT_CSS = """
    #I {
        height: 16;
    }
    """

# Please provide your image filename instead of hopper.jpg
    def compose(self) -> ComposeResult:
        yield EnGlyphImage("hopper.jpg", id="I")

if __name__ == "__main__":
    Test().run()
```

The default argument string for EnGlyphImage is a path to a named image. An
image can be resized by assigning TCSS attributes of width, height, max_width
and max_height. Aspect ratio is preserved if only one attribute is used and the
max attributes can be used to clip the image. The image types supported are
those supported by the Pillow module. The default glyxels used to build the
image in your terminal are 2x4 dots per cell, but a cell can only support 2
colors so the image is a nearest two color representation for the space covered
by a given cell. If you need fully accurate colors then passing the attribute
`basis=(1,2)` will cause the image to be constructed with only 2 glyxels.

