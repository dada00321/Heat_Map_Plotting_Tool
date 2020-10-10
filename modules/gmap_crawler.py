import time
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys

# lat: 緯度 log: 經度
def get_coordinate(addr):
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument("headless")
    wd_path = "D:/geckodriver/chromedriver.exe"
    driver = wd.Chrome(executable_path=wd_path, options=chrome_options)
    url = "https://www.google.com.tw/maps"
    driver.get(url)
    
    # locate the search box
    tmp = driver.find_elements_by_xpath("//input[@id='searchboxinput']")
    search_box = tmp[0]
    
    search_box.send_keys(addr)
    search_box.send_keys(Keys.ENTER)
    
    ''' 經實測，等待約3秒後，google map網址會自動加上經緯度 
    => 可爬出此URL並剖析出該地點的經緯度 '''
    #print("等待3秒")
    time.sleep(5)
    #print(driver.current_url)
    url = driver.current_url
    lat, log = url.split("@")[-1].split("/")[0].split(",")[:2]
    driver.quit()
    #print("成功取得經緯度!")
    
    return lat, log

if __name__ == "__main__":
    pass
    # 測試:
    '''
    # 基隆廟口夜市
    lat, log = get_coordinate("基隆市仁愛區愛四路20號")
    print(f"{lat}, {log}")
    
    # 天瓏書局
    lat, log = get_coordinate("台北市中正區重慶南路一段105號")
    print(f"{lat}, {log}")
    
    # 故宮郵局
    lat, log = get_coordinate("台北市士林區至善路二段221號")
    print(f"{lat}, {log}")
    '''
