'''Create large text output module for Textual with custom widget EnGlyph'''

from PIL import Image
import io
import os
from typing import List

from rich.console import Console, RenderableType
from rich.segment import Segment
from rich.text import Text

from textual.reactive import reactive
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
        color: $text;
        height: auto;
        width: auto;
    }
    """

    def __init__(self, renderable,
                 *args, 
                 basis = (2,4),
                 pips = False,
                 **kwargs ):
        super().__init__( *args, **kwargs )
        self._predicate = self._preprocess( renderable )
        self.basis = basis
        self.pips = pips
        self._process()
        self._postprocess()

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

    def __div__( self, rhs ):
        """create the intersection of two EnGlyphed widgets """
        return self._disection( self, rhs )

    def _intersection( self, rhs ):
        if isinstance( rhs, float ):
            pass

    def __str__(self) -> str:
        output = [strip.text for strip in self._slate_cache]
        return "\n".join( output )

    def _preprocess(self) -> None:
        """A stub handler for processing the input _predicate to the renderable"""
        pass

    def _process(self) -> None:
        """A stub handler for processing a renderable"""
        pass

    def _postprocess(self) -> None:
        """A stub handler to cache a slate (list of strips) for rendering"""
        pass

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
        self._preprocess( renderable )
        self._process()
        self._postprocess()
        self.refresh(layout=True)

    def on_mount( self ):
        self._process()
        self._postprocess()

    def render_line( self, y:int ) -> Strip:
        return self._slate_cache[y]

class EnGlyphText( EnGlyph ):
    """Process a textual renderable (including Rich.Text)"""
    def __init__(self, *args, 
                 markup: bool = True,
                 font_name:str = "TerminusTTF-4.46.0.ttf",
                 font_size:int = 12,
                 **kwargs ):
        self.markup = markup
        self._font_name = font_name
        self._font_size = font_size
        super().__init__( *args, **kwargs )

    def _preprocess(self, renderable: RenderableType|None = None):
        """A stub handler for processing the input _predicate to the renderable"""
        if renderable is not None:
            self.renderable = renderable
            if isinstance(renderable, str):
                if self.markup:
                    self.renderable = Text.from_markup(renderable)
                else:
                    self.renderable = Text(renderable)
        return renderable

    def _process(self) -> None:
        """A stub handler for processing a renderable"""
        self.renderable.stylize_before( self.rich_style )
        self._renderable = self.renderable

    def _postprocess(self) -> None:
        """A stub handler to cache a slate (list of strips) from _renderable"""
        slate = Console().render_lines( self._renderable, pad=False )
        slate_buf = []
        if self.basis == (0,0):
            slate_buf = [ Strip(strip) for strip in slate ]
        else:
            for strip in slate:
                for seg in strip:
                    pane = ToGlyxels.font_pane( seg.text, self._font_name, self._font_size )
                    slate = ToGlyxels.pane2slate( pane, seg.style, self.basis, self.pips )
                    slate_buf = ToGlyxels.slate_join( slate_buf, slate )
        self._slate_cache = slate_buf
        return


class EnGlyphSlate( EnGlyph ):
    """Process a list of Strips (or a widget?)"""
    def _enrender(self, renderable: list[Strip]|None = None) -> None:
        """A stub handler to pre-render an input for glyph processing"""
        if renderable is not None:
            self.renderable = self._enslate( renerable )

    def _encache(self) -> None:
            self._slate_cache = self._renderable = self.renderable

class EnGlyphImage( EnGlyph ):
    """Process a PIL image (or path to) into glyxels"""
    def __init__(self, *args,
                 repeat:int=3,
                 **kwargs ):
        self._repeats_n = repeat
        super().__init__( *args, **kwargs )


    animate = reactive(False, init=False)

    def on_mount(self) -> None:
        if self.animate:
            max_frames = self._repeats_n * self._frames_n
            self.interval_update = self.set_interval(
                    interval = self._duration_s,
                    callback = self.next_frame,
                    repeat = max_frames
                    ) 

    def previous_frame(self) -> None:
        if self.animate:
            current_frame = self._renderable.tell()
            if current_frame - 1 >= 0:
                self._renderable.seek( current_frame - 1 )
            else:
                self._renderable.seek( self._frames_n )
                self._postprocess()
                self.refresh(layout=True)

    def next_frame(self) -> None:
        current_frame = self._renderable.tell()
        if self.animate:
            if current_frame + 1 < self._frames_n:
                self._renderable.seek( current_frame + 1 )
            else:
                self._renderable.seek( 0 )
            self._postprocess()
            self.refresh(layout=True)

    def _preprocess(self, renderable = None) -> None:
        """A stub handler to pre-render an "image" input for glyph processing"""
        if renderable is not None:
            im_buff = renderable
            if isinstance( renderable, str ):
                #Load PIL image from file path
                with open( renderable, 'rb') as fh:
                    im_data = fh.read()
                    im_buff = io.BytesIO( im_data )
            self.renderable = Image.open( im_buff )
        return renderable

    def _process(self ) -> None:
        self._frames_n = self._get_frame_count( self.renderable )
        if self._frames_n > 0:
            self.animate = True
            self._duration_s = self.renderable.info.get("duration", 100)/1000
        self._renderable = self.renderable

    def _postprocess(self) -> None:
        """A stub handler to cache a slate (list of strips) from _renderable"""
        frame = self._renderable
        if self.animate:
            frame = self._renderable.convert('RGB')
            frame = frame.reduce( 4 )
        self._slate_cache = ToGlyxels.image2slate( frame, basis=self.basis, pips=self.pips )

    def _get_frame_count( self, image ):
        frames_n = 0
        image.seek(0)
        while True:
            try:
                image.seek(frames_n + 1)
                frames_n += 1
            except EOFError:
                break
        image.seek(0)
        return frames_n
