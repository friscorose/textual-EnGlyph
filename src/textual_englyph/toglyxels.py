""" Abstract module class to package up driver routines for EnGlyph"""
# pylint: disable=R0914
# greatly simplifies structure in __init__.py
from typing import List
from importlib import resources

from PIL import Image, ImageFont

from textual.strip import Strip
from rich.segment import Segment
from rich.style import Style
from rich.traceback import install
install()
#raise ValueError("My message")


class ToGlyxels():
    """Glyph pixels to enable user specified font based string rendering via PIL"""

    #full infill glyxel(glyph pixel) look up table, columns x rows
    full_glut = [[],["","",""],["","","","",""]]
    full_glut[1][1] = " █"
    full_glut[1][2] = " ▀▄█"
    full_glut[2][2] = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
    full_glut[2][3] = " 🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬑🬒🬓▌🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧▐🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻█"
    full_glut[2][4] = ( " 𜺨𜺫🮂𜴀▘𜴁𜴂𜴃𜴄▝𜴅𜴆𜴇𜴈▀𜴉𜴊𜴋𜴌🯦𜴍𜴎𜴏𜴐𜴑𜴒𜴓𜴔𜴕𜴖𜴗𜴘𜴙𜴚𜴛𜴜𜴝𜴞𜴟🯧𜴠𜴡𜴢𜴣𜴤𜴥𜴦𜴧𜴨𜴩𜴪𜴫𜴬𜴭𜴮𜴯𜴰𜴱𜴲𜴳𜴴𜴵🮅"
                        "𜺣𜴶𜴷𜴸𜴹𜴺𜴻𜴼𜴽𜴾𜴿𜵀𜵁𜵂𜵃𜵄▖𜵅𜵆𜵇𜵈▌𜵉𜵊𜵋𜵌▞𜵍𜵎𜵏𜵐▛𜵑𜵒𜵓𜵔𜵕𜵖𜵗𜵘𜵙𜵚𜵛𜵜𜵝𜵞𜵟𜵠𜵡𜵢𜵣𜵤𜵥𜵦𜵧𜵨𜵩𜵪𜵫𜵬𜵭𜵮𜵯𜵰"
                        "𜺠𜵱𜵲𜵳𜵴𜵵𜵶𜵷𜵸𜵹𜵺𜵻𜵼𜵽𜵾𜵿𜶀𜶁𜶂𜶃𜶄𜶅𜶆𜶇𜶈𜶉𜶊𜶋𜶌𜶍𜶎𜶏▗𜶐𜶑𜶒𜶓▚𜶔𜶕𜶖𜶗▐𜶘𜶙𜶚𜶛▜𜶜𜶝𜶞𜶟𜶠𜶡𜶢𜶣𜶤𜶥𜶦𜶧𜶨𜶩𜶪𜶫"
                        "▂𜶬𜶭𜶮𜶯𜶰𜶱𜶲𜶳𜶴𜶵𜶶𜶷𜶸𜶹𜶺𜶻𜶼𜶽𜶾𜶿𜷀𜷁𜷂𜷃𜷄𜷅𜷆𜷇𜷈𜷉𜷊𜷋𜷌𜷍𜷎𜷏𜷐𜷑𜷒𜷓𜷔𜷕𜷖𜷗𜷘𜷙𜷚▄𜷛𜷜𜷝𜷞▙𜷟𜷠𜷡𜷢▟𜷣▆𜷤𜷥█")
    #partial infill pixels(pips) glyxel look up table, columns x rows
    pips_glut =  [[],["","",""],["","","","",""]]
    pips_glut[1][1] = " ●"
    pips_glut[1][2] = " ᛫.:"
    pips_glut[2][2] = " 𜰡𜰢𜰣𜰤𜰥𜰦𜰧𜰨𜰩𜰪𜰫𜰬𜰭𜰮𜰯"
    pips_glut[2][3] = " 𜹑𜹒𜹓𜹔𜹕𜹖𜹗𜹘𜹙𜹚𜹛𜹜𜹝𜹞𜹟𜹠𜹡𜹢𜹣𜹤𜹥𜹦𜹧𜹨𜹩𜹪𜹫𜹬𜹭𜹮𜹯𜹰𜹱𜹲𜹳𜹴𜹵𜹶𜹷𜹸𜹹𜹺𜹻𜹼𜹽𜹾𜹿𜺀𜺁𜺂𜺃𜺄𜺅𜺆𜺇𜺈𜺉𜺊𜺋𜺌𜺍𜺎𜺏"
    pips_glut[2][4] = ( "⠀⠁⠈⠉⠂⠃⠊⠋⠐⠑⠘⠙⠒⠓⠚⠛⠄⠅⠌⠍⠆⠇⠎⠏⠔⠕⠜⠝⠖⠗⠞⠟⠠⠡⠨⠩⠢⠣⠪⠫⠰⠱⠸⠹⠲⠳⠺⠻⠤⠥⠬⠭⠦⠧⠮⠯⠴⠵⠼⠽⠶⠷⠾⠿"
                        "⡀⡁⡈⡉⡂⡃⡊⡋⡐⡑⡘⡙⡒⡓⡚⡛⡄⡅⡌⡍⡆⡇⡎⡏⡔⡕⡜⡝⡖⡗⡞⡟⡠⡡⡨⡩⡢⡣⡪⡫⡰⡱⡸⡹⡲⡳⡺⡻⡤⡥⡬⡭⡦⡧⡮⡯⡴⡵⡼⡽⡶⡷⡾⡿"
                        "⢀⢁⢈⢉⢂⢃⢊⢋⢐⢑⢘⢙⢒⢓⢚⢛⢄⢅⢌⢍⢆⢇⢎⢏⢔⢕⢜⢝⢖⢗⢞⢟⢠⢡⢨⢩⢢⢣⢪⢫⢰⢱⢸⢹⢲⢳⢺⢻⢤⢥⢬⢭⢦⢧⢮⢯⢴⢵⢼⢽⢶⢷⢾⢿"
                        "⣀⣁⣈⣉⣂⣃⣊⣋⣐⣑⣘⣙⣒⣓⣚⣛⣄⣅⣌⣍⣆⣇⣎⣏⣔⣕⣜⣝⣖⣗⣞⣟⣠⣡⣨⣩⣢⣣⣪⣫⣰⣱⣸⣹⣲⣳⣺⣻⣤⣥⣬⣭⣦⣧⣮⣯⣴⣵⣼⣽⣶⣷⣾⣿")


    @staticmethod
    def frame2slate( image,
                    mode_color=None,
                    mode_depth=None,
                    basis=(2,4),
                    pips=False
                    ):
        _,_,x,y = image.getbbox()

        glut = ToGlyxels.pips_glut if pips else ToGlyxels.full_glut

        slate = []
        for y_pixpos in range( 0, y, basis[1] ):
            y_strip = []
            for x_pixpos in range( 0, x, basis[0] ):
                cell_img = image.crop( (x_pixpos, y_pixpos, x_pixpos+basis[0], y_pixpos+basis[1]) )
                glyph_idx, glyph_sty = ToGlyxels._img4cell2vals4seg( cell_img )
                glyph = glut[basis[0]][basis[1]][glyph_idx]
                y_strip.append( Segment( glyph, glyph_sty ) )
            slate.append( Strip(y_strip) )
        return slate

    @staticmethod
    def _img4cell2vals4seg( image ):
        fg = []
        bg = []
        glut_idx = 0
        duotone = image.quantize( colors=2 )
        for idx, test_gx in enumerate( list(duotone.getdata()) ):
            if test_gx:
                fg.append( image.getdata()[idx] )
                glut_idx += 2**idx
            else:
                bg.append( image.getdata()[idx] )

        fg_color = ToGlyxels._colors2rgb4sty( fg )
        bg_color = ToGlyxels._colors2rgb4sty( bg )
        glyph_sty = Style.parse(" on ".join( [fg_color, bg_color] )) 
        #raise Exception( (glyph_idx, glyph_sty) )
        return (glut_idx, glyph_sty)

    @staticmethod
    def _colors2rgb4sty( rgb_list ):
        """Compute broken but fast RGB centroid"""
        n = len( rgb_list )
        s = [sum(x*x) for x in zip(*rgb_list)]
        ms = [x/n for x in v_sum]
        rms = [math.sqrt(x) for x in ms]
        R,G,B = [ int(x) for x in rms]
        return f"rgb({R},{G},{B})"

    @staticmethod
    def _idx4pal2rgb4sty( palette, index ):
        R,G,B = palette[index:index+3]
        return f"rgb({R},{G},{B})"


    @staticmethod
    def _get_fg_info( glyxel_color, mode ):
        #https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.convert
        #Assume grayscale
        glyxel_luminance = glyxel_color
        glyxel_rgb = f"rgb({glyxel_color},{glyxel_color},{glyxel_color})"
        if mode == "RGB":
            R,G,B = glyxel_color
            glyxel_luminance = R*0.299 + G*0.587 + B*0.114
            glyxel_rgb = f"rgb({R},{G},{B})"
        elif mode == "RGBA":
            R,G,B,A = glyxel_color
            glyxel_luminance = (R*0.299 + G*0.587 + B*0.114)*A/255
            R = R*A/255
            G = G*A/255
            B = B*A/255
            glyxel_rgb = f"rgb({R},{G},{B})"
        return (glyxel_luminance, glyxel_rgb)

    @staticmethod
    def _get_glyph_info( x: int, y: int, celllist: list ):
        offset = 0
        fg_color = "default"
        bg_color = "default"
        brightlist = []
        darklist = []
        colors = []
        
        """ Process current cell pixels for brightness (intensity) bilevel 'coloring'. """
        for exp, pixel in enumerate( celllist ):
            if self._get_intensity( pixel ) > self.weight:
                brightlist.append( pixel )
                offset += 2**exp
            else:
                darklist.append( pixel )

        if darklist:
            """ Simple RGB component averaging of background pixels, is this good?"""
            bg_color = self._get_color( tuple( [int(sum(y) / len(y)) for y in zip(*darklist)] ) )
            if brightlist:
                fg_color = self._get_color( tuple( [int(sum(y) / len(y)) for y in zip(*brightlist)] ) )
        elif not self.mono:
            """ All bright condition, reprocess cell for dominant 2 color pattern.
                A possibly better approach here would be use adjacent cells in a
                Floyd-Steinberg esque 2-color dithering downsampling."""
            offset = 0
            cellimg = Image.new( 'RGBA', (self.x_pixels, self.y_pixels) )
            cellimg.putdata( celllist )
            cellbiimg = cellimg.convert( 'P', dither=None, colors=2 )
            palette = cellbiimg.getpalette()
            cellbilist = list( cellbiimg.getdata() )
            for exp, pixel in enumerate( cellbilist ):
                if pixel:
                    offset += 2**exp
            bg_color = self._get_color( (palette[0], palette[1], palette[2], 255) )
            fg_color = self._get_color( (palette[3], palette[4], palette[5], 255) )

        if fg_color is not None:
            colors.append( fg_color )
        else:
            colors.append( "default" )
        if bg_color is not None:
            colors.append( bg_color )
        else:
            colors.append( "default" )
        style = Style.parse(" on ".join(colors)) 
        return( offset, style )

    @staticmethod
    def pane2slate(
            pane,
            style: Style|None,
            basis,
            pips ) -> List[List[Segment]]:
        ''' accept a PIL mask with dimensions (pane) and return a list of Textual strips '''
        x,y,mask = pane
        if x == 0 or y == 0:
            return [ Strip.blank(0) ]

        glut = ToGlyxels.pips_glut if pips else ToGlyxels.full_glut

        selection = Image.new( '1', (x,y) )
        selection.putdata(mask)
        #glyph based pixels must be an integer multiple of glyph cell basis, ie. 2x4 -> octants
        while x % basis[0] != 0:
            x += 1
        while y % basis[1] != 0:
            y += 1
        pane = Image.new( '1', (x,y) )
        #place bitmap into upper left corner
        pane.paste( selection, (0,0) )

        base_row = int( y/basis[1] - 1 )
        mid_row = int( base_row/2 )
        cap_row = 0

        slate = []
        for y_glyph in range( 0, y, basis[1] ):
            y_strip = []
            y_row = int( y_glyph/basis[1] )
            y_style = ToGlyxels._y_style( style, cap_row, mid_row, base_row, y_row)
            for x_glyph in range( 0, x, basis[0] ):
                glyph_idx = 0
                glyxel_list = []
                for y_idx in range( basis[1] ):
                    for x_idx in range( basis[0] ):
                        glyxel_list.append( pane.getpixel( (x_glyph+x_idx, y_glyph+y_idx) ) )
                for exp, g_color in enumerate( glyxel_list ):
                    if g_color > 0:
                        glyph_idx += 2**exp
                glyph = glut[basis[0]][basis[1]][glyph_idx]
                y_strip.append( Segment( glyph, y_style ) )
            slate.append( Strip(y_strip) )
        return slate

    @staticmethod
    def style_slate( slate, style):
        ''' re-style content of strips '''
        base_row = len( slate )
        mid_row = int( base_row/2 )
        cap_row = 0
        new_slate = []
        for y_row, y_strip in enumerate( slate ):
            y_style = ToGlyxels._y_style( style, cap_row, mid_row, base_row, y_row)
            new_slate.append( y_strip.apply_style( y_style ) )
        return new_slate

    @staticmethod
    def _y_style( style, cap_row, mid_row, base_row, y_row):
        if style:
            if style.overline and y_row != cap_row:
                style = style + Style(overline=False)
            if style.strike and y_row != mid_row:
                style = style + Style(strike=False)
            if y_row != base_row:
                if style.underline:
                    style = style + Style(underline=False)
                if style.underline2:
                    style = style + Style(underline2=False)
        return style

    @staticmethod
    def slate_join( strips, slate ):
        if len( strips ) == 0:
            return slate
        joint = []
        for idx, line in enumerate( strips ):
            joint.append(Strip.join( (line,slate[idx]) ).simplify())
        return joint

    @staticmethod
    def font_pane( phrase, font_name, font_size ):
        font_asset = resources.files().joinpath( "assets", font_name )
        font = ImageFont.truetype( font_asset, size=font_size )
        _,_,r,b = font.getbbox( phrase )
        mask = list( font.getmask(phrase, mode='1') )
        return (r,b,mask)
