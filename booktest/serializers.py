from rest_framework import serializers

from booktest.models import BookInfo, HeroInfo


# 模型序列化器 继承于serializer 让我们简便使用序列化器
class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""
    class Meta:
        model = BookInfo        # 声明属于哪个类
        fields = '__all__'      # 声明包含的字段:所有



# class HeroInfoSerializer(serializers.Serializer):
#     """英雄数据序列化器"""
#     GENDER_CHOICES = (
#         (0, 'male'),
#         (1, 'female')
#     )
#     id = serializers.IntegerField(label='ID', read_only=True)
#     hname = serializers.CharField(label='名字', max_length=20)
#     hgender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
#     hcomment = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)
#     hbook = BookInfoSerializer()
#
#
#
# class BookInfoSerializer(serializers.Serializer):
#     """图书数据序列化器"""
#     id = serializers.IntegerField(label='ID', read_only=True)
#     btitle = serializers.CharField(label='名称', max_length=20)
#     bpub_date = serializers.DateField(label='发布日期', required=False)
#     bread = serializers.IntegerField(label='阅读量', required=False)
#     bcomment = serializers.IntegerField(label='评论量', required=False)
#     image = serializers.ImageField(label='图片', required=False)
#     # heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # 新增
#     heroinfo_set = HeroInfoSerializer(many=True)


class HeroInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroInfo
        fields = '__all__'




