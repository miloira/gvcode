import base64
import random
import string
from io import BytesIO
from random import randint, choice
from PIL import ImageFont, ImageFilter, Image, ImageColor, ImageDraw



class VerificationCode:

    def __init__(
            self,
            width=200,
            height=80,
            fontsize=45,
            font_color_values=None,
            font_background_value=None,
            draw_dots=False,
            dots_width=1,
            draw_lines=True,
            lines_width=3,
            mask=False,
            font_type='arial.ttf'
    ):
        """
        初始化参数
        :param width: 图片宽度
        :param height: 图片高度
        :param fontsize: 图片尺寸
        :param font_color_values: 字体颜色值
        :param font_background_value: 背景颜色值
        :param draw_dots: 是否画干扰点
        :param dots_width: 干扰点宽度
        :param draw_lines: 是否画干扰线
        :param lines_width: 干扰线宽度
        :param mask: 是否使用磨砂效果
        :param font_type: 字体 (linux系统添加字体文件 /usr/share/fonts/arial.ttf)
        """
        self.code = None
        self._img = None
        self.width = width
        self.height = height
        self.fontsize = fontsize
        self.font = ImageFont.truetype(font_type, fontsize)
        self.draw_dots = draw_dots
        self.dots_width = dots_width
        self.draw_lines = draw_lines
        self.lines_width = lines_width
        self.mask = mask

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

    def random_color(self):
        return choice(self.font_colors)

    def img_blur(self, img: Image):
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

    def _gen_txt_img(self, text: str, fontsize: int, font):
        img = Image.new('RGBA', (fontsize, fontsize))
        text_draw = ImageDraw.Draw(img)
        text_draw.text((0, 0), text, fill=self.random_color(), font=font)
        img = img.rotate(angle=randint(-30, 90), expand=False)
        return img

    def generate(self, code):
        self._img = Image.new(
            'RGBA',
            (self.width, self.height),
            color=self.font_background
        )
        # blur image
        self.img_blur(self._img)
        base = int(self.width / len(code))

        for pos, c in enumerate(code):
            txt_img = self._gen_txt_img(c, self.fontsize, self.font)
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

    def generate_digit(self):
        self.code = ''.join(str(random.randrange(10000, 100000)))
        self.generate(self.code)

    def generate_alpha(self):
        code_list = []
        for i in range(5):
            code_list.append(choice(string.ascii_letters))

        self.code = ''.join(code_list)
        self.generate(self.code)

    def generate_mix(self):
        code_list = []
        for i in range(5):
            code_list.append(choice(string.digits + string.ascii_letters))

        self.code = ''.join(code_list)
        self.generate(self.code)

    def get_img_bytes(self, fm='png'):
        binary_stream = BytesIO()
        self._img.save(binary_stream, fm)
        return binary_stream.getvalue()

    def get_img_base64(self, fm='png'):
        b64_img_prefix = 'data:image/png;base64,'
        base64_img = b64_img_prefix + base64.b64encode(self.get_img_bytes(fm)).decode()
        return self.code, base64_img

    def save(self, filename: str = None, fm='png'):
        if filename is None:
            self._img.save(self.code + '.' + fm, fm)
        else:
            self._img.save(filename, fm)


if __name__ == '__main__':
    vc = VerificationCode()
    # 验证码类型
    # 自定义验证码
    # vc.generate('abcd')
    # 数字验证码
    # vc.generate_digit()
    # 字母验证码
    # vc.generate_alpha()
    # 数字字符混合验证码
    vc.generate_mix()

    # 图片字节码
    # print(vc.get_img_bytes())
    # 图片base64编码
    # print(vc.get_img_base64())
    # 保存图片
    vc.save()