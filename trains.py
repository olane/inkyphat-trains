import inkyphat
from PIL import ImageFont

inkyphat.set_colour("yellow")

font = ImageFont.truetype("./8bitoperator.ttf", 18)

inkyphat.text((5, 0), "16:44 - Kings Lynn - 16m", inkyphat.BLACK, font)
inkyphat.text((5, 20), "16:48 - Ely - 13m", inkyphat.BLACK, font)
inkyphat.text((5, 40), "17:11 - Norwich - 15m (EXPECTED 17:13)", inkyphat.BLACK, font)
inkyphat.text((5, 60), "17:44 - Kings Lynn - 16m", inkyphat.BLACK, font)
inkyphat.text((5, 80), "17:48 - Ely - 13m", inkyphat.BLACK, font)


inkyphat.show()
