
from PIL import Image
from PIL import ImageQt
from PIL import ImageColor
from PIL import ImageFont
from PIL import ImageDraw
from typing import Union
from io import BytesIO



class TableImage:

    def __init__(
    self,
    values: list,
    size: tuple,
    ttf: str,
    i_size: int,
    n_size: int,
    fill: Union[tuple, int] = 0,
    alert_fill: Union[int, tuple] = 220) -> None:

        self.values: tuple = values
        # self.image: Image = Image.new(mode='RGB', size=size, color='#ffffff')
        self.image: Image = Image.new(mode='RGBA', size=size, color='#ffffff')
        self.draw = ImageDraw.Draw(im=self.image)
        self.font = ImageFont.truetype(font=ttf, size=n_size)
        self.index_font = ImageFont.truetype(font=ttf, size=i_size)
        self.fill = fill
        self.alert_fill = alert_fill
        self.size = self.image.size
        self.i_size = i_size
        self.n_size = n_size

    def draw_lines(self, width) -> None:
        self.draw_middle_lines(width)

    def draw_middle_lines(self, width) -> None:
        self.draw.line((0, self.size[1] // 3) + (self.size[0], self.size[1] // 3), fill=self.fill, width=width)
        self.draw.line((0, self.size[1] * 2 // 3) + (self.size[0], self.size[1] * 2 // 3), fill=self.fill, width=width)
        self.draw.line((self.size[0] // 3, 0) + (self.size[0] // 3, self.size[1]), fill=self.fill, width=width)
        self.draw.line((self.size[0] * 2 // 3, 0) + (self.size[0] * 2 // 3, self.size[1]), fill=self.fill, width=width)

    def draw_indexes(self) -> None:
        index = 1
        for i in range(3):
            for j in range(3):
                self.draw.text((90 * j + 4, 90 * i), text=str(index), fill=self.fill, font=self.index_font)
                index += 1

    def draw_values(self) -> None:
        index = 0
        values = self.values
        for i in range(3):
            for j in range(3):
                size = ImageFont.ImageFont.getsize(self, text=str(values[index]))
                if type(values[index]) == int:
                    self.draw.text((90 * j - size[0] + 55, 90 * i - size[1] + 60), text=str(values[index]), fill=self.fill, font=self.font)
                else:
                    self.draw.text((90 * j - size[0] + 75, 90 * i - size[1] + 60), text=values[index], fill=self.alert_fill, font=self.font)                   
                index += 1


    def prepare_image(self, line_w):
        self.draw_lines(width=line_w)
        self.draw_indexes()
        self.draw_values()

    def show_image(self) -> None:
        self.image.show()

    def return_image(self):
        return ImageQt.ImageQt(self.image)




if __name__ == "__main__":
    image = TableImage(values=(7, 2, 'Нет', 'Нет', 5, 6, 7, 'Нет', 'Нет'), size=(270, 270), ttf='./resources/arial.ttf', i_size=18, n_size=35)
    image.prepare_image(line_w=2)
    image.show_image()