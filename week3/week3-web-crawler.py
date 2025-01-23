import urllib.request as req
import json , re , csv
#task2使用
from bs4 import BeautifulSoup as soup

#Task1 start
def Task1(regional_URL , MRT_URL):

    header={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    #地理資訊請求，獲取資料
    regional_request = req.Request(regional_URL , headers = header)
    regional_reponse = req.urlopen(regional_request).read()
    regional_data = json.loads(regional_reponse)["data"]["results"]

    #MRT資訊請求，獲取資料
    MRT_request = req.Request(MRT_URL , headers = header)
    MRT_reponse = req.urlopen(MRT_request).read()
    MRT_data = json.loads(MRT_reponse)["data"]

    #處理MRT資訊 => {"SERIAL_NO" : "地名"}
    MRT_to_district = {}
    for i in MRT_data:
        district = i["address"].split(" ")[2][0:3]
        i["address"] = district
        serial_no = i["SERIAL_NO"]
        MRT_to_district[serial_no] = district

    #處理MRT資訊 => {站名 : list[SERIAL_NO] }
    MRT_request = {}
    for i in MRT_data:
        mrt = i["MRT"]
        serial_no = i["SERIAL_NO"]
        if mrt not in MRT_request:
            MRT_request[mrt] = []
        MRT_request[mrt].append(serial_no) 


    pattern = r"https://.*?\.[Jj][Pp][Gg]"

    #獲取Spot.csv & MRT.csv所需資料
    Spot_results = []
    MRT_results= {}
    for i in regional_data:

        title = i["stitle"]
        longitude = i["longitude"]
        latitude = i["latitude"]
        serial_no =  i["SERIAL_NO"]
        imgs = re.findall(pattern , i["filelist"])
        img = imgs[0] if imgs else "No Image Available"

        for mrt_station, district in MRT_to_district.items():# 判斷資料是否包含SERIAL_NO
            if mrt_station in i.get("SERIAL_NO", ""):# 如果找到匹配的地鐵站，添加到結果
                result = [
                    title,
                    district,
                    longitude,
                    latitude,
                    img
                    ]
                Spot_results.append(result)

        for MRT_name , serial_numbers in MRT_request.items():
            if MRT_name not in MRT_results:
                MRT_results[MRT_name] = []
            if serial_no in serial_numbers:
                MRT_results[MRT_name].append(title) 



    # 指定檔案位置，這裡用完整路徑
    Spot_path = r"D:\weekly tasks\week3\Spot.csv"
    MRT_path = r"D:\weekly tasks\week3\mrt.csv"

    # 打開檔案並寫入資料
    with open(Spot_path, mode='w', newline='\n', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(Spot_results)
        csv_writer.writerows(" ")

    with open(MRT_path, mode='w', newline='\n', encoding='utf-8') as file:
        csv_writer = csv.writer(file, quoting=csv.QUOTE_NONE,escapechar=" ")
        for key, values in MRT_results.items():
                csv_writer.writerow([key, ",".join(values)])

Attractions_URL = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
MRT_URL = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"


Task1(Attractions_URL , MRT_URL)
#Task1 end

#Task2 start

def Task2(ptt_url):
    header_2 = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "cookie":"over18=1"}
    ptt_request = req.Request(ptt_url , headers=header_2)
    ppt_response = req.urlopen(ptt_request).read().decode("utf-8")

    root = soup(ppt_response , "html.parser")
    data = root.find_all("div" , class_="r-ent")

    article_list = [] 
    for article in data:
        if (article.a !=None):
            title = article.a.string
            if article.span != None:
                like = article.span.string
            else:
                like = article.span

            result = [
                title,
                like
                ]
                
            article_list.append(result)

    url_list = []
    for url in article_list:
        article_title = url[0]
        get_url = root.find("a" , string=article_title) 
        url_list.append(get_url["href"]) 

    count = 0 
    for i in url_list:

        article_url = "https://www.ptt.cc" + i 
        url_request = req.Request(article_url , headers=header_2)
        url_response = req.urlopen(url_request).read().decode("utf-8")
        root = soup(url_response , "html.parser")
        time_data = root.find_all("span" , class_="article-meta-value")

        if len(time_data) > 3:  
            article_list[count].append(time_data[3].string)  
        else:
            article_list[count].append(" ") 

        count += 1

    article_path = r"D:\weekly tasks\week3\article.csv"
    with open(article_path, mode='a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(article_list)


    root = soup(ppt_response , "html.parser")
    next_link = root.find("a" , string = "‹ 上頁")
    return next_link["href"]
   
    
ptt_url = "https://www.ptt.cc/bbs/Lottery/index.html"

count = 0
while count<3:
    ptt_url = "https://www.ptt.cc" + Task2(ptt_url)
    count += 1

#Task2 end
