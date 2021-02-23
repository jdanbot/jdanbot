from PIL import Image, ImageDraw, ImageFont

import os
import random

from ..config import IMAGE_PATH


class Photo:
    def __init__(self, path=None, xy=(220, 220)):
        if path is not None:
            self.path = path
            self.saved_path = path.split(".")[0] + "_saved.jpg"
            self.image = Image.open(path)
            self.idraw = ImageDraw.Draw(self.image)
        else:
            self.path = IMAGE_PATH.format(
                image=random.randint(0, 1000000000000000)
            )
            self.saved_path = f"{self.path.split('.')[0]}_saved.jpg"
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
        self.image.save(self.saved_path)
        return open(self.saved_path, "rb")

    def clean(self):
        self._remove(self.path)
        self._remove(self.saved_path)

    def font(self, path, size):
        self.font = ImageFont.truetype(path, size=size)

    def _remove(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
