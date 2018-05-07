thing = ''

'''
1.表单

django内置表单的内容, 使用forms模块的Form类
在单独的forms.py文件中创建表单类和创建模型类的方法很像, 然后视图类用到表单,实例对象就可以

Form类中内置一些方法,提供我们使用
比如:form = BookForm(request.POST) post上传的请求数据,通过自定义的表单类拿出
    form.is_valid() 验证表单数据的合法性
    form.cleaned_data 获取验证后的表单数据
    
快速创建表单:
表单中的数据与模型类对应,通过指定是哪个模型类
class BookForm(forms.ModelForm): # 必须继承ModelForm
    class Meta:
        model = BookInfo    # model 指明从属于哪个模型类
        fields = ('btitle', 'bpub_date')    # fields 指明向表单中添加模型类的哪个字段
'''


'''
2.admin

创建管理员 python manage.py createsuperuser
admin站点是管理数据库模型的
需要注册进去 admin.py :   admin.site.register(BookInfo)

默认的功能不能满足,需要定制化,自定义admin效果, 必须继承admin中ModelAdmin
class BookInfoAdmin(admin.ModelAdmin):
    # 具体添加的功能
    
使用自定义的模型管理器(注册进去)
方法1:放到第二个参数 admin.site.register(BookInfo,BookInfoAdmin)
方法2:@admin.register(BookInfo)
     class BookInfoAdmin(admin.ModelAdmin):
'''


'''
3.admin定制化 -> 列表页

(1)每页中显示多少条数据: list_per_page = num
(2)操作选项 的位置 : actions_on_top=True
                actions_on_bottom=False
(3)列表中的列 : list_display=['id','btitle',...]
(4)将函数方法作为列 : 设置short_description属性
注意class BookInfo(models.Model): 定义的方法是在模型类中,然后short_description把方法可以当做字段来用
    def pub_date(self):
        return self.bpub_date.strftime('%Y年%m月%d日') 改变时间的显示格式,定义一个方法
    pub_date.short_description = '发布日期'  函数方法.short_description # 设置方法为字段在admin中显示的标题
admin中:    
    list_display = ['id','btitle','pub_date']  # 这样就可以把方法当做字段写进去
(5)方法列是不能排序的，如果需要排序需要为方法指定排序依据。
    admin_order_field=模型类字段  注意也是在模型类中
(6)关联对象:无法直接访问关联对象的属性或方法，可以在模型类中封装方法，访问关联对象的成员。
    def read(self):
        return self.hbook.bread
    read.short_description = '图书阅读量'   
(7)右侧栏过滤器 
 list_filter = ['hbook', 'hgender']
(8)搜索框
search_fields = ['hname']
'''


'''
4.admin定制化 -> 详情编辑页

(1) 显示字段 : fields = ['btitle', 'bpub_date'] 详情页只显示这两个字段
(2)分组显示 : fieldsets = (
                ('基本', {'fields': ['btitle', 'bpub_date']}),
                ('高级', {
                    'fields': ['bread', 'bcomment'],
                    'classes': ('collapse',)  # 是否折叠显示})
                )

(3)关联对象 (嵌入)
在一对多的关系中，可以在一端的编辑页面中编辑多端的对象，嵌入多端对象的方式包括表格、块两种。
子类TabularInline：以表格的形式嵌入。
子类StackedInline：以块的形式嵌入。
块: 自定义 class HeroInfoStackInline(admin.StackedInline):
            model = HeroInfo  # 要编辑的对象
            extra = 1  # 附加编辑的数量

在 BookInfoAdmin(admin.ModelAdmin) 中 嵌入 inlines = [HeroInfoStackInline]

表格: 自定义 class HeroInfoTabularInline(admin.TabularInline):  就是继承的不同
                model = HeroInfo
                extra = 1
嵌入 inlines = [HeroInfoTabularInline]


站点信息:

admin.site.site_header 设置网站页头
admin.site.site_title 设置页面标题
admin.site.index_title 设置首页标语
比如:
admin.site.site_header = '传智书城'
admin.site.site_title = '传智书城MIS'
admin.site.index_title = '欢迎使用传智书城MIS'


上传图片:
pip install Pillow
配置:
MEDIA_ROOT=os.path.join(BASE_DIR,"static_files/media")
添加字段:
image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
upload_to 选项指明该字段的图片保存在MEDIA_ROOT目录中的哪个子目录
'''