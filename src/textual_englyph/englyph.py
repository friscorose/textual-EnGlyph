"""Create large text output module for Textual with custom widget EnGlyph"""
from rich.console import RenderableType

from textual.strip import Strip
from textual.widget import Widget


class EnPipe():
    """ A data structure for managing a slate(list'o'strips) sequence"""

    blank = [Strip.blank(0)]
    def __init__( self, slate=None ):
        self.aperiodic = False
        self.interval = 100/1000
        self.index = 0
        slate = slate or self.blank
        self.slates = { self.index:slate }

    def __iter__(self):
        return self

    def __next__(self):
        '''return the next slate in the pipeline'''
        if self.aperiodic:
            self.slates[ self.index ] = self.blank
        self.index = (self.index+1)%len(self.slates)
        return self.this()

    def __setitem__(self, key:int|float, value):
        '''enable slice/index assignment'''
        self.slates[ int(key) ] = value

    def __getitem__(self, key:int|float):
        '''enable slice/index access'''
        return self.slates[ int(key)%len(self.slates) ]

    def append(self, value):
        self.slates[ len(self.slates) ] = value

    def this(self, value=None ):
        '''Optionally change and return the current slate in the pipeline'''
        if value is not None:
            self.slates[ self.index ] = value
        return self.slates[ self.index ]


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


    def __init__(self, renderable, *args, **kwargs):
        self._maybe_default( 'slate_pipe', EnPipe(), kwargs=kwargs )
        self._maybe_default( 'basis', (2,4), kwargs=kwargs )
        self._maybe_default( 'pips', False, kwargs=kwargs )
        super().__init__( *args, **kwargs )
        self._predicate = self._preprocess( renderable )

    @property
    def _slate(self):
        return self._slate_pipe.this()

    @_slate.setter
    def _slate(self, renderable):
        self._slate_pipe.this( renderable )

    def on_mount(self) -> None:
        self._process()

    def get_content_width(self, container=None, viewport=None):
        return self._slate[0].cell_length

    def get_content_height(self, container=None, viewport=None, width=None):
        return len(self._slate)


    def __str__(self) -> str:
        output = self._predicate
        if not isinstance( output, str ):
            output = "Image Instance"
        if self._slate != EnPipe().blank:
            output = "\n".join( [strip.text for strip in self._slate] )
        return output

    def _maybe_reset( self, *arg, kwargs ):
        pass

    def _maybe_default( self, key, default, kwargs ):
        """Set obj _attribute to maybe kwargs value and remove from kwargs, or default"""
        _key = '_'+key
        attr_val = kwargs.pop(key, default )
        if attr_val is not None:
            setattr( self, _key, attr_val )
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

    def update(
        self,
        renderable: RenderableType | None = None,
        *args,
        **kwargs
    ) -> None:
        """New display input"""
        self._maybe_reset( *args, kwargs=kwargs )
        self._maybe_default( 'basis', self._basis, kwargs=kwargs )
        self._maybe_default( 'pips', self._pips, kwargs=kwargs )
        self._predicate = self._preprocess( renderable, *args, **kwargs )
        self._process()
        self.refresh(layout=True)

    def render_line(self, y: int) -> Strip:
        self._postprocess()
        strip = EnPipe().blank
        if y < self.get_content_height():
            strip = self._slate[y]
        return strip
