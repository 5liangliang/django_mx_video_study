__auther__ = "liangliang"
__date__ = "2019/6/29 21:14"
import re
from django import forms


from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        # 相当于中间件，在进行is_valid的时候就会自动使用这个函数
        # cleaned_data field已经clean了，我们将field的数据存放到这个变量中
        mobile = self.cleaned_data['mobile']

        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")