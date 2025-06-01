from textual_englyph import EnGlyphText
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical


class Test(App):

    def compose(self) -> ComposeResult:
        with Vertical():
            self.enhello = EnGlyphText("Hello Textual!", text_size="x-small", id="enhello")
            yield Label("Default is x-small", id="enlabel")
            yield EnGlyphText("looks like")
            yield self.enhello
            with Horizontal():
                yield Button("smaller", variant="primary", id="itsy" )
                yield Button("larger", variant="primary", id="bigy" )

    @on( Button.Pressed )
    def button_press( self, event ):
        H = self.query_one("#enhello")
        if event.button.id == "bigy" and H._text_size != "xxx-large":
            H.update(text_size="larger")
        if event.button.id == "itsy":
            H.update(text_size="smaller")
        self.query_one("#enlabel").update(H._text_size)


if __name__ == "__main__":
    Test().run()
