
### 安装
```shell script
pip install gvcode
```

### 例子
```python
from gvcode import VFCode



if __name__ == '__main__':
    vc = VFCode()
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
```