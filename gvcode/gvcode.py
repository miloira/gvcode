import base64
import random
import string
from io import BytesIO
from pathlib import Path
from random import randint, choice
from PIL import ImageFont, ImageFilter, Image, ImageColor, ImageDraw
from typing import List, Tuple, Any, Union, Optional


class VFCode:

    def __init__(
            self,
            width: int = 200,
            height: int = 80,
            fontsize: int = 50,
            font_color_values: Optional[List[str]] = None,
            font_background_value: Optional[str] = None,
            draw_dots: bool = False,
            dots_width: int = 1,
            draw_lines: bool = True,
            lines_width: int = 3,
            mask: bool = False,
            font: Optional[str] = None
    ):
        """
        初始化参数
        :param width: 图片宽度
        :param height: 图片高度
        :param fontsize: 字体尺寸
        :param font_color_values: 字体颜色值
        :param font_background_value: 背景颜色值
        :param draw_dots: 是否画干扰点
        :param dots_width: 干扰点宽度
        :param draw_lines: 是否画干扰线
        :param lines_width: 干扰线宽度
        :param mask: 是否使用磨砂效果
        :param font: 字体 内置可选字体 arial.ttf calibri.ttf simsun.ttc
        """
        self.code = None
        self._img = None
        self.width = width
        self.height = height
        self.fontsize = fontsize
        # linux添加字体文件 /usr/share/fonts/arial.ttf
        if font is None:
            self.font = ImageFont.truetype(str(Path(__file__).resolve().parent / 'fonts/arial.ttf'), fontsize)
        else:
            try:
                self.font = ImageFont.truetype(str(Path(__file__).resolve().parent / 'fonts/%s' % font), fontsize)
            except:
                self.font = ImageFont.truetype(font, fontsize)
        self.draw_dots = draw_dots
        self.dots_width = dots_width
        self.draw_lines = draw_lines
        self.lines_width = lines_width
        self.mask = mask

        self.symbol = None
        self.result = None

        if font_color_values:
            self.font_colors = [ImageColor.getcolor(value, 'RGBA') for value in font_color_values]
        else:
            color_values = [
                '#ffffff',
                '#000000',
                '#3e3e3e',
                '#ff1107',
                '#1bff46',
                '#ffbf13',
                '#235aff'
            ]
            self.font_colors = [ImageColor.getcolor(value, 'RGBA') for value in color_values]

        if font_background_value:
            self.font_background = ImageColor.getcolor(font_background_value, 'RGBA')
        else:
            self.font_background = ImageColor.getcolor('#ffffff', 'RGBA')

        # 移除字体颜色和背景颜色相同的值
        if self.font_background in self.font_colors:
            self.font_colors.remove(self.font_background)

    def random_color(self) -> Tuple:
        return choice(self.font_colors)

    def img_blur(self, img: Image) -> None:
        width, height = img.size
        draw = ImageDraw.Draw(img)

        if self.draw_lines:
            for i in range(5):
                x1 = randint(0, width)
                x2 = randint(0, width)
                y1 = randint(0, height)
                y2 = randint(0, height)
                draw.line((x1, y1, x2, y2), fill=self.random_color(), width=self.lines_width)

        if self.draw_dots:
            for i in range(30):
                draw.point([randint(0, width), randint(0, height)], fill=self.random_color())
                x = randint(0, width)
                y = randint(0, height)
                draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.random_color(), width=self.dots_width)

    def _gen_txt_img(self, text: str) -> Image.Image:
        img = Image.new('RGBA', (self.fontsize + 5, self.fontsize + 5))
        text_draw = ImageDraw.Draw(img)
        text_draw.text((0, 0), text, fill=self.random_color(), font=self.font)

        if self.symbol and self.result:
            if text == self.symbol:
                return img
            img = img.rotate(angle=randint(-30, 30), expand=False)
        else:
            img = img.rotate(angle=randint(-30, 90), expand=False)
        return img

    def generate(self, code) -> None:
        self.code = code
        self._img = Image.new(
            'RGBA',
            (self.width, self.height),
            color=self.font_background
        )
        # blur image
        self.img_blur(self._img)
        if self.symbol and self.result:
            deal_code = code.split(self.symbol)
            deal_code.insert(1, self.symbol)
        else:
            deal_code = code
        base = int(self.width / len(deal_code))
        for pos, c in enumerate(deal_code):
            txt_img = self._gen_txt_img(c)
            roffset = randint(-10, 10)

            # set the position and paste the code image
            x, y = pos * base + roffset, int((self.height - txt_img.height) / 2)

            if x < 0:
                x = 0
            if x > self.width:
                x = self.width
            self._img.paste(txt_img, box=(x, y), mask=txt_img)

        if self.mask:
            # ImageFilter.GaussianBlur
            self._img = self._img.filter(ImageFilter.GaussianBlur(radius=1))

    def generate_digit(self, length: int = 5) -> None:
        self.generate(''.join(str(random.randrange(10 ** (length - 1), 10 ** length))))

    def generate_alpha(self, length: int = 5) -> None:
        code_list = []
        for i in range(length):
            code_list.append(choice(string.ascii_letters))

        self.generate(''.join(code_list))

    def generate_mix(self, length: int = 5) -> None:
        code_list = []
        for i in range(length):
            code_list.append(choice(string.digits + string.ascii_letters))

        self.generate(''.join(code_list))

    def generate_op(self, symbol: str = 'x') -> None:
        self.symbol = symbol
        left_digit = random.randrange(10, 100)
        right_digit = random.randrange(10, 100)
        while left_digit <= right_digit:
            right_digit //= 2
        if symbol == '+':
            self.result = left_digit + right_digit
        elif symbol == '-':
            self.result = left_digit - right_digit
        elif symbol == 'x':
            left_digit = random.randrange(1, 10)
            right_digit = random.randrange(1, 10)
            self.result = left_digit * right_digit
        else:
            raise ValueError('仅支持 +-x')
        self.generate('%s%s%s' % (left_digit, symbol, right_digit))

    def get_img_bytes(self, fm='png') -> bytes:
        binary_stream = BytesIO()
        self._img.save(binary_stream, fm)
        return binary_stream.getvalue()

    def get_img_base64(self, fm='png') -> Tuple[Any, Union[str, Any]]:
        b64_img_prefix = 'data:image/png;base64,'
        base64_img = b64_img_prefix + base64.b64encode(self.get_img_bytes(fm)).decode()
        if self.symbol and self.result:
            return str(self.result), base64_img
        else:
            return self.code, base64_img

    def save(self, filename: str = None, fm='png') -> None:
        if filename is None:
            self._img.save(self.code + '.' + fm, fm)
        else:
            self._img.save(filename, fm)


if __name__ == '__main__':
    vc = VFCode(
        width=200,                       # 图片宽度
        height=80,                       # 图片高度
        fontsize=50,                     # 字体尺寸
        font_color_values=[
            '#ffffff',
            '#000000',
            '#3e3e3e',
            '#ff1107',
            '#1bff46',
            '#ffbf13',
            '#235aff'
        ],                                # 字体颜色值
        font_background_value='#ffffff',  # 背景颜色值
        draw_dots=False,                  # 是否画干扰点
        dots_width=1,                     # 干扰点宽度
        draw_lines=True,                  # 是否画干扰线
        lines_width=3,                    # 干扰线宽度
        mask=False,                       # 是否使用磨砂效果
        font='arial.ttf'                  # 字体 内置可选字体 arial.ttf calibri.ttf simsun.ttc
    )
    # 验证码类型
    # 自定义验证码
    # vc.generate('abcd')

    # 数字验证码（默认5位）
    # vc.generate_digit()
    # vc.generate_digit(4)

    # 字母验证码（默认5位）
    # vc.generate_alpha()
    # vc.generate_alpha(5)

    # 数字字母混合验证码（默认5位）
    # vc.generate_mix()
    # vc.generate_mix(6)

    # 数字加减验证码（默认加法）
    vc.generate_op()
    # 数字加减验证码（加法）
    # vc.generate_op('+')
    # 数字加减验证码（减法）
    # vc.generate_op('-')

    # 图片字节码
    # print(vc.get_img_bytes())
    # 图片base64编码
    print(vc.get_img_base64())
    # 保存图片
    vc.save()