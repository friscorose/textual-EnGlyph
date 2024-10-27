from .toglyxels import ToGlyxels

from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget

from rich.console import RenderableType
from rich.segment import Segment
from rich.style import Style
from rich.text import Text
from rich.traceback import install
install()

class EnGlyph( Widget, inherit_bindings=False ):
    DEFAULT_CSS = """
    EnGlyph {
        height: auto;
        width: auto;
    }
    """

    def __init__( self,
                 renderable: RenderableType = "",
                 *,
                 basis = (2,4),
                 pips = False,
                 markup: bool = True,
                 name: str | None = None,
                 id: str | None = None,
                 classes: str | None = None,
                 disabled: bool = False,
                 ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.markup = markup
        self.basis = basis
        self.pips = pips
        self._engender( renderable )
        #self.rich_style is not settled yet, trigger regenerate _strip_cache later
        self._renderable = None

    def get_content_width(self, a, b):
        return self._strips_cache[0].cell_length

    def get_content_height(self, a=None, b=None, c=None):
        return len( self._strips_cache )

    def _engender(self, renderable: RenderableType|None = None) -> None:
        if renderable is not None:
            self.renderable = renderable
            if isinstance(renderable, str):
                if self.markup:
                    self.renderable = Text.from_markup(renderable)
                else:
                    self.renderable = Text(renderable)
        self.renderable.stylize_before( self.rich_style )
        self._renderable = self.renderable
        self._strips_cache = ToGlyxels.from_renderable( self.renderable, self.basis, self.pips )

    def update( self, renderable: RenderableType|None = None, basis: tuple|None = None, pips: bool|None = None ) -> None:
        """New display input"""
        self.basis = basis or self.basis
        self.pips = pips or self.pips
        self._engender( renderable )
        self.refresh(layout=True)

    def render_line( self, row:int ) -> Strip:
        strip = Strip.blank(0)
        if row == self.get_content_height() or self._renderable != self.renderable:
            self._engender()
        if row < self.get_content_height():
            strip = self._strips_cache[row]
        return strip

