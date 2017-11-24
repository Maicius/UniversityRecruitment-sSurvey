# University Recruitment's Survey

### How to Begin

> 1. 配置开发环境python3, 建议配置redis，若未配置redis，则使用json文件存储数据
> 2. Fork代码,通过pull request提交
> 3. 查看[大学名单](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/%E6%8B%9F%E7%88%AC%E5%8F%96%E7%9A%84%E5%A4%A7%E5%AD%A6%E5%90%8D%E5%8D%95.md) ,其中未添加链接的表示还没有爬取信息的大学，选择其中一个大学进行爬取
> 4. 为了避免重复工作，请在正式开始爬取之前打开一个 **issue**, 告诉大家你要爬取的大学名称，并在爬取完成后在[大学名单](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/%E6%8B%9F%E7%88%AC%E5%8F%96%E7%9A%84%E5%A4%A7%E5%AD%A6%E5%90%8D%E5%8D%95.md)里添加相应的链接

### 一个关于大学校园招聘的数据调查

> 受张雪峰老师演讲的影响，“什么样的企业会到齐齐哈尔大学招聘，什么样的企业会到清华大学招聘？”  
[张雪峰老师演讲讲学历重不重要](http://www.iqiyi.com/w_19rvh719ol.html)  
> 仔细思考之后，决定用严肃的数据来回答这个严肃对问题  
> 欢迎一起来搞事  
> 它主要包含以下部分:  

### 主要工作

- 1.爬取各个大学的就业信息网，获取到各个大学校园内进行宣讲或招聘的企业名单  
    注意是要获得进入大学进行宣讲或招聘的企业，而不是单纯的挂个通知的企业
    （先爬100所大学吧）
    
- 2.根据某种标准对企业进行划分
- 3.数据分析


### 主要技术

- python 爬虫，beatuifulSoup/Requests等库
- 利用Redis进行存储（因为真的太方便了）

- 数据格式全部使用Json Array  
![数据格式](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/thu.png)
![数据格式](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/comany_info.png)


### 已爬取的大学就业信息网(持续更新)

#### C9

- [清华大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/c9/TsingHuaRecruitment.py)
- [南京大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/c9/NJURescruitment.py)
- [上海交通大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/Recruitment.py)
- 中国科学技术大学[代码](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/c9/USTCRecruitment.py) [数据](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/data/ustc_company_info.json)
- 浙江大学 [代码](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/c9/ZJURescruitment.py) [数据](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/data/zju_company_info.json)
- 复旦大学 [代码](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/c9/FDURescruitment.py) [数据](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/data/fdu_company_info.json)
- [哈尔滨工业大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/c9/HITRescruitment.py)
- [北京大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/c9/PKURecruitment.py)
- [西安交通大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/c9/XJTURecruitment.py)

#### 985

- [四川大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/main/Recruitment.py)
- [兰州大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/part985/LZURecruitment.py)
- [电子科技大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/part985/UESTCRecruitment.py)
- [重庆大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/part985/CQURescruitment.py)
- [华中科技大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/part985/HUSTRecruitment.py)
- [中南大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/part985/CSURecruitment.py)

#### 211

- [中央财经大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/part211/CUFERescruitment.py)
- [上海财经大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/part211/SUFERescruitment.py)
- [北京科技大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/part211/USTBRecruitment.py)

#### 一本

- [华北电力大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/top_public/NCEPURecruitment.py)暂时只获取了招聘会信息，双选会信息不全
- [南京邮电大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/top_public/NJUPTRecruitment.py)
- [北方工业大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/top_public/NCUTRecruitment.py)
- [燕山大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/top_public/YSURecruitment.py)
- [华侨大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/top_public/HQURecruitment.py)
- [杭州师范大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/top_public/HZNURecruitment.py)

#### 二本

- [四川大学锦城学院](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/JinChengRecruitment.py)
- [上海海关学院](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/SCCRecruitment.py)
- [成都信息工程大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/CUITRecruitment.py)
- [天津工业大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/TJPURecruitment.py)
- [温州大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/WZURecruitment.py)
- [烟台大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/YTURecruitment.py)
- [北京石油化工学院](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/BIPTRecruitment.py)
- [江汉大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/JHURecruitment.py)
- [浙江大学城市学院](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/basic_public/ZUCCRecruitment.py)

### 已爬取的公司名单（持续更新）

- [世界500强、中国500强、美国500强](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/enterprise/Top500.py)
- [中国民营企业500强、中国民营企业制造业500强、中国民营企业服务器100强](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/enterprise/China/ChinaPrivateTop500.py)
- [中国互联网企业100强](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/enterprise/China/ChinaInternetTop100.py)
- [咨询公司Top75](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/enterprise/financial/consult_top100.py)
- [投资机构Top100](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/enterprise/financial/InvestmentTop100.py)

### 其它

- [IT橘子网](https://github.com/Maicius/UniversityRecruitment-sSurvey/tree/master/CaptureITJUZI)(可根据关键字查询IT公司的融资情况)

### 一个简单的爬虫教程（欢迎加入这个项目）

> 大学就业信息网的结构大多十分简单，也没有什么验证码机制，所以用来入门爬虫的话再合适不过了
> 下面以兰州大学为例，我们爬取到兰州大学进行招聘到企业名单

- 1.首先，百度兰州大学就业信息网（基本上百度 xx大学就业信息网都能找到相应的网站），然后进去找到要到兰大进行宣讲大企业公示
- 2.注意不要找发布招聘信息的企业，那些企业不一定会到兰大进行宣讲，与我们的目标不合，最终，找到的网页如下:  
  
  ![兰大就业网专场招聘会](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/1.png)
  
- 3.打开浏览器开发者工具(推荐使用Chrome或火狐浏览器)，选择network 进行查看，点击每一条请求，查看其Response, 如果response中包含我们想要的数据，就记录下这条链接。如下图：  

  ![开发者模式](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/2.png)
  
- 4.因为通常一条请求中不会包含所有我们想要的数据，往往只有一页的数据，所以需要分析每条链接的构成规则，通常点击一下下一页或上一页，看浏览器中URL的变化，很快就明白了:  

  ![URL](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/3.png)
  ![URL](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/4.png)
  
- 5.如图，兰大的URL构成非常简单, 一共有50页，所以我们只需要循环构造 **list_1.shtml**这个参数就行
- 6.可以开始写代码了，构造URL，构造请求头， 对返回的内容解码，解析交给BeautifulSoup来做:


		base_url = "http://job.lzu.edu.cn/htmlfile/article/list/119/list_"
		url_tail = ".shtml"
    	host = "job.lzu.edu.cn"
    	header = Util.get_header(host)
    	max_page_num = 50
    	req = requests.Session()
    	re = Util.jedis()
    	re.connect_redis()
    	for i in range(1, max_page_num + 1):
        	url = base_url + str(i) + url_tail
        	html = req.get(headers=header, url=url).content.decode("utf-8")
        	parse_html(html, re)
        		print(i)
    	re.add_university("lzu_company_info")
    	print("finish")
- 7.这样就获得了完整的网页内容，下面开始解析, 将网页内容转化为BeautifulSoup的对象, 通过刚刚对网页的分析可以发现，所有我们想要的数据都被包裹在li中，所以，使用soup.find_all("li"),得到下面这样的效果：

  ![debug](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/7.png)
- 8.因为网页中使用li包裹的还有很多我们不想要的数据，可以根据数据下标进行准确的截取，比如兰大这个网页中，我们想要的数据在数组的第 24 到 77,因为静态网页的格式十分固定，所以可以直接设置数组下标范围进行截取。
- 9.通过debug（或者直接记住）,这些标签中的文字信息，在.text属性中，如图：
  
  ![debug](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/8.png)  

- 10.循环打印text,基本获得我们想要的数据:  
  ![debug](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/9.png)

- 11.格式化数据格式，将日期与文字分开，并去掉空白行，将数据存储进Redis中。在redis中的所有数据都保存为json格式（相应函数封装在util.Jedis里面）  
   ![redis](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/10.png)
- 12.这样，就完成了兰州大学的爬虫工作。大学网站大同小异，基本都是这种套路，具体的可以参考上面的源代码
- 13.欢迎一起来玩，直接Fork这个项目提交pull request就行,我真的很想看看，什么样的企业会到什么样的大学去招聘

### 一些动态网页的爬取技巧

- **强烈推荐使用火狐和Chrome浏览器**,两者搭配干活不累
- 1.动态网页的爬取着重分析URL和header的构成，建议在火狐浏览器下进行分析，因为火狐可以自动解析，方面读取，如图  
   ![火狐浏览器解析](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/json.png)  
- 2.动态网页的数据一般（只是一般）放在json格式的文件中，爬虫只需要获得该文件做解析就行。

- 3.在找到了获得返回数据的url之后，可以在火狐浏览器上编辑重发链接，测试数据是否正常
- 
- 4.有个很bug的行为，很多大学（比如中南大学和中国科学技术大学）的网站，获取数据的参数里有个叫pageSize（大概就是指定一次返回多少数据的参数）,见图：  
    ![pageSize](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/pagesize.png)  
    通常默认的是15或20这样的数字，表示一页返回15或20条数据，如果改变这个参数，比如直接设定为10000，那就能直接获得所有数据，就不用改变padeIndex发送多次请求了（就是说不用翻页了）  
    ![pageSize](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/chongfa.png) 
    
- 5.留意http header里Referer这个参数，它表示请求从哪里传过去的，比如请求B网页的header包含网页A的URL，表示这个B网页必须从A网页跳转过去，如果header里没有这个参数的话，直接爬是爬不了的。

- 6.需要登录的网站爬虫，一般使用cookie就行了，获取cookie的方式有很多，比如使用requests.Session()，但最简单的，用浏览器登录一遍再把cookie直接复制到header里就行了
- 7.有些网站的URL构成看起来莫名其妙,需要花点时间去分析构成，这个时候可能需要一些编码转换，推荐[站长转换工具](http://tool.chinaz.com/Tools/urlencode.aspx).推荐使用Visual Studio Code来分析复杂的URL,因为它有一个很神奇的功能,见图:  
   ![VSCode](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/VSCode.png)这样很容易发现规律
- 8.不是所有复杂的URL都需要花时间去分析，因为那个参数可能根本就没多大影响，比如清华大学这个的，即使为空也不影响获取数据:  
   ![callback](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/url.png)