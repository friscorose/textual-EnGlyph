"""Boilerplate code for testing purposes"""

from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText


class Test(App):
    """Test console markup styling the englyph text use case"""

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
