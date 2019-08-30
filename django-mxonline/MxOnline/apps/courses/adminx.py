__auther__ = "liangliang"

__date__ = "2019/6/23 10:06"

import xadmin

from .models import Course, Lesson, Video, CourseResource
from organization.models import CourseOrg

class CourseAdmin(object):

    list_display = ["name", "desc", "detail", "degree", "add_time",
                    "learn_times", "students", "fav_nums", "image", "click_nums", 'get_zj_nums', "go_to"]

    search_fields = ["name", "desc", "detail", "degree", "learn_times",
                     "students", "fav_nums", "image", "click_nums"]

    list_filter = ["name", "desc", "detail", "degree", "add_time",
                    "learn_times", "students", "fav_nums", "image", "click_nums"]
    list_editable = ['degree', 'desc']
    style_fields = {"detail": "ueditor"}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候，统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = CourseOrg.objects.filter(course_org=course_org).count()
            course_org.save()


class LessonAdmin(object):

    list_display = ["course", "name", "add_time"]
    search_fields = ["course", "name"]
    list_filter = ["course__name", "name", "add_time"]


class VideoAdmin(object):
    list_display = ["lesson", "name", "add_time"]
    search_fields = ["lesson", "name"]
    list_filter = ["lesson", "name", "add_time"]


class CourseResourceAdmin(object):
    list_display = ["course", "name", "add_time", "download"]
    search_fields = ["course", "name", "download"]
    list_filter = ["course", "name", "add_time", "download"]


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

