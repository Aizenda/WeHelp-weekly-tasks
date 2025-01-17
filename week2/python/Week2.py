print("-"*100+"task1"+"-"*100)
def find_and_print(messages, current_station):

    #建立車站順序list，方便後續使用
    green_line = {
        "Songshan" : 0, 
        "Nanjing Sanmin" :1,
        "Taipei Arena":2, 
        "Nanjing Fuxing":3,
        "Songjiang Nanjing" :4,
        "Zhongshan":5, 
        "Beimen":6,
        "Ximen":7,
        "Xiaonanmen":8, 
        "Chiang Kai-Shek Memorial Hall":9,
        "Guting":10, 
        "Taipower Building":11, 
        "Gongguan":12,
        "Wanlong":13, 
        "Jingmei":14, 
        "Dapinglin":15, 
        "Qizhang":16, 
        "Xindian City Hall":17, 
        "Xindian":18}
    
    Xiaobitan_line = {"Qizhang":0,"Xiaobitan":1}
    stations = {}
    for key , values in messages.items():
        for station in green_line.keys() | Xiaobitan_line.keys():
            if station in values:
                stations[key] = station
                break
    
    distance = {}
    #狀況1:都在綠線上
    #狀況2:一個在綠線 ， 一個在小碧潭線上
    #---> 狀況2-1 current_station在小碧潭線，station在綠線
    #---> 狀況2-2 current_station在綠線，station在小碧潭線
    #狀況3:都不再綠線上
    distance = {}
    for name, station in stations.items():

        if current_station in green_line and station in green_line:#都在綠線
            distance[name] = abs(green_line[current_station] - green_line[station])

        elif current_station in Xiaobitan_line and station in green_line:#current_station在小碧潭線，station在綠線 -->狀況2-1
             distance[name] = Xiaobitan_line[current_station] + abs(green_line['Qizhang'] - green_line[station])

        elif current_station in green_line and station in Xiaobitan_line:#current_station在綠線，station在小碧潭線 -->狀況2-2
            distance[name] = abs(green_line[current_station] - green_line['Qizhang']) + Xiaobitan_line[station]
             
        elif current_station in Xiaobitan_line and station in Xiaobitan_line:#都在小碧潭線
            distance[name] = abs(Xiaobitan_line[current_station] - Xiaobitan_line[station])
    
    min_sort = min(distance.values())
    names = []
    for key,values in distance.items():
        if values == min_sort:
            names.append(key)

    print(', '.join(names))

messages={
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."}

find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

print("-"*100+"task2"+"-"*100)

#先檢查時間 -> 時間ok -> 依照要求預約
#                       ->要求:價格
#                       ->要求:評分   
#           ->時間不ok -> 選擇要求第二的顧問
#           ->時間全部不ok -> No Service
def book(consultants, hour, duration, criteria):
    # 1. 計算要預約的時段
    booking_hours = set(range(hour, hour + duration))
    
    # 2. 找出有空的顧問
    available_consultants = []
    for consultant in consultants:
        # 檢查顧問是否有 office_hour 或是否有時間衝突
        if "office_hour" not in consultant or not booking_hours & set(consultant["office_hour"]):
            available_consultants.append(consultant)  
    # 3. 從可用的顧問中選出最適合的
    if not available_consultants:
        print("No service")
        return

    chosen = min(available_consultants, key=lambda x: x[criteria]) if criteria == "price" else max(available_consultants, key=lambda x: x["rate"])
    
    # 4. 更新選中顧問的預約時間
    for consultant in consultants:
        if consultant["name"] == chosen["name"]:
            if "office_hour" not in consultant:
                consultant["office_hour"] = list(booking_hours)
            else:
                consultant["office_hour"].extend(booking_hours)
        
    print(chosen["name"])

consultants=[
{"name":"John", "rate":4.5, "price":1000},
{"name":"Bob", "rate":3, "price":1200},
{"name":"Jenny", "rate":3.8, "price":800}
]

book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

print("-"*100+"task3"+"-"*100)
def func(*data):
    #處理姓名字數
    name_canter = []
    for i in data:
        if len(i) == 2 or len(i) == 3:
            i = i[1:2]
            name_canter.append(i)
        elif len(i) == 4 or len(i) == 5:
            i = i[2:3]
            name_canter.append(i)

    unique_indices = []
    for i in range(len(name_canter)):
        if name_canter.count(name_canter[i]) == 1:  # 檢查元素是否只出現一次
            unique_indices.append(i)

    if len(unique_indices) == 1:
        print(data[unique_indices[0]])
    else:
        print("沒有")
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆" ) # print 夏曼藍波安

print("-"*100+"task4"+"-"*100)
def get_number(index):
    # 初始值
    number = 0
    number_list = []
    
    # 從索引 0 開始迴圈直到指定的 index
    for i in range(index +1 ):
        number_list.append(number)
        number += 4
    # 等差數列 0, 4, 8,[12]...;但當index為3的倍數時 number為前項-1 與等差數列的12相差5,所以這邊-5
    # 變形等差 0, 4, 8,[7]...;
        if (i + 1 ) % 3 == 0:
            number -= 5
    print(number_list[index])
    
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70

print("-"*205)

