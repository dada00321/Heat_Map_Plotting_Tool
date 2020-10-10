from modules.excel_reader import get_address_list
from modules.gmap_crawler import get_coordinate
from modules.map_plotting_class_version import MapPlottingAssistant 
import os
import csv
import time
import random

"""
###################################################################
Part 1: 
    (1) Read address info from excel(.xlsx) files
        (using module func: get_address_list)
    (2) Crawl geographical latitude and longitude info
        (using module func: get_coordinate)
    (3) Plot the heapmap and other graphs
        (using module class: MapPlottingAssistant)
###################################################################
"""

''' [Notice] This func: 'get_addresses_dict' is different from 
                        'get_address_list' (method of outer module)
'''
def get_addresses_dict(excel_files_path):
    excel_files = os.listdir(excel_files_path)
    #print(excel_files)
    
    data_amount = 0
    addresses_dict = dict()
    for i in range(len(excel_files)):
    #idx = 4
    #for i in range(idx, idx+1):
        path = excel_files_path + excel_files[i]
        start_row = 5  # 起始 row
        col_name = "K" # "通訊地址"所在column
        address_list = get_address_list(path, start_row, col_name)
        data_amount += len(address_list)
        #print(address_list[:5])
        addresses_dict.setdefault(excel_files[i], address_list)
    #print(addresses_dict)
    print(f"\n資料源: {len(excel_files)}個excel檔案")
    print(f"共有{data_amount}筆資料")
    return addresses_dict, data_amount

''' 
    module: prepare_csv_data
    功能:   產生中繼資料 (後續再送交csv檔案儲存模組，存成csv檔)
           將所有excel文件中的所有地址，一個個用爬蟲程式取出經緯度資訊，
           並保存到csv檔。
    [注意] 爬蟲程式在連續傳送太多次請求後，可能會被對方網站擋下。
           故必須紀錄爬蟲失敗的ID，並在下一次從它開始。(休息一下或換proxy/IP接續爬)
'''
def prepare_csv_data(dict_obj, data_amount, num_list):
    is_completed = False
    csv_data_list = list()
    filename = "address_data.csv" # 中繼csv資料
    csv_path = f"./res/{filename}"
    
    startID = None
    if not os.path.exists(csv_path): # 第一次執行
        startID = 1
    else:
        with open(csv_path, mode='r', encoding="utf-8-sig") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            # 去除row 1(欄位名稱)後可得出記錄筆數
            record_amount = len([record for record in csv_reader]) - 1
            if record_amount == data_amount:
                is_completed = True
        startID = record_amount + 1
    
    if is_completed:
        print("csv檔案資料已全數建置成功！")
        return None
    else:
        print(f"從 ID:{startID} 開始爬經緯度...")
        # 取得 indices，以從 given dict中 "list起始索引值"、"元素所在該list之起始索引值" 的資料開始爬蟲
        index_1, index_2 = get_indeices_whereToExecute(startID, num_list)
        
        counter = startID
        # 到 google maps抓一組地址的經緯度精實測約需3秒
        aver_stop_time = 1.432 # 平均一次執行的暫停時間
        ''' 共需約4.432秒/抓取一組經緯度資料 '''
        exec_times = 0 # 爬蟲執行次數(每次暫停後清為0)
        maximum_times = random.randint(2, 5) # 初始化 maximum_times
        is_within_first_list = True
        for tuple_obj in list(dict_obj.items())[index_1:]:
            excel_fn, address_list  = tuple_obj[0], tuple_obj[1]
            
            start_index_2 = None
            if is_within_first_list:
                is_within_first_list = False
                start_index_2 = index_2
            else:
                start_index_2 = 0
            
            for i in range(start_index_2, len(address_list)):
                print(f"正在為 ID: {counter} 記錄資料")
                address = address_list[i]
                try:
                    # 避免爬蟲流量過大被網站擋下，每爬2~5次隨機暫停一段時間
                    if exec_times == maximum_times:
                        # calculate that wait for how much time
                        wait_time = round(aver_stop_time * maximum_times, 2)
                        print(f"Wait {wait_time} seconds ...")
                        time.sleep(wait_time)
                        # reset
                        exec_times = 0
                        maximum_times = random.randint(2, 5)
                    else:
                        exec_times += 1
                    
                    #lat, lng = 123, 125 # test
                    lat, lng = get_coordinate(address)
                except:
                    print("Fail to obtain coordinate.")
                    print("Process stopped!")
                    #break
                    return csv_data_list
                
                # data of all fields are prepared!
                # store data to a list, and forward it to csv-file saving module
                csv_data_list.append( {"addressID": counter,
                                       "excel file name": excel_fn,
                                       "address": address,
                                       "lat": lat,
                                       "lng": lng} )
                counter += 1
        return csv_data_list
        
''' 
    module: get_num_list
    功能:   給定起始ID，求出: 
           (1)index_1: 從 第幾個串列 開始爬蟲 (return value: index, start from 0) 
           (2)index_2: 起始ID 對應到該 起始串列 的index (start from 0)
'''

def get_num_list(dict_obj):
    num_list = list()
    count = 0
    for one_list in dict_obj.values():
        length = len(one_list)
        num_list.append(length + count) # 累計串列元素個數
        count += length
    del count
    return num_list
    
def get_indeices_whereToExecute(ID, num_list): # ID => min: 1, max: data_amount 
    is_index_1_found = False
    #print(num_list)
    index_1 = 0
    for num in num_list:
        if num >= int(ID):
            is_index_1_found = True
            break
        else:
            index_1 += 1

    if not is_index_1_found:
        print("錯誤！未找到 index-1 所在串列")
        return None
    else:
        if index_1 == 0:
            index_2 = ID -1
        else:
            index_2 = ID -1 -num_list[index_1-1]
        print(f"index_1: {index_1}, index_2: {index_2}")
        return index_1, index_2

def save_to_csv(list_obj):
    print("\n準備儲存csv檔案")
    if not os.path.exists("./res"):
        os.mkdir("./res")
    filename = "address_data.csv"
    csv_path = "./res/" + filename
    ############################################
    record_amount = 0 # in case: csv file isn't exists
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding="utf-8-sig") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # 包含header列的總記錄筆數:
            record_amount = len([record for record in csv_reader])
    ############################################
    with open(csv_path, mode='a', newline="", encoding="utf-8-sig") as csv_file:
        cols = ["addressID", "excel file name", "address", "lat", "lng"]
        writer = csv.DictWriter(csv_file, fieldnames=cols)
        if record_amount == 0: # 該csv檔沒有header
            writer.writeheader()
        #----------------------------------
        ''' 解析中繼資料 '''
        for dict_obj in list_obj:
            writer.writerow(dict_obj)
    print("csv檔案儲存完畢！")
    
"""
###################################################################
Part 2:
    Integrate all func in Part 1 into more simple routine !!
    => [Process 1] 和 [Process 2] 可以單獨執行
    => (1) [Process 1] 是 "csv資料: ID、地址及經緯度 自動蒐集程式"
                (可以分段: 每次會讀取csv檔的現存資料筆數，從最末端開始自動新增資料，
                 直到所有資料蒐集完畢為止。(原始excel總資料量 = csv資料量))
    => (2) [Process 2] "畫圖程式"
             產生: 1.紅點分布圖 2.地理標籤圖, 3.區域統計地圖, 4.熱度圖
###################################################################
"""
# [Process 1]:  Automatically read excel files and obtain "addresses",
#               scraping "longitude and latitude" of them, 
#               and then generate a csv file for use of plotting graphs.

def auto_collect_csv_file_data():
    excel_files_path = "./raw_excel_data/"
    addresses_dict, data_amount = get_addresses_dict(excel_files_path)
    num_list = get_num_list(addresses_dict)
    #print(num_list)
    '''
    for tuple_obj in list(addresses_dict.items())[3:]:
        address_list = tuple_obj[1]
        print(address_list, end="\n"*3)
    '''
    #record_crawling_progress("1")
    
    csv_data_list = prepare_csv_data(addresses_dict, data_amount, num_list)
    if csv_data_list != None:
        save_to_csv(csv_data_list)

# [Process 2]:  Draw maps
def draw_maps(map_type):
    # 圖型繪製的中心區域經緯度
    lat = 25.035298
    lng = 121.5218117
    # 縮放比例
    zoom = 12
    plotter = MapPlottingAssistant(lat, lng, zoom)
    
    map_names = ["1.紅點分布圖", "2.地理標籤圖", "3.區域統計地圖", "4.熱度圖"]
    #plotter.read_csv_and_save_maps(map_names)
    #plotter.read_csv_and_save_maps_in_diff_years(map_names)
    plotter.read_csv_and_save_maps(map_names, map_type)

if __name__ == "__main__":
    """ 
    Process 1 / 「csv資料: ID、地址及經緯度 自動蒐集程式」 
    儲存位置: res/address_data.csv
    """
    auto_collect_csv_file_data()
    
    """ 
    Process 2 / 「畫圖程式」: "year_useless" or "year_related"
    儲存位置: res/..
    """
    
    '''   (1)執行以下 method，可產生「不分年度」的數張互動地圖 '''
    #draw_maps("year_useless")
    
    '''   (2)執行以下 method，可產生「依年度區分」的數張互動地圖，並分類儲存 '''
    #draw_maps("year_related")
    
    
