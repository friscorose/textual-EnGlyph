from textual_englyph import EnGlyph
from textual.app import App, ComposeResult

class Test(App):

    phrase_list = ["Hello Textual.", "It's the world!"]
    basis_list = [(2,4),(2,3),(2,2),(1,2),(1,1)]
    use_pips = False

    test_widget = EnGlyph("From EnGlyph:")

    def compose(self) -> ComposeResult:
        yield self.test_widget

    def on_mount(self):
        self.set_interval( 2.2, self.next_render )

    def next_render(self):
        this_basis = self.basis_list.pop(0)
        self.basis_list.append( this_basis )

        self.test_widget.update( phrase=self.phrase_list[0], basis=this_basis, pips=self.use_pips )
        self.set_timer(1, self.rerender)

    def rerender(self):
        self.test_widget.update( phrase=self.phrase_list[1], basis=self.basis_list[-1], pips=self.use_pips )
        if self.basis_list[-1] == (1,1):
            self.use_pips = not self.use_pips
            if not self.use_pips: 
                self.test_widget.update( phrase="GoodBye!", basis=self.basis_list[-1], pips=self.use_pips )
                self.set_timer(1, self.app.exit)


if __name__ == "__main__":
    Test().run()

