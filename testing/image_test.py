'''Boilerplate code for testing purposes'''
from PIL import Image
import os
from textual.app import App, ComposeResult
from textual_englyph import EnGlyphImage

class Test(App):
    '''Test the basic englyph image use case'''
    def compose(self) -> ComposeResult:
        #yield EnGlyphImage( "testing/twirl.gif" )
        yield EnGlyphImage( "testing/hopper.jpg" )

# uv run testing/image_test.py
if __name__ == "__main__":
    Test().run(inline=True, inline_no_clear=True)
