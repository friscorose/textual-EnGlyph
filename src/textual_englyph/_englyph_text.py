"""Create large text output module for Textual with custom widget EnGlyph"""
from collections import deque, namedtuple

from rich.console import Console, RenderableType
from rich.text import Text

from textual.strip import Strip

from .englyph import EnGlyph
from .toglyxels import ToGlyxels


class EnGlyphText(EnGlyph):
    """
    A Textual widget to show a variety of large text outputs.
    Process a textual renderable (including Rich.Text)
    Args:
        renderable: Rich renderable or string to display
        text_size:str["medium"], choose size configuration of font
        pips:bool[False], show glyxels in reduced density
        font_name:str[TerminusTTF-4.46.0.ttf], set name/path for font shown in glyxels
        font_size:int[12], set height of font in glyxels, ie. 12pt -> 12gx
        markup:bool[True], Rich Text inline console styling of string
        name:str, Standard Textual Widget argument
        id:str, Standard Textual Widget argument
        classes:str, Standard Textual Widget argument
        disabled:bool, Standard Textual Widget argument
    """


    _config = {
        #"xx-small": (0, "", (0, 0)),  # Unicode text like ᵧ (0x1d67), future use
        "x-small": (1, "", (0, 0)),  # What your terminal normally uses
        "small": (8, "miniwi.ttf", (2, 4)),
        "medium": (7, "casio-fx-9860gii.ttf", (2, 4)),
        "large": (12, "TerminusTTF-4.46.0.ttf", (2, 4)),
        "x-large": (14, "TerminusTTF-4.46.0.ttf", (2, 4)),
        "xx-large": (16, "TerminusTTF-4.46.0.ttf", (2, 4)),
        "xxx-large": (18, "TerminusTTF-4.46.0.ttf", (2, 4)),
        "custom": (None, None, None)
    }


    # All values are integer glyxel counts
    SlugSet= namedtuple( 'SlugSet', ['basis', 'points', 'font', 'leading', 'tracking'] )
    _settings = {  
        # Unicode text like ᵧ (0x1d67), future use
        #"xx-small": SlugSet( basis=(0,0), points=0, font="", leading=1, tracking=1 ),
        # What your terminal normally uses
        "x-small": SlugSet( basis=(0,0), points=0, font="", leading=1, tracking=1 ),
        "small": SlugSet( basis=(2,4), points=8, font="miniwi.ttf", leading=8, tracking=1 ),
        "medium": SlugSet( basis=(2,4), points=7, font="casio-fx-9860gii.ttf", leading=8, tracking=1 ),
        "large": SlugSet( basis=(2,4), points=12, font="TerminusTTF-4.46.0.ttf", leading=12, tracking=1 ),
        "x-large": SlugSet( basis=(2,4), points=14, font="TerminusTTF-4.46.0.ttf", leading=16, tracking=1 ),
        "xx-large": SlugSet( basis=(2,4), points=18, font="TerminusTTF-4.46.0.ttf", leading=20, tracking=2 ),
        "xxx-large": SlugSet( basis=(2,4), points=20, font="TerminusTTF-4.46.0.ttf", leading=24, tracking=2 ),
        "custom": None
    }


    def __init__(
        self,
        *args,
        **kwargs,
    ):
        self._glyph_state = deque( self._config )
        self._maybe_default( 'text_size', 'x-small', kwargs=kwargs )
        self._maybe_reset( self, *args, kwargs=kwargs )
        super().__init__( *args, basis=self._basis, **kwargs )

    @property
    def _text_size(self):
        return self._glyph_state[0]

    @_text_size.setter
    def _text_size(self, size_key: str ):
        try:
            if size_key == "custom":
                custom_idx = self._glyph_state.index( size_key )
                self._glyph_state.rotate( -custom_idx )
            elif size_key == "larger" or size_key == "smaller":
                """relative size adjustment logic"""
                if self._glyph_state[0] == "custom":
                    """predefined font config or custom?"""
                    if size_key == "larger":
                        self._maybe_default( 'font_size', self._font_size +2, {} )
                    else:
                        """smaller"""
                        self._maybe_default( 'font_size', self._font_size -2, {} )
                        #need logic to re-attach to defined configs if possible
                else:
                    if size_key == "larger":
                        if self._glyph_state[1] == "custom":
                            self._maybe_default( 'font_size', self._font_size +2, {} )
                        self._glyph_state.rotate( -1 )
                    else:
                        """smaller"""
                        if self._glyph_state[-1] != "custom":
                            self._glyph_state.rotate( 1 )
                            size_key = self._glyph_state[0]
                            self._maybe_default( 'font_size', self._config[size_key][0], {} )
                            self._maybe_default( 'font_name', self._config[size_key][1], {} )
                            self._maybe_default( 'basis', self._config[size_key][2], {} )
            else:
                """absolute size logic"""
                glyph_idx = self._glyph_state.index( size_key )
                self._glyph_state.rotate( -glyph_idx )
                self._maybe_default( 'font_size', self._config[size_key][0], {} )
                self._maybe_default( 'font_name', self._config[size_key][1], {} )
                self._maybe_default( 'basis', self._config[size_key][2], {} )
        except ValueError:
            raise ValueError

    def _maybe_reset( self, *args, kwargs ):
        """Setup the attributes used for displaying character glyphs"""
        # text_size presets font_size, font_name and basis
        self._maybe_default( 'text_size', self._text_size, kwargs=kwargs )
        # Allow overrides by specified attributes
        self._maybe_default( 'font_size', self._config[self._text_size][0], kwargs=kwargs )
        self._maybe_default( 'font_name', self._config[self._text_size][1], kwargs=kwargs )
        self._maybe_default( 'basis', self._config[self._text_size][2], kwargs=kwargs )
        # Enable fancy text
        self._maybe_default( 'markup', True, kwargs=kwargs )

    def marking( self, renderable ):
        if self._markup:
            #raise AttributeError( Text.from_markup(renderable) )
            return Text.from_markup(renderable)
        else:
            return Text(renderable)

    def chalking( self ):
        """A handler for processing the renderable to a slate (list of strips)"""
        slate = Console().render_lines(self.renderable, pad=False)
        slate_buf = []
        if self._basis == (0, 0):
            slate_buf = [Strip(strip) for strip in slate]
        else:
            for strip in slate:
                for seg in strip:
                    pane = ToGlyxels.font_pane( seg.text, self._font_name, self._font_size)
                    slate = ToGlyxels.pane2slate(pane, seg.style, self._basis, self._pips)
                    slate_buf = ToGlyxels.slate_join(slate_buf, slate)
        return slate_buf

    def _preprocess(self, renderable: RenderableType | None = None, *args, **kwargs ):
        """A stub handler for processing the input _predicate to the renderable"""
        if renderable is None:
            renderable = self._predicate
        self.renderable = self.marking( renderable )
        self._slate = self.chalking()
        return renderable

    def _process(self) -> None:
        """A stub handler to cache a slate (list of strips) from renderable"""
        self.renderable.stylize_before(self.rich_style)
        # raise AttributeError( "" )
        self._slate = self.chalking()
