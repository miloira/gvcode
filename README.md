### 代码示例

```python
from gvcode import VerificationCode


if __name__ == '__main__':    
    vc = VerificationCode()
    # 验证码类型
    # 自定义验证码
    # vc.generate('abcd')
    # 数字验证码
    # vc.generate_digit()
    # 字母验证码
    # vc.generate_alpha()
    # 数字字母混合验证码
    vc.generate_mix()

    # 图片字节码
    # print(vc.get_img_bytes())
    # 图片base64编码
    # print(vc.get_img_base64())
    # 保存图片
    vc.save()
```