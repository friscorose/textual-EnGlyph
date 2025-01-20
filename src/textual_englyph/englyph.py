'''Create large text output module for Textual with custom widget EnGlyph'''

from PIL import Image
import os
from typing import List

from rich.console import Console, RenderableType
from rich.segment import Segment
from rich.text import Text

from textual.strip import Strip
from textual.widget import Widget

from .toglyxels import ToGlyxels

class EnGlyph( Widget, inherit_bindings=False ):
    '''
    Textual widget to show a variety of large text outputs.

    Args:
        renderable: Rich renderable or string to display
        basis:tuple[(2,4)], the (x,y) partitions of cell glyph pixels (glyxel | gx)
        pips:bool[False], show glyxels in reduced density
        font_size:int[12], set height of font in glyxels, ie. 12pt -> 12gx
        markup:bool[True], Rich Text inline console styling of string
        name:str, Standard Textual Widget argument
        id:str, Standard Textual Widget argument
        classes:str, Standard Textual Widget argument
        disabled:bool, Standard Textual Widget argument
    '''

    DEFAULT_CSS = """
    EnGlyph {
        height: auto;
        width: auto;
    }
    """

    # Rich Text or string for visual rendering to a slate
    _text = None
    # a PIL image for visual rendering to a slate
    _pane = None
    # a list[Strips] for the visual presence of cells
    _slate = None

    def __init__( # pylint: disable=R0902,R0913 # following would greatly increase complexity
                 self,
                 renderable,
                 *,
                 basis = (2,4),
                 pips = False,
                 font_name:str = "TerminusTTF-4.46.0.ttf",
                 font_size:int = 12,
                 markup: bool = True,
                 name: str | None = None,
                 id = None,
                 classes: str | None = None,
                 disabled: bool = False
                 ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.markup = markup
        self.basis = basis
        self.pips = pips
        self._font_name = font_name
        self._font_size = font_size
        self._enrender( renderable )
        #self.rich_style is not settled yet, trigger regenerate _slate_cache later
        self._encache()
        self._renderable = None

    def __add__( self, rhs ):
        """create the union of two EnGlyphed widgets """
        return self._union( self, rhs )

    __radd__ = __add__

    def __sub__( self, rhs ):
        """create the difference of two EnGlyphed widgetslinux disables  """
        return self._difference( self, rhs )

    def __mul__( self, rhs ):
        """create the intersection of two EnGlyphed widgets """
        return self._intersection( self, rhs )

    def __str__(self) -> str:
        output = [strip.text for strip in self._slate_cache]
        return "\n".join( output )

    def _enrender(self, renderable: RenderableType|None = None) -> None:
        """A stub handler to style, if appropriate, an input for glyph processing"""
        pass

    def _encache(self) -> None:
        """A stub handler to accept an input for glyph processing"""
        pass

    def _enslate(self, slate ) -> None:
        """A stub handler to accept a slate for glyph processing"""
        if self.basis == (0,0):
            return [ Strip(strip) for strip in slate ]
        slate_buf = []
        for strip in slate:
            for seg in strip:
                pane = ToGlyxels.font_pane( seg.text, self._font_name, self._font_size )
                slate = ToGlyxels.pane2slate( pane, seg.style, self.basis, self.pips )
                slate_buf = ToGlyxels.slate_join( slate_buf, slate )
        return slate_buf

    def get_content_width(self,
                          container=None,
                          viewport=None):
        return self._slate_cache[0].cell_length

    def get_content_height(self,
                           container=None,
                           viewport=None,
                           width=None):
        return len( self._slate_cache )

    def update( self,
               renderable: RenderableType|None = None,
               basis: tuple|None = None,
               pips: bool|None = None,
               font_size: int|None = None
               ) -> None:
        """New display input"""
        self.basis = basis or self.basis
        self.pips = pips or self.pips
        self._font_size = font_size or self._font_size
        self._enrender( renderable )
        self._encache()
        self.refresh(layout=True)

    def render_line( self, y:int ) -> Strip:
        strip = Strip.blank(0)
        if self._renderable != self.renderable:
            self._encache()
        if y < self.get_content_height():
            strip = self._slate_cache[y]
        return strip

class EnGlyphText( EnGlyph ):
    """Process a textual renderable (including Rich.Text)"""
    def _enrender(self, renderable: RenderableType|None = None) -> None:
        """A stub handler to style, if appropriate, an input for glyph processing"""
        if renderable is not None:
            self.renderable = renderable
            if isinstance(renderable, str):
                if self.markup:
                    self.renderable = Text.from_markup(renderable)
                else:
                    self.renderable = Text(renderable)

    def _encache(self) -> None:
        """A stub handler to accept an input for glyph processing"""
        self.renderable.stylize_before( self.rich_style )
        self._renderable = self.renderable
        cons_slate = Console().render_lines( self.renderable, pad=False )
        self._slate_cache = self._enslate( cons_slate )

class EnGlyphSlate( EnGlyph ):
    """Process a list of Strips"""
    def _enrender(self, renderable: list[Strip]|None = None) -> None:
        """A stub handler to style, if appropriate, an input for glyph processing"""
        if renderable is not None:
            self.renderable = self._enslate( renerable )

    def _encache(self) -> None:
            self._slate_cache = self._renderable = self.renderable

class EnGlyphImage( EnGlyph ):
    """Process a PIL image into glyxels"""
    def _enrender(self, renderable = None) -> None:
        """A stub handler to style, if appropriate, an input for glyph processing"""
        if renderable is not None:
            if isinstance( renderable, str ):
                renderable = Image.open( renderable )
            renderable = renderable.resize((64,64)) 
            #renderable.show()
            self.renderable = ToGlyxels.frame2slate( renderable )

    def _encache(self) -> None:
            self._slate_cache = self._renderable = self.renderable
