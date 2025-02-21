'''Create large text output module for Textual with custom widget EnGlyph'''

from PIL import Image, ImageOps
import io



from .englyph import EnGlyph
from .toglyxels import ToGlyxels

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
        cell_width = self.parent.size.width or self.app.size.width
        cell_height = self.styles.max_height.cells
        bbox_x = self.basis[0] * cell_width
        bbox_y = self.basis[1] * cell_height
        im_size = (bbox_x, bbox_y)
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
