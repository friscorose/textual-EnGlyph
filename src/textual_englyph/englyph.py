from textual.widget import Widget
from textual.reactive import reactive
from textual.strip import Strip

from rich.segment import Segment
from rich.style import Style

class EnGlyph( Widget ):
    phrase = reactive("Hello from englyph!")

    def on_click( self ) -> None:
        self.update( "It's George" )

    def update( self, text) -> None:
        self.phrase = text

    def render_line( self, row:int) -> Strip:
        if row > 0:
            return Strip.blank(1)
        return Strip( [Segment(self.phrase, Style.parse("default on default"))], 18 )
