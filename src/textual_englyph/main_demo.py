'''Boilerplate code for demo'''
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Button, TextArea
from textual_englyph import EnGlyph

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
    '''Test CSS and console markup styling the basic englyph use case'''
    TITLE = "EnGlyph_Demo"
    DEFAULT_CSS = """
    TextArea {
        min-height: 80%;
        width: 57;
        max-width: 57;
    }
    EnGlyph {
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
                yield Button( str(EnGlyph("PREV")) )
                yield EnGlyph("Examples")
                yield Button( str(EnGlyph("NEXT")) )
            with Horizontal():
                yield self.code
                yield EnGlyph("EnGlyph [blue]Textual!")

def main_demo():
    '''main_demo runner method'''
    app = MainDemo()
    app.run()

if __name__ == "__main__":
    main_demo()
