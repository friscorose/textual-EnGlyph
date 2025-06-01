"""Abstract module class to package up driver routines for EnGlyph"""

# pylint: disable=R0914
# greatly simplifies structure in __init__.py
from typing import List
from importlib import resources

from PIL import Image, ImageFont

from textual.strip import Strip
from rich.color import Color, ColorTriplet, ColorType
from rich.segment import Segment
from rich.style import Style
from rich.traceback import install

install()
# raise ValueError("My message")

def EnLoad( maybe_path ):
    """
    A function to load file data into memory from a path and return that refernce.
    """
    import io

    if isinstance(maybe_path, str):
        with open(maybe_path, "rb") as fh:
            im_data = fh.read()
            im_buff = io.BytesIO(im_data)
            maybe_path = Image.open(im_buff)
    return maybe_path

class ToGlyxels:
    """Glyph pixels to enable user specified font based string rendering via PIL"""

    @staticmethod
    def font_pane(phrase, font_name, font_size):
        font_asset = resources.files().joinpath("assets", font_name)
        if not font_asset.is_file():
            raise AttributeError( font_asset )
        font = ImageFont.truetype(font_asset, size=font_size)
        _, _, r, b = font.getbbox(phrase)
        # raise AttributeError( r, b )
        mask = list(font.getmask(phrase, mode="1"))
        return (r, b, mask)

    # full infill glyxel(glyph pixel) look up table, columns x rows
    full_glut = [[], ["", "", ""], ["", "", "", "", ""]]
    full_glut[1][1] = " █"
    full_glut[1][2] = " ▀▄█"
    full_glut[2][2] = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
    full_glut[2][3] = " 🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬑🬒🬓▌🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧▐🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻█"
    full_glut[2][4] = (
        " 𜺨𜺫🮂𜴀▘𜴁𜴂𜴃𜴄▝𜴅𜴆𜴇𜴈▀𜴉𜴊𜴋𜴌🯦𜴍𜴎𜴏𜴐𜴑𜴒𜴓𜴔𜴕𜴖𜴗𜴘𜴙𜴚𜴛𜴜𜴝𜴞𜴟🯧𜴠𜴡𜴢𜴣𜴤𜴥𜴦𜴧𜴨𜴩𜴪𜴫𜴬𜴭𜴮𜴯𜴰𜴱𜴲𜴳𜴴𜴵🮅"
        "𜺣𜴶𜴷𜴸𜴹𜴺𜴻𜴼𜴽𜴾𜴿𜵀𜵁𜵂𜵃𜵄▖𜵅𜵆𜵇𜵈▌𜵉𜵊𜵋𜵌▞𜵍𜵎𜵏𜵐▛𜵑𜵒𜵓𜵔𜵕𜵖𜵗𜵘𜵙𜵚𜵛𜵜𜵝𜵞𜵟𜵠𜵡𜵢𜵣𜵤𜵥𜵦𜵧𜵨𜵩𜵪𜵫𜵬𜵭𜵮𜵯𜵰"
        "𜺠𜵱𜵲𜵳𜵴𜵵𜵶𜵷𜵸𜵹𜵺𜵻𜵼𜵽𜵾𜵿𜶀𜶁𜶂𜶃𜶄𜶅𜶆𜶇𜶈𜶉𜶊𜶋𜶌𜶍𜶎𜶏▗𜶐𜶑𜶒𜶓▚𜶔𜶕𜶖𜶗▐𜶘𜶙𜶚𜶛▜𜶜𜶝𜶞𜶟𜶠𜶡𜶢𜶣𜶤𜶥𜶦𜶧𜶨𜶩𜶪𜶫"
        "▂𜶬𜶭𜶮𜶯𜶰𜶱𜶲𜶳𜶴𜶵𜶶𜶷𜶸𜶹𜶺𜶻𜶼𜶽𜶾𜶿𜷀𜷁𜷂𜷃𜷄𜷅𜷆𜷇𜷈𜷉𜷊𜷋𜷌𜷍𜷎𜷏𜷐𜷑𜷒𜷓𜷔𜷕𜷖𜷗𜷘𜷙𜷚▄𜷛𜷜𜷝𜷞▙𜷟𜷠𜷡𜷢▟𜷣▆𜷤𜷥█"
    )
    # partial infill pixels(pips) glyxel look up table, columns x rows
    pips_glut = [[], ["", "", ""], ["", "", "", "", ""]]
    pips_glut[1][1] = " ●"
    pips_glut[1][2] = " ᛫.:"
    pips_glut[2][2] = " 𜰡𜰢𜰣𜰤𜰥𜰦𜰧𜰨𜰩𜰪𜰫𜰬𜰭𜰮𜰯"
    pips_glut[2][3] = " 𜹑𜹒𜹓𜹔𜹕𜹖𜹗𜹘𜹙𜹚𜹛𜹜𜹝𜹞𜹟𜹠𜹡𜹢𜹣𜹤𜹥𜹦𜹧𜹨𜹩𜹪𜹫𜹬𜹭𜹮𜹯𜹰𜹱𜹲𜹳𜹴𜹵𜹶𜹷𜹸𜹹𜹺𜹻𜹼𜹽𜹾𜹿𜺀𜺁𜺂𜺃𜺄𜺅𜺆𜺇𜺈𜺉𜺊𜺋𜺌𜺍𜺎𜺏"
    pips_glut[2][4] = (
        "⠀⠁⠈⠉⠂⠃⠊⠋⠐⠑⠘⠙⠒⠓⠚⠛⠄⠅⠌⠍⠆⠇⠎⠏⠔⠕⠜⠝⠖⠗⠞⠟⠠⠡⠨⠩⠢⠣⠪⠫⠰⠱⠸⠹⠲⠳⠺⠻⠤⠥⠬⠭⠦⠧⠮⠯⠴⠵⠼⠽⠶⠷⠾⠿"
        "⡀⡁⡈⡉⡂⡃⡊⡋⡐⡑⡘⡙⡒⡓⡚⡛⡄⡅⡌⡍⡆⡇⡎⡏⡔⡕⡜⡝⡖⡗⡞⡟⡠⡡⡨⡩⡢⡣⡪⡫⡰⡱⡸⡹⡲⡳⡺⡻⡤⡥⡬⡭⡦⡧⡮⡯⡴⡵⡼⡽⡶⡷⡾⡿"
        "⢀⢁⢈⢉⢂⢃⢊⢋⢐⢑⢘⢙⢒⢓⢚⢛⢄⢅⢌⢍⢆⢇⢎⢏⢔⢕⢜⢝⢖⢗⢞⢟⢠⢡⢨⢩⢢⢣⢪⢫⢰⢱⢸⢹⢲⢳⢺⢻⢤⢥⢬⢭⢦⢧⢮⢯⢴⢵⢼⢽⢶⢷⢾⢿"
        "⣀⣁⣈⣉⣂⣃⣊⣋⣐⣑⣘⣙⣒⣓⣚⣛⣄⣅⣌⣍⣆⣇⣎⣏⣔⣕⣜⣝⣖⣗⣞⣟⣠⣡⣨⣩⣢⣣⣪⣫⣰⣱⣸⣹⣲⣳⣺⣻⣤⣥⣬⣭⣦⣧⣮⣯⣴⣵⣼⣽⣶⣷⣾⣿"
    )

    @staticmethod
    def image2slate(image, basis=(2, 4), pips=False):
        """A fast method to convert a PIL image into a slate (list of strips)"""
        #raise AttributeError( bbox_size )
        #raise AttributeError( image.getbbox() )
        x_size, y_size = image.size
        #_, _, x_size, y_size = image.getbbox() 
        dx, dy = basis
        glut = ToGlyxels.pips_glut if pips else ToGlyxels.full_glut
        slate = []

        for y_pos in range(0, y_size, dy):
            y_strip = []
            for x_pos in range(0, x_size, dx):
                cell_img = image.crop((x_pos, y_pos, x_pos + dx, y_pos + dy))
                glut_idx, glyph_sty = ToGlyxels._img4cell2vals4seg(cell_img)
                glyph = glut[dx][dy][glut_idx]
                y_strip.append(Segment(glyph, glyph_sty))
            slate.append(Strip(y_strip))

        return slate

    @staticmethod
    def _img4cell2vals4seg(image):
        """Compute glyph look up table offset and associated style coloring"""
        fg = []
        bg = []
        glut_idx = 0

        duotone = image.quantize(colors=2)
        for idx, test_gx in enumerate(list(duotone.getdata())):
            if test_gx:
                fg.append(image.getdata()[idx])
                glut_idx += 2**idx
            else:
                bg.append(image.getdata()[idx])

        fg_color = ToGlyxels._colors2rgb4sty(fg)
        bg_color = ToGlyxels._colors2rgb4sty(bg)
        glyph_sty = Style( color=fg_color, bgcolor=bg_color)

        return (glut_idx, glyph_sty)

    @staticmethod
    def _colors2rgb4sty(RGB_list):
        """Compute broken but fast RGB centroid"""
        rgb_list = RGB_list
        n = len(rgb_list)
        if n == 0:
            return Color( name="rgb_cell", type=ColorType.TRUECOLOR, triplet=ColorTriplet(0, 0, 0) )
        else:
            R, G, B = [sum(x) for x in zip(*rgb_list)]
            return Color( name="rgb_cell", type=ColorType.TRUECOLOR, triplet=ColorTriplet(R//n, G//n, B//n) )

    @staticmethod
    def pane2slate(pane, style: Style | None, basis, pips) -> List[List[Segment]]:
        """accept a PIL mask with dimensions (pane) and return a list of Textual strips"""
        x, y, mask = pane
        if x == 0 or y == 0:
            return [Strip.blank(0)]

        glut = ToGlyxels.pips_glut if pips else ToGlyxels.full_glut

        selection = Image.new("1", (x, y))
        selection.putdata(mask)
        # glyph based pixels must be an integer multiple of glyph cell basis, ie. 2x4 -> octants
        while x % basis[0] != 0:
            x += 1
        while y % basis[1] != 0:
            y += 1
        pane = Image.new("1", (x, y))
        # place bitmap into upper left corner
        pane.paste(selection, (0, 0))

        base_row = int(y / basis[1] - 1)
        mid_row = int(base_row / 2)
        cap_row = 0

        slate = []
        for y_glyph in range(0, y, basis[1]):
            y_strip = []
            y_row = int(y_glyph / basis[1])
            y_style = ToGlyxels._y_style(style, cap_row, mid_row, base_row, y_row)
            for x_glyph in range(0, x, basis[0]):
                glyph_idx = 0
                glyxel_list = []
                for y_idx in range(basis[1]):
                    for x_idx in range(basis[0]):
                        glyxel_list.append(
                            pane.getpixel((x_glyph + x_idx, y_glyph + y_idx))
                        )
                for exp, g_color in enumerate(glyxel_list):
                    if g_color > 0:
                        glyph_idx += 2**exp
                glyph = glut[basis[0]][basis[1]][glyph_idx]
                y_strip.append(Segment(glyph, y_style))
            slate.append(Strip(y_strip))
        return slate

    @staticmethod
    def style_slate(slate, style):
        """re-style content of strips"""
        base_row = len(slate)
        mid_row = int(base_row / 2)
        cap_row = 0
        new_slate = []
        for y_row, y_strip in enumerate(slate):
            y_style = ToGlyxels._y_style(style, cap_row, mid_row, base_row, y_row)
            new_slate.append(y_strip.apply_style(y_style))
        return new_slate

    @staticmethod
    def _y_style(style, cap_row, mid_row, base_row, y_row):
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
    def slate_join(strips, slate):
        if len(strips) == 0:
            return slate
        joint = []
        for idx, line in enumerate(strips):
            joint.append(Strip.join((line, slate[idx])).simplify())
        return joint
