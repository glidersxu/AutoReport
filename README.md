## 目标

实现《小学生睡眠情况日报》（使用腾讯文档）每日自动填报睡眠时间。

## 实现路径

1、使用python开发，利用selenium测试类，实现自动登录、自动填报。

2、使用windows自带任务计划，新增一个任务。



---

## 开发过程

开发环境：Win7+pycharm+python3.8

主要功能：

- 自动登录

- 自动填报

- 表格定位

- 随机时间

### **自动**登录

自动登录腾讯文档(使用时必须要先登录QQ)。这里最主要是找到登录按钮的className。目前根据页面不同有两种方式，按实际情况选择

1、先显示只读表格，点击右上角登录

```Python
elmet = driver.find_element_by_id("header-login-btn")
elmet.click()
time.sleep(2)
driver.switch_to.frame("login_frame")
elmet = driver.find_element_by_id("img_out_你的QQ号码")# 需要修改
elmet.click()
# 转换frame
driver.switch_to.parent_frame()
time.sleep(5)
```

2、先显示登录页面，登录后进入表格

```Python
elmet = driver.find_element_by_id("blankpage-button-pc")
elmet.click()
time.sleep(3)
# 得提前登录qq，因为这里用了快捷登录接口
driver.switch_to.frame("login_frame")
elmet = driver.find_element_by_id("img_out_你的QQ号码")# 需要修改
elmet.click()
# 转换frame
driver.switch_to.parent_frame()
time.sleep(5)
```







### **表格**定位

前期走了很多弯路，想通过键盘事件、鼠标事件去定位，但都失败了。后借鉴网络上的资料，得知腾讯文档网址里面有隐藏的表格位置。[https://腾讯文档地址?tab=g273er&c=](https://docs.qq.com/sheet/DRGFOR09Qc2hMTnNs?tab=g273er&c=)E23A0A0，其中C=E23即为腾讯文档中的E列23行。因此只需要去定义行列的标量即可。本次我仅需要定义列的变量即可。



```Python
    # print(workdays('2021-08-31','2021-09-14'))  #数据测试用
    date_str = "2021-08-31"  # 开始打开日期
    date_end = datetime.now().strftime('%Y-%m-%d')
    caltime = workdays(date_str, date_end)  # 计算从开始打卡到今天间隔的工作日天数
    start = 3  # 开始填表的列数
    c = chr(int(caltime) + start - 1 + 65)  # 计算偏量值1
    # print(c)
    h = 43  # 行号，即你要填写对应的行号
  
    url = "https://腾讯文档地址&c=" + c + str(h) +"A0A0" # 需要修改
```

那么我们只要弄控制行、列这两个变量就可以完美的解决定位问题。在本需求中（如下图），行是固定的，难点在列，并不是按照自然月来的，而且只有工作日，所以我定义一个计算两个日期间工作日天数的函数，这样就可以去控制列数。



![](https://secure.wostatic.cn/static/qDLa3WqSMaRgTDyZ7Lf5mZ/微信图片_20210914115033.png)

```Python
def workdays(start,end):
    '''
    计算两个日期间的工作日
    start:开始时间
    end:结束时间
    '''
     # 字符串格式日期的处理
    if type(start) == str:
        start = datetime.strptime(start,'%Y-%m-%d').date()
    if type(end) == str:
        end = datetime.strptime(end,'%Y-%m-%d').date()
    # 开始日期大，颠倒开始日期和结束日期
    if start > end:
        start,end = end,start
    counts = 0
    while True:
        if start > end:
            break
        if is_workday(start):
            counts += 1
        start += timedelta(days=1)
    return counts
```

### 随机时间

既然是每日打卡，每天都填写同一个时间显的太不真实，所以我通过random()函数随机从数组中选择一个。

```Python
sleeptime = ['21:00', '21:10', '21:20', '21:30', '21:40', '21:50', '21:35']
sleeptime = random.choice(sleeptime)
```

### 数据录入

定位和数据都准备妥当，那现在就录入即可。如果需要一次性录入多条，那增加相应sengd_key即可，如果都是同一个变量，可通过循环语句重复。

```Python
elmet = driver.find_element_by_class_name('formula-input')
elmet.click()
elmet.send_keys(sleeptime)  # 输入xxx,即你想输入的字符
time.sleep(1)
elmet.send_keys(Keys.ENTER)
time.sleep(3)
elmet.send_keys(Keys.TAB)
```



---

## 其它

### 生成exe文件

```Bash
pyinstaller -F ***.py
```



制定windows任务计划

这部分就不写了

---

## 完整代码



[完整代码](https://www.wolai.com/bn45fLrH5MB6EPi9HuDrr7)

