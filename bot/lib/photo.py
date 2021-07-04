from PIL import Image, ImageDraw, ImageFont

import io
import random

from ..config import IMAGE_PATH


class Photo:
    def __init__(self, path=None, xy=(220, 220)):
        self.image = Image.new("RGB", xy, (255, 255, 255))
        self.idraw = ImageDraw.Draw(self.image)

    def resize(self, size):
        self.image.thumbnail((size[0], size[1]))

    def rectangle(self, size1, size2, color):
        self.idraw.rectangle((size1, size2), fill=color)

    def text(self, color, xy, text, p=3, shadowcolor="white", outline=True):
        x, y = xy[0], xy[1]

        if outline:
            self.idraw.text((x-p, y), text, font=self.font, fill=shadowcolor)
            self.idraw.text((x+p, y), text, font=self.font, fill=shadowcolor)
            self.idraw.text((x, y-p), text, font=self.font, fill=shadowcolor)
            self.idraw.text((x, y+p), text, font=self.font, fill=shadowcolor)

            # thicker border
            self.idraw.text((x-p, y-p), text, font=self.font, fill=shadowcolor)
            self.idraw.text((x+p, y-p), text, font=self.font, fill=shadowcolor)
            self.idraw.text((x-p, y+p), text, font=self.font, fill=shadowcolor)
            self.idraw.text((x+p, y+p), text, font=self.font, fill=shadowcolor)

        self.idraw.text((x, y), text, font=self.font, fill=color)

    def parseXY(self, xy):
        xy = xy.split("x")

        if int(xy[0]) > 99999:
            raise ValueError

        if int(xy[1]) > 99999:
            raise ValueError

        return (int(xy[0]), int(xy[1]))

    def save(self):
        file = io.BytesIO()
        self.image.save(file, "PNG")
        file.seek(0)

        return file

    def font(self, path, size):
        self.font = ImageFont.truetype(path, size=size)