import time
import requests
from bs4 import BeautifulSoup


head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"}
def scrape_douban_top250():
    #初始变量
    base_url="https://movie.douban.com/top250"
    all_movie_name=[]
    all_score=[]
    all_short_comment=[]

    #依次爬取每一页数据
    for start in range(0,250,25):
        url=f"{base_url}?start={start}"
        page=start//25+1
        print(f"正在爬取第{page}页")

        #获取请求
        response=requests.get(url,headers=head)

        if response.ok:
            soup=BeautifulSoup(response.text,"html.parser")
            movies=soup.find_all("div",attrs={"class":"info"})
            #电影名称
            for movie in movies:
                movie_name=movie.find("span",attrs={"class":"title"})
                all_movie_name.append(movie_name.text)
            #电影评分
                score=movie.find("span",attrs={"property":"v:average"})
                all_score.append(score.text)
            #电影短评
                short_comment=movie.find("span",attrs={"class":"inq"})
                all_short_comment.append(short_comment.text.strip() if short_comment else "暂无短评")
        else:
            print(f"请求失败，状态码：{response.status_code}")

        time.sleep(2)

    for i,(movie_name,score,short_comment) in enumerate(zip(all_movie_name,all_score,all_short_comment),1):
        print(f"{i}.{movie_name}\t评分：{score}\t短评：{short_comment}")

    print(f"\n共爬取{len(all_movie_name)}部电影。")
if __name__ == "__main__":
    scrape_douban_top250()