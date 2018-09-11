import inkyphat
from PIL import ImageFont
import national_rail_fetcher

inkyphat.set_colour("yellow")

font = ImageFont.truetype("./8bitoperator.ttf", 12)

lines = national_rail_fetcher.get_board_lines()

y = 0
for line in lines:
    inkyphat.text((5, y), line, inkyphat.BLACK, font)
    y += 20
    
inkyphat.show()
