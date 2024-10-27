from textual_englyph import EnGlyph
from textual.app import App, ComposeResult

class Test(App):
    DEFAULT_CSS = """
    EnGlyph {
        height: 4;
        color: green;
        text-style: strike;
        }
    """

    def compose(self) -> ComposeResult:
        #yield EnGlyph("Hello [blue]Textual!")
        yield EnGlyph("Hello [u blue]Textual!")
        #yield EnGlyph("[u blue]Textual!")

if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
