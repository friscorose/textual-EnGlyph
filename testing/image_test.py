"""Boilerplate code for testing purposes"""

# import pyinstrument
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphText, EnGlyphImage


class Test(App):
    """Test the basic englyph image use case"""

    DEFAULT_CSS = """
    #I {
        height: 32;
    }
    #T {
        background: white 20%;
        padding: 1;
        position: relative;
        offset: 34 -3;
    }
    """

    def compose(self) -> ComposeResult:
        yield EnGlyphImage("testing/hopper.jpg", id="I")
        yield EnGlyphText("'Grace' hopper.jpg", id="T")
        #yield EnGlyphImage( "testing/twirl.gif", id="I" )
        #yield EnGlyphText( " Coup de Grâce ", id="T", text_size="medium" )

    def on_key( self, event ):
        img = self.query_one( "#I" )
        if event.key == "full_stop":
            img.pipeline_advance()
        elif event.key == "comma":
            img.pipeline_advance( -1 )
        self.notify( event.key )
            #img._pipeline_retard()

# uv run testing/image_test.py
if __name__ == "__main__":
    # with pyinstrument.profile():
    Test().run()
    #Test().run(inline=True, inline_no_clear=True)
