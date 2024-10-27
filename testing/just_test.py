from textual_englyph import EnGlyph
from textual.app import App, ComposeResult

class Test(App):
    DEFAULT_CSS = """
    EnGlyph {
        color: green;
        text-style: underline;
        }
    """

    def compose(self) -> ComposeResult:
        yield EnGlyph("Hello [blue]Textual!")

if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
