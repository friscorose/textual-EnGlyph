from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.reactive import reactive
from textual.strip import Strip

from rich.console import Console
from rich.segment import Segment
from rich.style import Style

class EnGlyph( Static ):

    def on_mount(self):
        self.update("Hello from englyph!")

class Test(App):

    def compose(self) -> ComposeResult:
        yield EnGlyph()

if __name__ == "__main__":
    Test().run()
