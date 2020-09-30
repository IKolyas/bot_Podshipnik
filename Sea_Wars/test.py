import createArena
from PIL import Image, ImageDraw, ImageFont
import sys

try:
    tatras = Image.open("board.png")
except Exception as e:
    print(e, "Unable to load image")
    sys.exit(1)

draw = ImageDraw.Draw(tatras)
ship = "X"
font = ImageFont.truetype("arial.ttf", size=52)

sbX = 55
sbY = 48

# idraw.text((55, 48), ship, font=font, fill='#1C0606')
# idraw.text((110, 98), ship, font=font, fill='#1C0606')

# tatras.save('newBoard.png')

newRand = createArena.Arena


def point(randBoard):
    for r in range(0, 10):
        for c in randBoard.col:
            if randBoard.loc[r, c] == 'k':
                draw.text((sbX * r, sbY * randBoard.col.index(c)), ship, font=font, fill='#1C0606')


point(newRand)
