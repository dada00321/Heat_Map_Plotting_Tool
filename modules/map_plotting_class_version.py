# Author: Dada Liu (劉永琦)
import folium
import pandas as pd
from folium import plugins
from folium.plugins import HeatMap
import os

class MapPlottingAssistant():
    # mathod: 讀csv檔 => 畫圖 => 存圖(.html)
    # 整合成一個方法，方便主程式呼叫 
    
    def exec_getMap_byIndex(self, index, input_data):
        if index == 0:
            curr_map = self.getMap(input_data) # 紅點分布圖
        elif index == 1:
            curr_map = self.getMap_with_marker_and_popText(input_data) # 地理標籤圖
        elif index == 2:
            curr_map = self.getMap_with_statistic_area(input_data) # 區域統計地圖
        else:
            curr_map = self.getMap_HeapMap(input_data) # 熱度圖
        return curr_map
        
    def read_csv_and_save_maps(self, map_names, map_type):
        path = "./res/address_data.csv"
        self.read_csv_data(path)
        
        map_types = ["year_useless", "year_related"]
        
        if map_type == map_types[1]:
            # year_records: 年度資料
            years, year_records = self.split_data()
        
        for idx, map_name in enumerate(map_names):
            if map_type == map_types[0]:
                curr_map = self.exec_getMap_byIndex(idx, input_data=self.data)
                self.save_map(curr_map, map_name)
            elif map_type == map_types[1]:
                for i in range(len(years)):
                    year = years[i]
                    year_record = year_records[i]
                    curr_map = self.exec_getMap_byIndex(idx, input_data=year_record)
                    self.save_map(curr_map, map_name, save_type=2, year=year)
    
    ''' ***此方法可產生"不分年度"的數張互動地圖 '''
    def read_csv_and_save_maps_allInOne(self, map_names): # 4 maps: need 4 names
        path = "./res/address_data.csv"
        self.read_csv_data(path)
        for idx, map_name in enumerate(map_names):
            if idx == 0:
                curr_map = self.getMap(self.data) # 紅點分布圖
            elif idx == 1:
                curr_map = self.getMap_with_marker_and_popText(self.data) # 地理標籤圖
            elif idx == 2:
                curr_map = self.getMap_with_statistic_area(self.data) # 區域統計地圖
            else:
                curr_map = self.getMap_HeapMap(self.data) # 熱度圖
            self.save_map(curr_map, map_name)
    
    ''' ***此方法可產生"依年度區分"的數張互動地圖，並分類儲存 '''
    def read_csv_and_save_maps_inDiffYears(self, map_names):
        path = "./res/address_data.csv"
        self.read_csv_data(path)
        
        # year_records: 年度資料
        years, year_records = self.split_data()
        
        for idx, map_name in enumerate(map_names):
            for i in range(len(years)):
                year = years[i]
                year_record = year_records[i]
                if idx == 0:
                    curr_map = self.getMap(year_record)
                elif idx == 1:
                    curr_map = self.getMap_with_marker_and_popText(year_record)
                elif idx == 2:
                    curr_map = self.getMap_with_statistic_area(year_record)
                else:
                    curr_map = self.getMap_HeapMap(year_record)
                self.save_map(curr_map, map_name, save_type=2, year=year)
    
    ###############################################
    '''
    lat: 緯度 (e.g. North latitude/北緯)
    lng: 經度 (e.g. West longitude/西經)
    --------------------------------------
    zoom_start: 縮放比例(12~16, 數字越大，比例越大)
    '''
    def __init__(self, lat, lng, zoom):
        self.latitude = lat
        self.longitude = lng
        self.zoom_size = zoom
        
    def read_csv_data(self, path):
        self.data = pd.read_csv(path)
        #self.data = self.data.iloc[0:limit, :] # limit: 限制資料筆數
        
    def split_data(self):
        start_yy = 107; end_yy = 109 # 資料"最早年度"和"最晚年度"
        years = [str(year) for year in range(start_yy, end_yy+1)]
        year_records = list()
        for year in years:
            # df: 依年度過濾出當年的資料
            df = self.data[self.data["excel file name"].str.contains(year)]
            year_records.append(df)
        return years, year_records
    #-----------------------------------------
    def get_clean_map(self):
        map_ = folium.Map(location=[self.latitude, self.longitude], zoom_start=self.zoom_size)
        # 黑白mode:
        #map_ = folium.Map(location=[self.latitude, self.longitude], zoom_start=self.zoom_size, tiles='Stamen Toner')
        return map_
        
    def save_map(self, map_, map_name, save_type=1, year=None):
        # 建立資料夾
        if not os.path.exists("./res"):
            os.mkdir("./res")
        if save_type == 1:
            dir_name = "地理分布圖"
        elif save_type == 2:
            dir_name = "可呈現不同年度變化的地理分布圖"
        if not os.path.exists(f"./res/{dir_name}"):
            os.mkdir(f"./res/{dir_name}")
        #----------------------------------------------
        if save_type == 1:   # 直接儲存(依照 map_name 存圖)
            path = f"./res/{dir_name}/{map_name}.html"
        elif save_type == 2: # 分類儲存(依照 map_name 建資料夾，再分類存圖)
            if not os.path.exists(f"./res/{dir_name}/{map_name}"):
                os.mkdir(f"./res/{dir_name}/{map_name}")
            path = f"./res/{dir_name}/{map_name}/{year}.html"
        map_.save(path)
        
    def getMap(self, input_data): # 紅點分布圖
        new_map = self.get_clean_map()
        features = folium.map.FeatureGroup()
        for lat, lng in zip(input_data.lat, input_data.lng):
            features.add_child(
                folium.CircleMarker(
                    [lat, lng],
                    radius=7, # define how big latou want the circle markers to be
                    color='latellow',
                    fill=True,
                    fill_color='red',
                    fill_opacitlat=0.4
                )
            )
        new_map.add_child(features)
        return new_map
    
    def getMap_with_marker_and_popText(self, input_data): # 地理標籤圖
        map_ = self.get_clean_map()
        # add pop-up telngt to each marker on the map
        latitudes = list(input_data.lat)
        longitudes = list(input_data.lng)
        labels = list(input_data.address)
        for lat, lng, label in zip(latitudes, longitudes, labels):
            folium.Marker([lat, lng], popup=label).add_to(map_)
        return map_
    
    def getMap_with_statistic_area(self, input_data): # 區域統計地圖
        new_map = self.get_clean_map()
        features = plugins.MarkerCluster().add_to(new_map)
        
        for lat, lng, label, in zip(input_data.lat, input_data.lng, input_data.address):
            folium.Marker(
                location=[lat, lng],
                icon=None,
                popup=label,
            ).add_to(features)
        new_map.add_child(features)
        return new_map
    
    def getMap_HeapMap(self, input_data): # 熱度圖(heat map)
        new_map = self.get_clean_map()
        
        # Convert data format
        '''
        e.g.
        [ [37.748520075538, -122.42024729644899],
          [37.748520075538, -122.42024729644899], 
          [37.7762384154187, -122.464940040095] ]
        '''
        heatdata = input_data[['lat','lng']].values.tolist()
        #print("heatdata:\n", heatdata)
        
        # add incidents to map
        HeatMap(heatdata).add_to(new_map)
        return new_map
        
if __name__ == "__main__":
    #pass
    lat = 25.035298; lng = 121.5218117  # 圖型繪製的中心區域經緯度
    zoom = 12 # 縮放比例 
    painter = MapPlottingAssistant(lat, lng, zoom)
    
    path = "../res/address_data.csv"
    painter.read_csv_data(path)
    
    # 測試:
    ''' 
    lat = 25.035298; lng = 121.5218117  # 圖型繪製的中心區域經緯度
    zoom = 12 # 縮放比例 
    painter = MapPlottingAssistant(lat, lng, zoom)
    
    path = "../res/address_data.csv"
    painter.read_csv_data(path)
    input_data = painter.data
    #------------------------------
    map_1 = painter.getMap(input_data)
    painter.save_map(map_1, "map_1.html")
    
    map_2 = painter.getMap_with_marker_and_popText(input_data)
    painter.save_map(map_2, "map_2.html")
    
    map_3 = painter.getMap_with_statistic_area(input_data)
    painter.save_map(map_3, "map_3.html")
    
    map_4 = painter.getMap_HeapMap(input_data)
    painter.save_map(map_4, "map_4.html")
    '''
    