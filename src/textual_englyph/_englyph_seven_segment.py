"""Create seven segment display output for Textual with custom widget EnGlyph"""

from ._englyph_text import EnGlyphText

class EnSevSeg(EnGlyphText):
    """Seven Segement Display"""

    DEFAULT_CSS = """
    EnSevSeg {
        color: red;
        background: #400000;
        border: outer black;
    }
    """
    null_pinput = 0xED00 #Unicode PUA offset for pinput in EmSevSeg.ttf

    _config = {
        "smaller": (-2, "", (0, 0)), # for dynamic update of relative text_size
        "x-small": (1, "", (0, 0)),  # What your terminal normally uses
        "small": (8, "EnSevSeg_8x5.ttf", (2, 4)),
        "larger": (+2, "", (0, 0)), # for dynamic update of relative text_size
    }

    def __init__(
        self,
        *args,
        pinput: int|tuple|list|None = None,
        text_size: str|None = "small",
        **kwargs,
    ):
        super().__init__(
                *args,
                text_size=text_size,
                **kwargs)

    def _pinput2string( self, pinput ):
        pass

