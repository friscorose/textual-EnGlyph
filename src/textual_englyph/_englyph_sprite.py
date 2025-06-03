from ._englyph_image import EnGlyphImage
from .toglyxels import ToGlyxels, EnLoad

class EnGlyphSprite( EnGlyphImage ):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, repeat=0, **kwargs)

    def prior_frame( self, index ):
        self.pipeline_advance( -1 )

    def next_frame( self, index ):
        self.pipeline_advance( 1 )

    def show_frame( self, index ):
        self.pipeline_advance( 0 )

