__auther__ = "liangliang"
__date__ = "2019/6/26 16:41"


from random import Random
from django.core.mail import send_mail
# import uuid
# import hashlib

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgijklmnopqrstuvwxyz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# def get_random_str():
#     uuid_val = uuid.uuid4()
#     uuid_str = str(uuid_val).encode("utf-8")
#     md5 = hashlib.md5()
#     md5.update(uuid_str)
#     return md5.hexdigest()

def send_register_email(email, send_type="register"):
    # 实例化一个邮箱验证对象，将code、email、send_type
    # 都传入这个对象，进行保存
    # 将需要发送的code事先保存到数据库中
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "小吴视频在线教育网激活链接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        # 判断邮件发送是否成功
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "小吴视频在线教育网密码重置链接"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        # 判断邮件发送是否成功
        if send_status:
            pass

    elif send_type == "update_email":
        email_title = "小吴视频在线教育网邮箱修改验证码"
        email_body = "你的邮箱验证码为：{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        # 判断邮件发送是否成功
        if send_status:
            pass