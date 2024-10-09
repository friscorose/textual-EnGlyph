from textual.widget import Widget
from textual.reactive import reactive
from textual.strip import Strip

from rich.segment import Segment
from rich.style import Style

class EnGlyph( Widget ):
    phrase = reactive("Hello from englyph!")
    fashion = reactive( Style.parse("default on default") )

    def on_click( self ) -> None:
        self.update( "It's George" )

    def update( self, phrase: str|None = None, fashion: Style|str|None = None ) -> None:
        self.phrase = phrase or self.phrase
        if isinstance( fashion, str ):
            self.fashion = Style.parse( fashion )
        else:
            self.fashion = fashion or self.fashion

    def render_line( self, row:int ) -> Strip:
        strip = Strip( [Segment(self.phrase, self.fashion)] )
        if row:
            strip = Strip.blank(0)
        return strip
