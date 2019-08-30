__auther__ = "liangliang"
__date__ = "2019/6/23 10:30"


import xadmin
from .models import CityDict, CourseOrg, Teacher
from courses.models import Lesson


class LessonInline(object):
    model = Lesson
    extra = 0


class CityDictAdmin(object):

    list_display = ["name", "desc", "add_time"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc", "add_time"]


class CourseOrgAdmin(object):

    list_display = ["name", "desc", "add_time", "click_nums",
                    "fav_nums", "image", "address", "city"]
    search_fields = ["name", "desc", "click_nums", "fav_nums",
                     "image", "address", "city"]
    list_filter = ["name", "desc", "add_time", "click_nums",
                   "fav_nums", "image", "address", "city"]
    relfield_style = 'fk_ajax'
    inlines = [LessonInline]


class TeacherAdmin(object):

    list_display = ["org", "name", "work_years", "work_company",
                    "work_position", "points", "click_nums", "fav_nums", "add_time"]

    search_fields = ["org", "name", "work_years", "work_company",
                    "work_position", "points", "click_nums", "fav_nums"]

    list_filter = ["org", "name", "work_years", "work_company",
                    "work_position", "points", "click_nums", "fav_nums"]


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
