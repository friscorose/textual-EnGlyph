"""Create large text output module for Textual with custom widget EnGlyph"""

from rich.console import RenderableType

from rich.text import Text
from textual.strip import Strip
from textual.widget import Widget


class EnGlyph(Widget, inherit_bindings=False):
    """
    Textual widget to show a variety of large text outputs.

    Args:
        renderable: Rich renderable or string to display
        basis:tuple[(2,4)], the (x,y) partitions of cell glyph pixels (glyxel | gx)
        pips:bool[False], show glyxels in reduced density

        name:str, Standard Textual Widget argument
        id:str, Standard Textual Widget argument
        classes:str, Standard Textual Widget argument
        disabled:bool, Standard Textual Widget argument
    """

    DEFAULT_CSS = """
    EnGlyph {
        color: $text;
        height: auto;
        width: auto;
    }
    """

    _empty_slate = [Strip.blank(0)]
    _slate = _slate_cache = _empty_slate
    _pane = None

    def __init__(self, renderable, *args, basis=(2, 4), pips=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.basis = basis
        self.pips = pips
        self._predicate = self._preprocess(renderable)

    def on_mount(self) -> None:
        self._process()

    def get_content_width(self, container=None, viewport=None):
        return self._slate[0].cell_length

    def get_content_height(self, container=None, viewport=None, width=None):
        return len(self._slate)

    def __add__(self, rhs):
        """create the union of two EnGlyphed widgets"""
        # return self._union( self, rhs )
        pass

    __radd__ = __add__

    def __sub__(self, rhs):
        """create the difference of two EnGlyphed widgetslinux disables"""
        return self._difference(self, rhs)

    def __mul__(self, rhs):
        """create the intersection of two EnGlyphed widgets"""
        return self._intersection(self, rhs)

    def __div__(self, rhs):
        """create the intersection of two EnGlyphed widgets"""
        return self._disection(self, rhs)

    def _union(self, rhs):
        for idy, strip in enumerate(rhs._slate):
            for idx, seg in enumerate(strip):
                pass

    def _intersection(self, rhs):
        if isinstance(rhs, float):
            pass

    def __str__(self) -> str:
        output = self._predicate
        if self._slate != self._empty_slate:
            output = "\n".join( [strip.text for strip in self._slate] )
        return output

    def _maybe_default( self, key, default, kwargs ):
        _key = '_'+key
        self_val = attr_val = default
        if hasattr( self, key ):
            self_val = getattr( self, _key )
            attr_val = kwargs.pop(key, self_val )
            setattr( self, _key, attr_val )
        else:
            attr_val = kwargs.pop(key, default )
            setattr( self, _key, attr_val )
        #raise AttributeError( attr_val )
        return getattr( self, _key )

    def _preprocess(self) -> None:
        """A stub handler for processing the input _predicate to the renderable"""
        pass

    def _process(self) -> None:
        """A stub handler for processing a renderable"""
        pass

    def _postprocess(self) -> None:
        """A stub handler to cache a slate (list of strips) for rendering"""
        pass

    def toPane( self, renderable = None, withStyle=False ):
        pass

    def toSlate( self, pane ):
        pass

    def update(
        self,
        renderable: RenderableType | None = None,
        *args,
        **kwargs
    ) -> None:
        """New display input"""
        self.basis = kwargs.pop( 'basis', self.basis )
        self.pips = kwargs.pop( 'pips', self.pips )
        self._font_size = kwargs.pop( 'font_size', self._font_size )
        self._predicate = self._preprocess( renderable, *args, **kwargs )
        self._process()
        self.refresh(layout=True)

    def render_line(self, y: int) -> Strip:
        self._postprocess()
        strip = Strip.blank(0)
        if y < self.get_content_height():
            strip = self._slate[y]
        return strip
