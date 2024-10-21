from .toglyxels import ToGlyxels

from textual.widget import Widget
from textual.reactive import reactive
from textual.strip import Strip

from rich.console import RenderableType
from rich.segment import Segment
from rich.style import Style


class EnGlyph( Widget, inherit_bindings=False ):
    def __init__( self,
                 phrase: RenderableType = "",
                 *,
                 basis = (2,4),
                 pips = False,
                 name: str | None = None,
                 id: str | None = None,
                 classes: str | None = None,
                 disabled: bool = False,
                 ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.phrase = str( phrase )
        self.basis = basis
        self.pips = pips
        self._strips_cache = None
        self.update()

    def on_click( self ) -> None:
        self.update( "It's George" )

    def update( self, phrase: str|None = None, basis: str|None = None ) -> None:
        """New display input"""
        self.phrase = phrase or self.phrase
        self.basis = basis or self.basis
        self._strips_cache = ToGlyxels.from_string( self.phrase, self.basis, self.pips )
        self.refresh(layout=True)

    def render_line( self, row:int ) -> Strip:
        strip = Strip.blank(0)
        if self._strips_cache is not None and row < len( self._strips_cache ):
            strip = self._strips_cache[row]
        return strip

