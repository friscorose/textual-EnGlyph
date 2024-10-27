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
        self.renderable = self._enRich_string( renderable, markup )
        self.basis = basis
        self.pips = pips
        self._strips_cache = ToGlyxels.from_renderable( self.renderable, self.basis, self.pips )

    def get_content_width(self, a, b):
        return self._strips_cache[0].cell_length

    def get_content_height(self, a, b, c):
        return len( self._strips_cache )

    def _enRich_string(self, renderable: RenderableType, markup: bool=True) -> RenderableType:
        if isinstance(renderable, str):
            if markup:
                renderable = Text.from_markup(renderable)
            else:
                renderable = Text(renderable)
        return renderable

    def update( self, renderable: str|None = None, basis: str|None = None, pips: bool|None = None ) -> None:
        """New display input"""
        self.renderable = renderable or self.renderable
        self.basis = basis or self.basis
        self.pips = pips or self.pips
        self.refresh(layout=True)

    def render_line( self, row:int ) -> Strip:
        strip = Strip.blank(0)
        if row == 0:
            self.renderable.stylize_before( self.rich_style )
            self._strips_cache = ToGlyxels.from_renderable( self.renderable, self.basis, self.pips )
        if self._strips_cache is not None and row < len( self._strips_cache ):
            strip = self._strips_cache[row]

        return strip

