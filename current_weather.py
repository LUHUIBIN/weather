from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import data1_analysis

def getDriver(chrome_options=None):
    opt = webdriver.ChromeOptions()
    opt.add_argument("--disable-extensions")
    opt.add_argument("--disable-gpu")
    #options.add_argument("--no-sandbox") # linux only
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])
    opt.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver

def main():
    url = 'http://www.weather.com.cn/weather1d/101120601.shtml'
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # define headless
    driver = getDriver()
    driver.get(url)

    content = driver.page_source
    bs4 = BeautifulSoup(content, "html.parser")

    current_tem = bs4.find('div','tem')
    current_tem = current_tem.find('span').string
    data1_analysis.usart(current_tem)
    print(current_tem)

    current_win = bs4.find('div','zs w')
    win = current_win.find('span').string
    win_degree = current_win.find('em').string
    print(win)
    print(win_degree)
    data1_analysis.usart(win)
    data1_analysis.usart(win_degree)


if __name__ == '__main__':
    main()