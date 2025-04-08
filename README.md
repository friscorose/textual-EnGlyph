# Textual-EnGlyph
A large font rendering widget for the Textual platform.

# Requirements
For this to look good you will need a terminal emulator that supports Unicode and a font
that has glyphs for the Symbols for Legacy Computing block defined by Unicode version 16.0. 

## Known terminals
 - iTerm2 (OS X)
 - xfce4-Terminal (Linux)
 - Terminal (Windows)
 - ...and many more.

## Known terminal fonts
 - Cascadia Code https://github.com/microsoft/cascadia-code/, v 2404.3 or later
 - GNU Unifont http://savannah.gnu.org/projects/unifont/, v 16.0 or later 
 - Iosevka https://typeof.net/Iosevka/, v 13.9.1 or later

# Howto
This widget library is available as a python PyPi library. 

This HowTo recommends `uv` to manage your python environment,
see https://docs.astral.sh/uv/guides/ for using `uv`.

Install and inport the text widget
```bash
uv pip install textual-englyph
```
Use as a module in your textual python app. Save the following simple example as `text.py`
```python
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText


class Test(App):
    """Test console markup styling the englyph text use case"""

    def compose(self) -> ComposeResult:
        yield EnGlyphText("From [red]EnGlyph,", text_size="x-small")
        yield EnGlyphText("Bonjour [dark_orange]Textual!", text_size="small")
        yield EnGlyphText("Olá [bright_yellow]Textual!", text_size="medium")
        yield EnGlyphText("Привiт [green]Textual!", text_size="large")
        yield EnGlyphText("Γειά σου [cornflower_blue]Textual!", text_size="x-large")
        yield EnGlyphText("Ciao [blue1]Textual!", text_size="xx-large")
        yield EnGlyphText("Dobrý deň [violet]Textual!", text_size="xxx-large")

if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
```
and run it (use ctrl-q to exit)
```bash
uv run text.py
```

EnGlyph also includes an image widget that can display many image formats
```python
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText, EnGlyphImage


class Test(App):
    """Test the basic englyph image use case"""

    DEFAULT_CSS = """
    #I {
        width: 16;
    }
    #T {
        background: white 50%;
        position: relative;
        offset: 6 -1;
    }
    """

    def compose(self) -> ComposeResult:
        yield EnGlyphImage("path_to_your_image.jpg", id="I")
        yield EnGlyphText("Caption Text", id="T")


# uv run testing/image_test.py
if __name__ == "__main__":
    # with pyinstrument.profile():
    Test().run()
```

Happy Coding!
