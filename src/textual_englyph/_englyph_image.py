"""Create large text output module for Textual with custom widget EnGlyph"""

from PIL import ImageOps

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
        max-height: 24;
    }
    """

    def __init__(self, *args, repeat: int = 3, **kwargs):
        self._repeats_n = repeat
        super().__init__(*args, **kwargs)

    animate = False

    def _rescale_img(self, img) -> None:
        """Contain the image within height or width keeping aspect ratio or fit image if both"""
        use_width = use_height = False
        try:
            cell_width = self.styles.width.cells
            if cell_width is not None:
                use_width = True
            else:
                cell_width = self.styles.max_width.cells 
        except:
            pass

        try:
            cell_height = self.styles.height.cells
            if cell_height is not None:
                use_height = True
        except:
            pass

        cell_width = cell_width or self.parent.size.width or self.app.size.width
        cell_height = cell_height or self.styles.max_height.cells

        im_size = (self.basis[0] * cell_width, self.basis[1] * cell_height)
        if use_width and use_height:
            im_data = img.resize( im_size )
        else:
            im_data = ImageOps.contain(img, im_size)

        return im_data

    def _update_frame(self, image_frame=None) -> None:
        """accept an image frame to show or move to the next image frame in a sequence"""
        current_frame = self._renderable.tell()
        if image_frame is not None:
            frame = image_frame
        else:
            frame = self._renderable
            if self.animate != 0:
                next_frame = (current_frame + self.animate) % (self._frames_n + 1)
                frame.seek(next_frame)
        self._dblbuff_push(self._rescale_img(frame.convert("RGB")))

    def _dblbuff_init(self) -> None:
        frame = self._rescale_img(self._renderable.convert("RGB"))
        self._slate_cache = ToGlyxels.image2slate(
            frame, basis=self.basis, pips=self.pips
        )
        self._slate = self._slate_cache

    def _dblbuff_push(self, frame) -> None:
        self._slate = self._slate_cache
        self.refresh(layout=True)
        self._slate_cache = ToGlyxels.image2slate(
            frame, basis=self.basis, pips=self.pips
        )

    def _preprocess(self, renderable=None) -> None:
        """A stub init handler to preset "image" properties for glyph processing"""
        if renderable is not None:
            self._renderable = EnLoad( renderable )
        self._frames_n = self._get_frame_count(self._renderable)
        if self._frames_n > 0:
            self.animate = 1
            self._duration_s = self._renderable.info.get("duration", 100) / 1000
        else:
            self.animate = 0
        return renderable

    def _process(self) -> None:
        """A stub on_mount (DOM ready) handler for "image" glyph processing"""
        self._dblbuff_init()
        if self.animate != 0:
            max_frames = self._repeats_n * (self._frames_n + 1)
            self.interval_update = self.set_interval(
                interval=self._duration_s,
                callback=self._update_frame,
                repeat=max_frames,
            )

    def _get_frame_count(self, image):
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
