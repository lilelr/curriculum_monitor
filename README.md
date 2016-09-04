# curriculum_monitor
scrapy 应用

程序使用方法:
首先电脑配有python(>=2.7),并装好scrapy
以下修改全在curriculum_monitor/spiders/monitor_spider.py文件中
1.  第 33 行 monitor_curriculum_code = "*" *号改为自己想监听的课程代码
2.   第 65,66行, 修改为自己的 http://sep.ucas.ac.cn/ 登录用户名和密码
3.   打开chrome 浏览器,登录到选课系统主界面,右键单击出现可选菜单后,点击"审查元素",底部将会出现浏览器监控界面,如下图

![](http://7xtc7i.com1.z0.glb.clouddn.com/Snip20160904_2.png)

4. 点击选修课程下拉列表中的“选择课程”，选择“计算机学院”，点击“新增本学期研究生课程”，进入到计算机专业课选课界面，点击底部浏览器监控界面中的 ”应用” （Application) 菜单按钮，展开左侧 Cookies 列表，右侧将会出现本次会话的 JESSIONID,route,sepuser 信息，把对应的值复制到 monitor_spider.py中 100至102行相对应的值中，如下图。

![](http://7xtc7i.com1.z0.glb.clouddn.com/Snip20160904_3.png)

5. 点击底部浏览器监控界面中的 ”网络”（Network）菜单按钮，从左侧请求资源列表中找第一个请求名 “selectCourse?...”,点击它，复制右侧出现的 Request URL值 替换monitor_spider.py中 112 行 url 的值,如下图。

 ![](http://7xtc7i.com1.z0.glb.clouddn.com/Snip20160904_4.png)

6. 打开一个任意终端 ，输入”scrapy crawl monitor“ 即可实现一次监听。
   运行curriculum_monitor/monitor.sh脚本， 即执行 ”sh monitor.sh"即可实现每隔5分钟监听一次。监听间隔可修改monitor.sh 脚本中的一个数字，单位为秒。
