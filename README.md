[文件資料夾]
    (1) raw_excel_data
        概述: 學生資訊excel檔
        檔案: (I)   1071＊＊ 107＊＊考生資料.xlsx
      	      (II)  ＊＊ 107＊＊聯招考生資料.xlsx
      	      (III) ＊＊ 108＊＊.xlsx
      	      (IV)  ＊＊ 108＊＊聯招考生資料.xlsx
      	      (V)   ＊＊ 109＊＊＊＊＊＊＊考生資料.xlsx
        說明: 原始資料，5份excel檔案。
        (為嚴防個資外洩，故檔案名稱稍做處理)

    (2) res
        概述: 中繼資訊
        檔案: address_data.csv
        說明: 存放根據原始文件中「通訊地址」爬取到的
             「經緯度」等中繼資訊，供熱度圖模取使用。

    (3) description docs
        概述: 說明文件
        檔案: (I)   地址轉經緯度_說明文件.txt

              (II)  利用經緯度繪製熱度圖及分布圖_說明文件.txt
        說明: 使用、程式功能 說明文件。
             「地址 => 經緯度」、
             「經緯度 => 繪製熱度圖」的詳細解說。

[程式碼]
    (1) HeatMapPainter.py: Python 主程式
        概述: 執行完整功能
        檔案: HeatMapPainter.py
        說明: 藉由 modules 資料夾中的模組，實現功能：
              讀取多份excel檔案 
              => 將地址轉經緯度 
              => 繪製熱度圖

    (2) modules: 程式模組
        概述: 讓主程式呼叫、取用功能。
        檔案: (I)   excel_reader.py
              (II)  gmap_crawler.py
              (III) map_plotting_class_version.py
        說明: (I)   excel_reader.py
                    此模組負責讀取csv檔案。
                    篩選出所有地址欄位，回傳給主程式。

              (II)  gmap_crawler.py
                    此模組負責爬蟲 Google Maps網頁。
                    利用(I)得到的所有地址，
                    自動填入、按Enter、抓出經緯度，並回傳。

              (III) map_plotting_class_version.py
                    此模組負責畫「熱度圖(Heat Map)」，同時
                    也會產生「紅點分布圖」、「地理標籤圖」、
                    「區域統計地圖」到「地理分布圖」資料夾。
                    利用(II)得到的所有經緯度資訊，
                    此模組負責繪製，並存成html檔案的熱度圖。
                    (和其它可視覺化、可互動式的地圖)