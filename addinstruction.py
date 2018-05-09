thing = 'DRF框架'
# 其实就是Django RESTful Framework
# RESTful一种API的命名风格,主要因为前后端分离开发出现
# 前后端分离: 用户访问静态文件的服务器,数据全部由ajax请求给到
# RESTful风格:数据应该是名词,而动词由HTTP的请求方式来体现
# RESTful风格的API给前端返回 结果对象,无论什么请求方式

'''
特点: 反复重复
因为不论什么请求方式,都需要给前端返回对象内容,就是json格式的
所以每次如果有查询的结果对象都需要遍历成字典,和flask相同

如果不是get请求是带有内容的请求,那从前端接收的是json格式
每次都需要从request.body中拿出内容,是bytes格式
然后decode解码成json字符串然后再loads成可以给python处理的字典
'''


'''
说明:
return JsonResponse(book_list, safe=False)
# 对safe的说明,我们传过去的book_list是一个list格式
# 在前端json支持{}格式也支持[]格式
# 但是django中认为[]的json格式是不安全的会进行校验
# 所以把safe选项关闭False,不进行校验就可以传[]
'''


'''
序列化：对查询结果进行遍历,然后转成字典,给到JsonResponse
反序列化：接收前端json处理成字典,然后校验
'''


'''
1.DRF框架工程搭建,建立在django的基础上
安装DRF: pip install djangorestframework
注册DRF: INSTALLED_APPS = ['rest_framework',]
在子应用中serializers.py创建序列化器,用于执行序列化和反序列化
在views中类视图使用序列化器,在urls中写地址
'''


'''
2.序列化器: serializer

定义: 其实ModelSerializer是Serializer的子类,更方便有模型类的序列化器的创建,实际产生的序列化器如下
class BookInfoSerializer(serializers.Serializer):   实际继承Serializer
    """图书数据序列化器"""      序列化器:执行序列化和反序列化
    id = serializers.IntegerField(label='ID', read_only=True)     read_only:只在输出响应中使用,就是给前端的时候,而前端给我们传请求的时候,不做验证
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
    
字段 : 跟模型类创建很相似,具体存在的字段见讲义   还有常用的参数(就是约束)


使用: 创建对象 serializer = Serializer(instance=None, data=empty, **kwarg)
             说明: 序列化时，将模型类对象传入instance参数   instance = 序列化对象
                    反序列化时，将要被反序列化的数据传入data参数    data = 反序列化对象
                    可通过context参数额外添加数据 即 **kwarg : context={'request': request}  通过Serializer对象的context属性获取
'''


'''
3.序列化操作 : 其实就是查询到对象之后,遍历构造字典的过程,而JsonResponse由内置的 Renderer渲染器来执行

3-1.序列化只使用序列化器对象的第一个参数instance
serializer = BookInfoSerializer(instance = book)
通过data属性可以获取序列化后的数据,这个data跟第二个参数可不是一个
serializer.data
# {'id': 2, 'btitle': '天龙八部', 'bpub_date': '1986-07-24', 'bread': 36, 'bcomment': 40, 'image': None}

3-2.如果要被序列化的是包含多条数据的查询集QuerySet,添加many=True参数
book_qs = BookInfo.objects.all()
serializer = BookInfoSerializer(book_qs, many=True)
serializer.data
'''


'''
4.关联对象嵌套序列化(由hero->book通过 hbook方法)

4-1.hbook是个外键: PrimaryKeyRelatedField
hbook = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
因为是外键,第二个位置必须有read_only=True 或者 查询集 queryset=BookInfo.objects.all() 要不报错
serializer.data 序列化的时候 结果是 关联对象的主键 {'hbook': 2}   即 book.id

4-2.因为id不直观,想要详细内容的字符串,把外键字段改为 :  StringRelatedField
hbook = serializers.StringRelatedField(label='图书')
结果: {'hbook': '天龙八部'}

4-3.接口链接: HyperlinkedRelatedField
hbook = serializers.HyperlinkedRelatedField(label='图书', read_only=True, view_name='books-detail')
必须指明view_name参数，以便DRF根据视图名称寻找路由，进而拼接成完整URL   这个view_name传什么:url中有1个参数,是命名空间,是跟它关联 
结果: {'hbook': 'http://127.0.0.1:8000/books/2/'}

4-4.关联对象的指定字段数据 :  SlugRelatedField
hbook = serializers.SlugRelatedField(label='图书', read_only=True, slug_field='bpub_date')
slug_field指明使用关联对象的哪个字段
结果:{'hbook': datetime.date(1986, 7, 24)}

4-5.使用关联对象的序列化器:  直接把所属book的所有内容序列化
hbook = BookInfoSerializer()
结果:{'hbook': OrderedDict([('id', 2), ('btitle', '天龙八部')te', '1986-07-24'), ('bread', 36), ('bcomment', 40), ('image', None)])}

'''


'''
5.重写to_representation方法
序列化器的每个字段实际都是由该字段的to_representation方法决定展示格式的，可以通过重写该方法来决定格式
注意,to_representations方法不仅局限在控制关联对象格式上，适用于各个序列化器字段类型
class BookRelateField(serializers.RelatedField):
    """自定义新的关联字段"""
    def to_representation(self, value):
        return 'Book: %d %s' % (value.id, value.btitle)

hbook = BookRelateField(read_only=True)
结果:{'hbook': 'Book: 2 天龙八部'}


重点: 上边的都是 多对一 关系 即使用hbook
    如果是 一对多 关系 即使用 heroinfo_set.all  此时关联字段类型通用,即上边的字段通用,但是需要添加many=True的参数
heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  

'''


'''
6.反序列化 : 接收前端传过来的json处理是由 Parser解析器 来执行,反序列化只进行验证和保存

使用: 
data = {'bpub_date': 123}
serializer = BookInfoSerializer(data=data)  构造对象,第一个参数instance不传,传data
serializer.is_valid()  # 返回False        调用验证方法
serializer.errors                        查看错误
# {'btitle': [ErrorDetail(string='This field is required.', code='required')], 'bpub_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].', code='invalid')]}
serializer.validated_data  # {}         标题没传,时间写错,当然获取不到,验证都没通过


6-1.验证 is_valid()方法
(1)报错:  序列化器对象的errors属性获取错误信息，返回字典，包含了字段和字段的错误
        非字段错误，可以通过修改REST framework配置中的NON_FIELD_ERRORS_KEY来控制错误字典中的键名
把报错给前端,显示HTTP 400 Bad Request请求错误 : is_valid(raise_exception=True) 开启参数      

(2)验证成功，可以通过序列化器对象的validated_data属性获取数据

(3)自定义验证,在执行is_valid时验证

(3-1)validate_<field_name> : 对字段进行验证
class BookInfoSerializer(serializers.Serializer):
    def validate_btitle(self, value):   验证btitle字段,value是传入的btitle值
        if 'django' not in value.lower():
            raise serializers.ValidationError("图书不是关于Django的")
        return value

(3-2)validate : 对多个字段进行比较验证时
class BookInfoSerializer(serializers.Serializer):
    def validate(self, attrs):      使用attrs
        bread = attrs['bread']
        bcomment = attrs['bcomment']
        if bread < bcomment:
            raise serializers.ValidationError('阅读量小于评论量')
        return attrs
        
(3-3)validators : 在字段中添加validators选项参数，也可以补充验证行为,这时候验证函数名随便起,   
                    但是验证哪个字段就在哪个字段加,其实就是方法(1-1),但是函数是写在class外部的,全局的
def about_django(value):
    if 'django' not in value.lower():
        raise serializers.ValidationError("图书不是关于Django的")  注意并不需要return
class BookInfoSerializer(serializers.Serializer):
    btitle = serializers.CharField(label='名称', max_length=20, validators=[about_django]) 注意是[]
    
REST framework内置的validators :
    单字段唯一 : UniqueValidator
            validators=[UniqueValidator(queryset=BlogPost.objects.all())]
    联合唯一 : UniqueTogetherValidation     是都唯一还是有一个唯一就行
            class ExampleSerializer(serializers.Serializer):
                # 写在类中
                class Meta:
                    validators = [
                        UniqueTogetherValidator(
                            queryset=ToDoItem.objects.all(),
                            fields=('list', 'position')
                        )]
'''


'''
6-2.保存

验证成功,validated_data可以取出数据,serializer.save()保存并返回数据对象,实际是执行create()和update()方法,好像不用重写,但是讲义中有具体执行过程

说明:
serializer.save(),save中可以传参数,参数可以在create()和update()中的validated_data参数获取到
默认序列化器必须传递所有required的字段，否则会抛出验证异常。但是我们可以使用partial参数来允许部分字段更新
serializer = CommentSerializer(comment, data={'content': u'foo bar'}, partial=True)

针对序列化器:三个参数,第一个参数好像可以作反序列化的对象使用, 有对象且必有data参数
                    而如果是序列化第一个参数作为序列化的对象,遍历它
'''


'''
7.子类 ModelSerializer

class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""
    class Meta:
        model = BookInfo        # 依据的模型类
        fields = '__all__'      # 所有字段

可以验证(shell): serializer = BookInfoSerializer()
            >>> serializer  可以看到结构

7-1.指定字段
(1) 指定 fields = ('id', 'btitle', 'bpub_date')
(2) 排除 exclude = ('image',)  注意是元组
(3) 指明只读字段 read_only_fields = ('id', 'bread', 'bcomment') 即只在序列化输出时使用

7-2.嵌套关系字段  depth
默认生成的hbook = PrimaryKeyRelatedField(label='图书', queryset=BookInfo.objects.all())就是个外键,并且以id来关联
嵌套的层级和详细信息   depth = 1
    hbook = NestedSerializer(read_only=True): 并且有所属书籍的详细信息

7-3.添加或修改原有参数
extra_kwargs = {
            'bread': {'min_value': 0, 'required': True}},
            'bcomment': {'min_value': 0, 'required': True}},
        }

修改了默认生成的序列化器中字段的参数
bread = IntegerField(label='阅读量', max_value=2147483647, min_value=0, required=True)
bcomment = IntegerField(label='评论量', max_value=2147483647, min_value=0, required=True)
'''