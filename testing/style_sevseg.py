"""Boilerplate code for testing purposes"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button
from textual_englyph import EnGlyphText, EnSevSeg


class Test(App):
    """Test console markup styling the englyph text use case"""
    DEFAULT_CSS="""
    #hi {
        color: darkslategray 100%;
        background: aquamarine 60%;
    }
    #pi {
        color: #75ffff;
        background: #1c80d8;
    }
    #clock {
        margin: 1;
        #hours {
            border-right: none;
        }
        #minutes {
            border-left: none;
        }
        #colon {
            color: red;
            background: #400000;
            border-top: outer black;
            border-bottom: outer black;
        }
    }
    """
    minute = 19

    def compose(self) -> ComposeResult:
        """Display seven segment digits. Can use Latin basic characters or
        8 bit direct segment control in PUA \uED00 - \uEDFF
        where 1<<0 (LSB) is segement a, 1<<2 is b, ..., 1<<7 is g and 1<<8 is DP
        """
        yield EnSevSeg("Hello Textual", id="hi")
        yield EnSevSeg("\uEDCF \uED06 4 1 5", id="pi", basis=(1,2))
        yield Button("Add Min", id="toc")
        with Horizontal(id="clock"):
            yield EnSevSeg(" 4", id="hours")
            yield EnGlyphText("[blink]:", text_size="small", id="colon")
            yield EnSevSeg(f"{self.minute:02}", id="minutes")
        yield EnGlyphText('Your terminal font')
        yield EnGlyphText('\uED06 2 3', font_name='EnSevSeg_8x5.ttf', font_size=8, basis=(2,4) )

    def on_button_pressed(self):
        self.minute +=1
        self.query_one("#minutes").update( f"{self.minute:02}" )

if __name__ == "__main__":
    Test().run()
