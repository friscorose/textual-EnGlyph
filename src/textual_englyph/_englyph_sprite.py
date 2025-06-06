from ._englyph_image import EnGlyphImage
from .toglyxels import ToGlyxels, EnLoad

class EnGlyphSprite( EnGlyphImage ):
    def __init__(self, *args, **kwargs):
        self.dragging = False
        super().__init__(*args, repeat=0, **kwargs)

    def prior_frame( self ):
        self.pipeline_advance( -1 )

    def next_frame( self ):
        self.pipeline_advance( 1 )

    def show_frame( self, index ):
        self.pipeline_show( index )

    def on_mouse_move(self, event):
        if self.dragging:
            self.offset = self.offset + event.delta

    def on_mouse_up(self):
        """clean up mouse handling"""
        self.dragging = False
        self.release_mouse()

    def on_mouse_down(self):
        self.dragging = True
        self.capture_mouse()
