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