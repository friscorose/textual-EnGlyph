from textual_englyph import EnGlyph
from textual.app import App, ComposeResult

class Test(App):
    DEFAULT_CSS = """
    EnGlyph {
        height: 10;
        color: green;
        }
    """

    def compose(self) -> ComposeResult:
        yield EnGlyph("Hello [blue]Textual!")

if __name__ == "__main__":
    Test().run(inline=True)
