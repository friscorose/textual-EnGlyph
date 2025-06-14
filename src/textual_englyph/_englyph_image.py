"""Create large text output module for Textual with custom widget EnGlyph"""

from contextlib import suppress
from PIL import ImageOps

from textual import work

from .englyph import EnGlyph
from .toglyxels import ToGlyxels, EnLoad


class EnGlyphImage(EnGlyph):
    """A Textual widget to process a PIL image (or path to) into glyxels.
        Args:
            renderable (PIL Image | path str): The image to be displayed.
            basis (tuple int,int): Glyph pixel (glyxel) partitions in x then y.
            pips (Bool): Are glyxels partition filling or not.
            repeat (int): Number of times an animated image loops.
            Standard Textual Widget Args.
            
        Returns:
            Textual Widget Instance.
    """

    DEFAULT_CSS = """
    EnGlyphImage {
        max-height: 32;
    }
    """

    def __init__(self, *args, repeat: int = 3, **kwargs):
        self.animate = 0
        self._repeats_n = repeat
        super().__init__(*args, **kwargs)

    def pipeline_show(self, index:int = 1 ) -> None:
        self._slate_pipe.show( index )
        self.refresh(layout=True)

    def pipeline_advance(self, frames:int = 1 ) -> None:
        _ = self._slate_pipe.step( frames )
        self.refresh(layout=True)

    def enable_animate(self):
        if self.animate != 0:
            self.animate_timer.reset()
            self.animate_timer.resume()

    def _preprocess(self, pil_img=None) -> None:
        """init handler to preset PIL image(renderable) properties for glyph processing"""
        if pil_img is not None:
            self.renderable = EnLoad( pil_img )
        self._frames_n = self._get_frame_count(self.renderable)
        #raise AttributeError( self._frames_n )
        #raise AttributeError( self._repeats_n )
        if self._repeats_n > 0:
            self.animate = 1 # animation steps per frame
            self._duration_s = self.renderable.info.get("duration", 100) / 1000
        return pil_img

    def _process(self) -> None:
        """An on_mount (DOM ready) handler for "image" glyph processing"""
        self._pipeline_init()
        if self.animate != 0:
            max_frames = self._repeats_n * self._frames_n - 1
            self.animate_timer = self.set_interval(
                interval=self._duration_s,
                callback=self.pipeline_advance,
                repeat=max_frames,
                pause=True
            )

    def _pipeline_init(self) -> None:
        if isinstance( self.renderable, list ):
            self.load_pipe( self.renderable[0], self._slate_pipe.this )
        else:
            self.load_pipe( self.renderable, self._slate_pipe.this )
        if self._frames_n > 0:
            self._pipeline_fill( self.renderable )

    @work(exclusive=True, thread=True )
    def _pipeline_fill(self, renderable) -> None:
        for idx in range( 1, self._frames_n ):
            if isinstance( renderable, list ):
                self.load_pipe( renderable[ idx ], self._slate_pipe.append )
            else:
                renderable.seek( idx )
                self.load_pipe( renderable, self._slate_pipe.append )
        if self._repeats_n > 0:
            self.enable_animate()

    def load_pipe(self, img, pipe ):
        #raise AttributeError( self._repeats_n )
        frame = self._rescale_img(img.convert("RGB"))
        slate = ToGlyxels.image2slate( frame, basis=self._basis, pips=self._pips)
        pipe( slate )

    def _rescale_img(self, img) -> None:
        """Contain the image within CSS height or width keeping aspect ratio or fit image if both
        if max-height or max-width is specified the crop the image to the max dimension."""
        use_width = use_height = False
        cell_width = cell_height = 1

        with suppress(AttributeError):
            cell_width = self.styles.width.cells
            if cell_width is not None:
                use_width = True
            else:
                cell_width = self.styles.max_width.cells 

        with suppress(AttributeError):
            cell_height = self.styles.height.cells
            if cell_height is not None:
                use_height = True
            else:
                cell_height = self.styles.max_height.cells

        cell_width = cell_width or self.parent.size.width or self.app.size.width
        cell_height = cell_height or self.parent.size.height

        im_size = (self._basis[0] * cell_width, self._basis[1] * cell_height)
        if use_width and use_height:
            im_data = img.resize( im_size )
        else:
            im_data = ImageOps.contain(img, im_size)

        return im_data

    def _get_frame_count(self, images):
        if isinstance( images, list ):
            return len( images )
        frames_n = 0
        try:
            images.seek(0)
            while True:
                try:
                    images.seek(frames_n + 1)
                    frames_n += 1
                except EOFError:
                    break
            images.seek(0)
        finally:
            return frames_n + 1
