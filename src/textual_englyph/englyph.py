from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Static
from textual.reactive import reactive
from textual.strip import Strip

from rich.console import Console
from rich.segment import Segment
from rich.style import Style

class EnGlyph( Widget ):

    def render_line( self, row:int)-> Strip:
        if row > 0:
            return Strip.blank(1)
        return Strip( [Segment("Hello from englyph!", Style.parse("default on default"))], 18 )
