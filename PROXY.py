from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pyautogui
from random import choice
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import zipfile
from fake_useragent import UserAgent

def proxies(username, password, endpoint, port):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxies",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (endpoint, port, username, password)

    extension = 'proxy_extension.zip'

    with zipfile.ZipFile(extension, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return extension

proxy_list = [
    {"host":"181.41.197.13",'port':'59100','username':'************','password':'***************','failed':0},
              {"host":"181.215.11.193",'port':'59100','username':'************','password':'***************','failed':0},
              {"host":"185.187.233.239",'port':'59100','username':'************','password':'***************','failed':0},
              {"host":"173.249.166.226",'port':'59100','username':'************','password':'***************','failed':0},
              {"host":"141.11.140.183",'port':'59100','username':'************','password':'***************','failed':0},
              {"host":"45.156.118.242",'port':'59100','username':'************','password':'***************','failed':0},
              ]
def create_new_chrome_browser(use_proxy=True):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    ua = UserAgent(os='windows',min_percentage=.5)
    user_agent = ua.getChrome
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    prefs = {"credentials_enable_service": False,
        "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)    
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-agent={user_agent}")
    if use_proxy:
        
        if len(proxy_list) > 0:
            proxy_selected = choice(proxy_list)
            proxies(proxy_selected['username'], proxy_selected['password'], proxy_selected['host'], proxy_selected['port'])
            options.add_extension('proxy_extension.zip')
            print(proxy_selected,'proxy ok')
        
    else:
        proxy_selected = []
        pass
    # options.add_argument('--load-extension=proxy_extension.zip')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    while True:
        try:
            driver.get('http://checkip.amazonaws.com//')
            ip = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body")
                )
            )
            print(ip.text)
            proxy_list
            break
        except:
            if len(proxy_list) > 0:
                proxy_selected['failed'] += 1
                if proxy_selected['failed'] > 3:
                    proxy_list.remove(proxy_selected)
                    print('proxy ok',proxy_selected)
    return driver
