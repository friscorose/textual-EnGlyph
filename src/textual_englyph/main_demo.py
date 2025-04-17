"""Boilerplate code for demo"""

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Button, TextArea
from textual_englyph import EnGlyphText

# pylint: disable=R0801
CONTENT = '''\
from textual.app import App, ComposeResult
from textual_englyph import EnGlyph

class Test(App):
    DEFAULT_CSS = """
    EnGlyph {
        color: green;
        text-style: underline;
        }
    """

    def compose(self) -> ComposeResult:
        yield EnGlyph("EnGlyph [blue]Textual!")

if __name__ == "__main__":
    app = Test()
    app.run()
'''


class MainDemo(App):
    """Test CSS and console markup styling the basic englyph use case"""

    TITLE = "EnGlyph_Demo"
    DEFAULT_CSS = """
    TextArea {
        min-height: 80%;
        width: 57;
        max-width: 57;
    }
    EnGlyphText {
        color: green;
        text-style: underline;
        }
    #choice {
        height: 10;
        align: center top;
    }
    """

    code = TextArea(CONTENT)
    code.read_only = True

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Vertical():
            with Horizontal(id="choice"):
                yield Button(str(EnGlyphText("PREV", font_size="small")))
                yield EnGlyphText("Examples")
                yield Button(str(EnGlyphText("NEXT")))
            with Horizontal():
                yield self.code
                yield EnGlyphText("EnGlyph [blue]Textual!", font_size="small")


def main_demo():
    """main_demo runner method"""
    app = MainDemo()
    app.run()


if __name__ == "__main__":
    main_demo()
