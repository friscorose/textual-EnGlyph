'''Create large text output module for Textual with custom widget EnGlyph'''

from PIL import Image, ImageOps
import io
import os
from typing import List

from rich.console import Console, RenderableType
from rich.segment import Segment
from rich.text import Text

from textual.geometry import Size
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

    _slate = _slate_cache = [Strip.blank(0)]

    def __init__(self, renderable,
                 *args, 
                 basis = (2,4),
                 pips = False,
                 **kwargs ):
        super().__init__( *args, **kwargs )
        self.basis = basis
        self.pips = pips
        self._predicate = self._preprocess( renderable )

    def on_mount( self ):
        self._process()

    def get_content_width(self,
                          container=None,
                          viewport=None):
        return self._slate[0].cell_length

    def get_content_height(self,
                           container=None,
                           viewport=None,
                           width=None):
        return len( self._slate )

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
        output = [strip.text for strip in self._slate]
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
        self._predicate = self._preprocess( renderable )
        self._process()
        self._postprocess()
        self.refresh(layout=True)

    def render_line( self, y:int ) -> Strip:
        self._postprocess()
        return self._slate[y]

class EnGlyphText( EnGlyph ):
    """
    A Textual widget to show a variety of large text outputs.
    Process a textual renderable (including Rich.Text)
    Args:
        renderable: Rich renderable or string to display
        size:str["medium"], choose size configuration of font
        basis:tuple[(2,4)], the (x,y) partitions of cell glyph pixels (glyxel | gx)
        pips:bool[False], show glyxels in reduced density
        font_name:str[TerminusTTF-4.46.0.ttf], set name/path for font shown in glyxels
        font_size:int[12], set height of font in glyxels, ie. 12pt -> 12gx
        markup:bool[True], Rich Text inline console styling of string
        name:str, Standard Textual Widget argument
        id:str, Standard Textual Widget argument
        classes:str, Standard Textual Widget argument
        disabled:bool, Standard Textual Widget argument
    """

    _size_config = {
            "smaller":( -2, "", (0,0) ),
            "larger":( +2, "", (0,0) ),

            "xx-small":( 0, "", (0,0) ), #Unicode chars like ᵧ (0x1d67), not implimented
            "x-small":( 1, "", (0,0) ), #What your terminal normally uses
            "small":( 8, "AtariSmall.ttf", (2,4) ),
            "medium":( 7, "casio-fx-9860gii.ttf", (2,4) ),
            "large":(  7, "casio-fx-9860gii.ttf", (2,3) ),
            "x-large":( 12, "TerminusTTF-4.46.0.ttf", (2,4) ),
            "xx-large":( 14, "TerminusTTF-4.46.0.ttf", (2,4) ),
            "xxx-large":( 16, "TerminusTTF-4.46.0.ttf", (2,4) ),
            }

    def __init__(self, *args, 
                 size: str = "x-small",
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
            self._renderable = renderable
            if isinstance(renderable, str):
                if self.markup:
                    self._renderable = Text.from_markup(renderable)
                else:
                    self._renderable = Text(renderable)
        return renderable

    def _process(self) -> None:
        """A stub handler for processing a renderable"""
        self._renderable.stylize_before( self.rich_style )

    def _postprocess(self) -> None:
        """A stub handler to cache a slate (list of strips) from renderable"""
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
        self._slate = slate_buf
        return

class EnGlyphDrawn( EnGlyph ):
    pass


class EnGlyphSlate( EnGlyph ):
    """Process a list of Strips (or a widget?)"""
    def _enrender(self, renderable: list[Strip]|None = None) -> None:
        """A stub handler to pre-render an input for glyph processing"""
        if renderable is not None:
            self._renderable = self._enslate( renerable )

    def _encache(self) -> None:
            self._slate = self._renderable

class EnGlyphImage( EnGlyph ):
    """Process a PIL image (or path to) into glyxels"""
    DEFAULT_CSS="""
    EnGlyphImage {
        max-height: 24;
    }
    """
    def __init__(self, *args,
                 repeat:int=3,
                 **kwargs ):
        self._repeats_n = repeat
        super().__init__( *args, **kwargs )


    animate = False

    def _rescale_img( self, img ) -> None:
        """Adjust the image by factor and to nearest full cell size and nearest aspect ratio"""
        ImgSize = Size( *img.size )
        cell_width = self.parent.size.width or self.app.size.width
        cell_height = self.styles.max_height.cells
        bbox_x = self.basis[0] * cell_width
        bbox_y = self.basis[1] * cell_height
        im_size = (bbox_x, bbox_y)
        #raise AttributeError( im_size )
        return ImageOps.contain( img, im_size )

    def _update_frame(self, image_frame = None) -> None:
        """accept an image frame to show or move to the next image frame in a sequence"""
        current_frame = self._renderable.tell()
        if image_frame is not None:
            frame = image_frame
        else:
            frame = self._renderable
            if self.animate != 0:
                next_frame = (current_frame + self.animate) % (self._frames_n + 1)
                frame.seek( next_frame )
        self._dblbuff_push( self._rescale_img( frame.convert('RGB') ) )

    def _dblbuff_init(self) -> None:
        frame = self._rescale_img( self._renderable.convert('RGB') )
        self._slate_cache = ToGlyxels.image2slate( frame, basis=self.basis, pips=self.pips )
        self._slate = self._slate_cache
        
    def _dblbuff_push(self, frame) -> None:
        self._slate = self._slate_cache
        self.refresh(layout=True)
        self._slate_cache = ToGlyxels.image2slate( frame, basis=self.basis, pips=self.pips )

    def _preprocess(self, renderable = None) -> None:
        """A stub init handler to preset "image" properties for glyph processing"""
        if renderable is not None:
            im_buff = renderable
            if isinstance( renderable, str ):
                #Load PIL image from file path
                with open( renderable, 'rb') as fh:
                    im_data = fh.read()
                    im_buff = io.BytesIO( im_data )
            self._renderable = Image.open( im_buff )
        self._frames_n = self._get_frame_count( self._renderable )
        if self._frames_n > 0:
            self.animate = 1
            self._duration_s = self._renderable.info.get("duration", 100)/1000
        else:
            self.animate = 0
        return renderable

    def _process(self ) -> None:
        """A stub on_mount (DOM ready) handler for "image" glyph processing"""
        self._dblbuff_init()
        if self.animate != 0:
            max_frames = self._repeats_n * (self._frames_n + 1)
            self.interval_update = self.set_interval(
                    interval = self._duration_s,
                    callback = self._update_frame,
                    repeat = max_frames
                    ) 

    def _postprocess(self) -> None:
        """A stub handler to cache a slate (list of strips) from renderable"""
        pass

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
