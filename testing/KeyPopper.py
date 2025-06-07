from textual.app import App, ComposeResult
from textual.widgets import Footer
from textual_englyph import EnGlyphText, EnGlyphSprite


class Test(App):
    """Test the basic animated sprite prototype"""

    CSS = """
    EnGlyphSprite {
        height: 10;
        position: relative;
        offset: 70vw 70vh;
        opacity: 60%;
    }
    .bubble {
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

    kcats = ["cats/cat_idle_keyboard.png","cats/cat_right_paw_keyboard.png",
             "cats/cat_idle_keyboard.png","cats/cat_left_paw_keyboard.png"]
    BongoCatKeys = EnGlyphSprite(kcats, id="I", basis=(2,3))

    def compose(self) -> ComposeResult:
        yield self.BongoCatKeys
        yield Footer()

    def on_key(self, event):
        try:
            self.bubble.remove()
        except:
            pass
        self.bubble = EnGlyphText(event.key, classes="bubble", text_size="large", basis=(2,3) ) 
        self.query_one("#I").next_frame()
        self.app.mount( self.bubble )
        self.set_timer( 2.33, self.bubble.remove )
        self.set_timer( 0.33, self.query_one("#I").next_frame )

if __name__ == "__main__":
    Test().run()
