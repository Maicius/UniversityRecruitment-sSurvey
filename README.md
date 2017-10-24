# University Recruitment's Survey

### How to Begin
> 1. 配置开发环境， python 3, redis
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

- [清华大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/TsingHuaRecruitment.py)
- [南京大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/NJURescruitment.py)
- [上海交通大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/Recruitment.py)
- [哈尔滨工业大学]()
#### 985
- [四川大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/Recruitment.py)
- [兰州大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/LZURecruitment.py)

#### 211

- [中央财经大学](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/CUFERescruitment.py)

#### 其他

- [四川大学锦城学院](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/university/JinChengRecruitment.py)


### 已爬取的公司名单（持续更新）

- [世界500强、中国500强、美国500强](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/enterprise/Top500.py)


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