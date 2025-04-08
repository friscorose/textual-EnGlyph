# Textual-EnGlyph
A large font and image rendering widget for the Textual platform.

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

Install and import the text widget
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
        yield EnGlyphText("From Englyph, Hello [violet]Textual!", text_size="small")

if __name__ == "__main__":
    Test().run()
```
and run it (use ctrl-q to exit)
```bash
uv run text.py
```

See Overview.md for more information regarding EnGlyph capabilities.
