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
    EnGlyphText {
        color: green;
        text-style: underline;
        }
    """

    def compose(self) -> ComposeResult:
        yield EnGlyphText("EnGlyph [blue]Textual!", text_size="large")

if __name__ == "__main__":
    app = Test()
    app.run()
'''


class MainDemo(App):
    """Test CSS and console markup styling the basic englyph use case"""

    TITLE = "EnGlyph_Demo"
    DEFAULT_CSS = """\
    TextArea {
        min-height: 80%;
        max-width: 80;
    }
    EnGlyphText {
        color: green;
        width: auto;
        content-align-vertical: middle;
        padding: 1 2;
        &.title {
            text-style: underline;
            align: center middle;
        }
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
                yield Button(str(EnGlyphText("PREV", text_size="medium")))
                yield EnGlyphText("Examples", text_size="medium")
                yield Button(str(EnGlyphText("NEXT", text_size="medium")))
            with Horizontal():
                yield self.code
                yield EnGlyphText(
                    "EnGlyph [blue]Textual![/blue]",
                    text_size="large",
                    classes="title",
                )


def main_demo():
    """main_demo runner method"""
    app = MainDemo()
    app.run()


if __name__ == "__main__":
    main_demo()
