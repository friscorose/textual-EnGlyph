'''Boilerplate code for testing purposes'''
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText, EnGlyphImage

class Test(App):
    '''Test the basic englyph image use case'''
    def compose(self) -> ComposeResult:
        yield EnGlyphImage( "testing/hopper.jpg" )
        yield EnGlyphText( "'Grace' hopper.jpg" )
        #yield EnGlyphImage( "testing/twirl.gif" )
        #yield EnGlyphText( "The coup de grâce" )

# uv run testing/image_test.py
if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
