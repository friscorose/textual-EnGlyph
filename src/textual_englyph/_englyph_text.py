"""Create large text output module for Textual with custom widget EnGlyph"""

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
        "smaller": (-2, "", (0, 0)), # for dynamic update of relative text_size
        "xx-small": (0, "", (0, 0)),  # Unicode chars like ᵧ (0x1d67), not implimented
        "x-small": (1, "", (0, 0)),  # What your terminal normally uses
        "small": (8, "miniwi.ttf", (2, 4)),
        "medium": (7, "casio-fx-9860gii.ttf", (2, 4)),
        "large": (7, "casio-fx-9860gii.ttf", (2, 3)),
        "x-large": (12, "TerminusTTF-4.46.0.ttf", (2, 4)),
        "xx-large": (14, "TerminusTTF-4.46.0.ttf", (2, 4)),
        "xxx-large": (18, "TerminusTTF-4.46.0.ttf", (2, 4)),
        "larger": (+2, "", (0, 0)), # for dynamic update of relative text_size
    }

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        self._maybe_reset( self, *args, kwargs=kwargs )
        super().__init__( *args, basis=self._basis, **kwargs )

    def _maybe_reset( self, *args, kwargs ):
        """Setup the attributes used for displaying character glyphs"""
        # text_size presets font_size, font_name and basis
        self._maybe_default( 'text_size', 'x-small', kwargs=kwargs )
        # Allow overrides by calls
        self._maybe_default( 'font_size', self._config[self._text_size][0], kwargs=kwargs )
        self._maybe_default( 'font_name', self._config[self._text_size][1], kwargs=kwargs )
        self._maybe_default( 'basis', self._config[self._text_size][2], kwargs=kwargs )
        # Enable fancy text
        self._maybe_default( 'markup', True, kwargs=kwargs )

    def marking( self, renderable ):
        if self._markup:
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
