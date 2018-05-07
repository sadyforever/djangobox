from django.contrib import admin

# Register your models here.
from django.contrib import admin
from booktest.models import BookInfo,HeroInfo

# admin.site.register(BookInfo)
# admin.site.register(HeroInfo)

# class HeroInfoStackInline(admin.StackedInline):
#     model = HeroInfo  # 要编辑的对象
#     extra = 1  # 附加编辑的数量

admin.site.site_header = '传智书城'
admin.site.site_title = '传智书城MIS'
admin.site.index_title = '欢迎使用传智书城MIS'


class HeroInfoTabularInline(admin.TabularInline):
    model = HeroInfo
    extra = 1

@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = True

    list_display = ['id', 'btitle','pub_date']
    # fields = ['btitle', 'bpub_date']
    fieldsets = (
        ('基本', {'fields': ['btitle', 'bpub_date','image']}),
        ('高级', {
            'fields': ['bread', 'bcomment'],
            'classes': ('collapse',)  # 是否折叠显示
        })
    )

    # inlines = [HeroInfoStackInline]
    # inlines = [HeroInfoTabularInline]
@admin.register(HeroInfo)
class HeroInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'hname', 'hbook', 'read']
    list_filter = ['hbook', 'hgender']
    search_fields = ['hname']



