'''Boilerplate code for testing purposes'''
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText, EnGlyphImage

class Test(App):
    '''Test the basic englyph image use case'''
    DEFAULT_CSS ="""
    SCREEN {
        color: blue;
        background: blue;
    }
    #T {
        background: white 50%;
        position: relative;
        offset: 6 -1;
    }
    """
    def compose(self) -> ComposeResult:
        #yield EnGlyphImage( "testing/hopper.jpg" )
        #yield EnGlyphText( "'Grace' hopper.jpg" )
        yield EnGlyphImage( "testing/twirl.gif" )
        yield EnGlyphText( "The coup de grâce", id="T", font_size=7, font_name="casio-fx-9860gii.ttf", basis=(2,4) )

# uv run testing/image_test.py
if __name__ == "__main__":
    Test().run()
    #Test().run(inline=True, inline_no_clear=True)
