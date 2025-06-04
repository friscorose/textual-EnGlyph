from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer
from textual_englyph import EnGlyphText, EnGlyphSprite


class Test(App):
    """Test the basic englyph image use case"""

    CSS = """
    Horizontal {
        align: right bottom;
        dock: bottom;
        width: 1fr;
        height: auto;
        position: absolute;
    }
    EnGlyphSprite {
        height: 10;
        position: relative;
        offset: 0 1;
    }
    .bubble {
        background: blue;
        position: absolute;
        offset: 50vw 0;
        background: white 20%;
        padding-left: 2;
        padding-right: 2;
    }
    """

    #BongoCat = EnGlyphSprite("cats/cat_idle.png", id="I")
    cats = ["cats/cat_idle.png","cats/cat_right_paw.png","cats/cat_left_paw.png"]
    BongoCat = EnGlyphSprite(cats, id="I")

    kcats = ["cats/cat_idle_keyboard.png","cats/cat_right_paw_keyboard.png","cats/cat_left_paw_keyboard.png"]
    BongoCatKeys = EnGlyphSprite(kcats, id="I")

    def compose(self) -> ComposeResult:
        with Horizontal(id="II"):
            yield self.BongoCatKeys
        yield Footer()

    def on_key(self, event):
        self.query_one("#I").pipeline_advance()
        try:
            self.bubble.remove()
        except:
            pass
        self.bubble = EnGlyphText(event.key, classes="bubble", text_size="large") 
        self.app.mount( self.bubble )

# uv run testing/image_test.py
if __name__ == "__main__":
    # with pyinstrument.profile():
    Test().run()
    #Test().run(inline=True, inline_no_clear=True)
        #self.query_one("#I").show_frame( 1 )
        #self.notify(event.key)
