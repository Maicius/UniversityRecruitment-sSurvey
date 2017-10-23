# University Recruitment's Survey

### 一个关于大学校园招聘的数据调查

> 受张雪峰老师演讲的影响，“什么样的企业会到齐齐哈尔大学招聘，什么样的企业会到清华大学招聘？”  
[张雪峰老师演讲讲学历重不重要](http://www.iqiyi.com/w_19rvh719ol.html)  
> 仔细思考之后，决定用严肃的数据来回答这个严肃对问题  
> 欢迎一起来搞事  
> 它主要包含以下部分:  

### 主要工作

- 1.爬取各个大学的就业信息网，获取到各个大学校园内进行宣讲或招聘的企业名单  
    注意是要获得进入大学进行宣讲或招聘的企业，而不是单纯的挂个通知的企业
    
- 2.根据某种标准对企业进行划分
- 3.数据分析


### 主要技术

- python 爬虫，beatuifulSoup/Requests等库
- 利用Redis进行存储（因为真的太方便了）

- 数据格式全部使用Json Array  
![数据格式](https://github.com/Maicius/UniversityRecruitment-sSurvey/blob/master/file/thu.png)
![数据格式]()