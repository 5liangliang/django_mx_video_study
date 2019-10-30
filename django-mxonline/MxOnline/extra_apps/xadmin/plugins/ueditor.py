__auther__ = "liangliang"
__date__ = "2019/7/25 13:26"


import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, ModelFormAdminView, UpdateAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from django.conf import settings


class XadminUEditorWidget(UEditorWidget):
    def __init__(self, **kwargs):
        self.ueditor_options = kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)


class UeditorPlugin(BaseAdminPlugin):

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == "ueditor":
            if isinstance(db_field, UEditorField):
                widget = db_field.formfield().widget
                params = {}
                params.update(widget.ueditor_settings)
                params.update(widget.attrs)
                return {"widget": XadminUEditorWidget(**params)}
        return attrs

    # 在我们生成的页面中放入自己的js文件
    def block_extrahead(self, context, nodes):
        js = '<script type="text/javascript" src="%s"></script>'%(
            settings.STATIC_URL + "ueditor/ueditor.config.js")  # 自己的静态目录
        js += '<script type="text/javascript" src="%s"></script>'%(
            settings.STATIC_URL + "ueditor/ueditor.all.min.js")  # 自己的静态目录
        nodes.append(js)


# 新增页面
xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)
# 修改页面
xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)