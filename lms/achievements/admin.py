from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelFilter, PolymorphicChildModelAdmin

from lms.achievements.models import Achievement, CourseAchievement, LessonAchievement, StepAchievement, TopicAchievement


class AchievementAdmin(PolymorphicParentModelAdmin):
    base_model = Achievement
    child_models = (StepAchievement,
                    LessonAchievement,
                    TopicAchievement,
                    CourseAchievement
                    )
    list_filter = (PolymorphicChildModelFilter,)
    list_display = ('id',
                    'user',
                    'points',
                    )
    list_display_links = ('id',
                          'user',
                          'points',
                          )
    search_fields = ('id',
                     'user',
                     'points',
                     )


class StepAchievementAdmin(PolymorphicChildModelAdmin):
    base_model = StepAchievement
    list_display = ('id',
                    'user',
                    'points',
                    'for_what',
                    )
    list_display_links = ('id',
                          'user',
                          'points',
                          'for_what',
                          )
    search_fields = ('id',
                     'user',
                     'points',
                     'for_what',
                     )


class LessonAchievementAdmin(PolymorphicChildModelAdmin):
    base_model = LessonAchievement
    list_display = ('id',
                    'user',
                    'points',
                    'for_what',
                    )
    list_display_links = ('id',
                          'user',
                          'points',
                          'for_what',
                          )
    search_fields = ('id',
                     'user',
                     'points',
                     'for_what',
                     )


class TopicAchievementAdmin(PolymorphicChildModelAdmin):
    base_model = TopicAchievement
    list_display = ('id',
                    'user',
                    'points',
                    'for_what',
                    )
    list_display_links = ('id',
                          'user',
                          'points',
                          'for_what',
                          )
    search_fields = ('id',
                     'user',
                     'points',
                     'for_what',
                     )


class CourseAchievementAdmin(PolymorphicChildModelAdmin):
    base_model = CourseAchievement
    list_display = ('id',
                    'user',
                    'points',
                    'for_what',
                    )
    list_display_links = ('id',
                          'user',
                          'points',
                          'for_what',
                          )
    search_fields = ('id',
                     'user',
                     'points',
                     'for_what',
                     )


admin.site.register(Achievement, AchievementAdmin)
admin.site.register(StepAchievement, StepAchievementAdmin)
admin.site.register(LessonAchievement, LessonAchievementAdmin)
admin.site.register(TopicAchievement, TopicAchievementAdmin)
admin.site.register(CourseAchievement, CourseAchievementAdmin)
