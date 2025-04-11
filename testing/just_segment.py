"""Boilerplate code for testing purposes"""

from textual.app import App, ComposeResult
from textual_englyph import EnSevSeg


class Test(App):
    """Test console markup styling the englyph text use case"""

    def compose(self) -> ComposeResult:
        yield EnSevSeg("[red]\uEDCF1415")

if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
