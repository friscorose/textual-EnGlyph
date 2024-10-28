'''Boilerplate code for demo'''
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual_englyph import EnGlyph

class MainDemo(App):
    '''Test CSS and console markup styling the basic englyph use case'''
    DEFAULT_CSS = """
    EnGlyph {
        color: green;
        text-style: underline;
        }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield EnGlyph("Hello [blue]Textual!")

def main_demo():
    '''main_demo runner method'''
    app = MainDemo()
    app.run()

if __name__ == "__main__":
    main_demo()
