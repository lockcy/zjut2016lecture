zjut 2016级16选8讲座抢票工具

预装环境：python3.6  nonebot requests等库 酷q

运行时登录酷q

将所要信息填入request1.py的q_data中（支持多条信息）

同时运行main.py和request1.py

重新运行时清空awesome\plugins\re.txt 文件，否则会向上一次的问卷提交

注意验证码识别api账号密码的填写

5.8
因为若快会存在崩溃的情况，更新了post的脚本，使用了https://www.jianshu.com/p/34961ceedcb4
现在不需要验证码了

5.10
对关键部分进行url编码，start_time参数可以精确到秒（不是很清楚wjx的判定...），同时通过延时，减少了被发现的几率
