# 2020, 4/16, thurs, by Vivy (Queen)

# target function we play this time 
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException

# http requests
import os, sys, re, types, time, inspect, logging
import urllib, requests
from requests.exceptions import Timeout
from urllib.error import URLError, HTTPError
from io import StringIO

# to do ip addr formatter
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

#from retrying import retry
#from random import randint

# -------------------- Main Feature  called function-------------------------
# main func calling proxy_server, default speed is set up.
# recall below object called Browse_Agent
# use numpy to do ip addr format
def proxy_server(speed_limit=800):
    while True:
        default = Browse_Agent(url="", use_proxy=False)
        html = default.browser.execute_script('''function getElementByXpath(path) {
                                            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                        }
                                        return getElementByXpath("//table[@id='tblproxy']").outerHTML''')
        ori_df = pd.read_html(html, header=0, skiprows=[1,2], encoding='utf-8')
        df = ori_df[0]
        df['Response times'] = df['Response times'].apply(lambda x: pd.to_numeric(x.replace('ms','')))
        df = df[df['Response times']<speed_limit]

        if df.empty:
            continue

        df = df.sample(frac=1)
        print(df.to_dict())
        default=None

        for index, row in df.iterrows():
            proxy_server = '{}:{:.0f}'.format(row['Ip Address'], row['Port'])
            print("proxy server start on.")
            yield proxy_server

# Error Handlers for URL error, selenium, timeout
def retry_once_url_error(exception):
    if isinstance(exception, URLError) and not isinstance(exception, HTTPError):
        print("shall retry... due to url error.")
        return True
    else:
        return False

def retry_once_selenium_error(exception):
    return isinstance(exception, NoSuchElementException)

def retry_once_timeout(exception):
    return isinstance(exception, TimeoutException)

# -------------------- Main Object called Class -------------------------
# Browser
# User agent
# Proxy (not reverse one)
# func called as delete, get, post
# main instance is calling the proxy_server()
class Browse_Agent(object):
    
    def __init__(self, url, use_proxy=True):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.proxy_creator = proxy_server() if use_proxy else None

        # under case of using windows system and crome browser
        if 'win' in sys.platform:
            path = os.path.join(dir_path, "..", "Lib", "chromedriver.exe")
        else:
            os.chmod(os.path.join(dir_path, "..", "Lib", "chromedriver"), 0o777)
            path = os.path.join(dir_path, "..", "Lib", "chromedriver")

        print("Browser start on!")
        self.__browse(path, url)
        
    #@retry(retry_on_exception=retry_if_timeout, stop_max_attempt_number=5, stop_max_delay=100000, wait_random_min=5000, wait_random_max=10000)
    def __browse(self, path, url):
        options = webdriver.ChromeOptions()
        # crome options setup:
        # cert
        # gpu
        # sandbox
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        if isinstance(self.proxy_creator, types.GeneratorType):
            proxy = next(self.proxy_creator)
            logging.info('[Proxy] {}'.format(proxy))
            options.add_argument('--proxy-server={}'.format(proxy))
        print("get web page from target url now.")
        self.browser = webdriver.Chrome(executable_path=path, chrome_options=options)
        self.browser.get(url)
        self.browser.implicitly_wait(8)

    # freeze      
    def __del__(self):
        # logging.warn("Job completed, exit browser id={}.".format(id(self)))
        print("job completed, so gonna exist browser now.")
        if self.browser and isinstance(self.browser, webdriver.Chrome):
            self.browser.quit()

#-------------------------------------------------

# def string2ipAddr_converter(js_string):
#     try:
#         ip_string = re.match("^document.write\((.+)\);$", js_string).groups()[0]
#         ip_address = ip_string.replace('.substr(', '[').replace(')', ':]')
#         return eval(ip_address)
    
#     except Exception as e:
#         return np.nan

#-------------------------------------------------

# class Requests_Helper(object):
    
#     def __init__(self, use_proxy=True):
#         if use_proxy:
#             self.proxy_creator = proxy_server()
#             self.proxy_ip = next(self.proxy_creator)
#         else:
#             self.proxy_ip = None

#     #@retry(retry_on_exception=retry_if_url_error, stop_max_attempt_number=3, stop_max_delay=10000, wait_random_min=1000, wait_random_max=5000)
#     def get(self, url, params={}, encoding='utf-8', **kwargs):
#         try:
#             if self.proxy_ip:
#                 proxies = {'http': self.proxy_ip}
#                 response = requests.get(url=url, params=params, timeout=180, proxies=proxies, **kwargs)
#             else:
#                 response = requests.get(url=url, params=params, timeout=180, **kwargs)
                
#             if response.status_code == 200:
#                 buffer = response.content.decode(encoding)
#             else:
#                 print("status code is no 200.")
#                 raise requests.HTTPError("<{} {}>".format(response.status_code, response.reason))
#         except HTTPError as e:
#             frame = inspect.currentframe()
#             args, _, _, values = inspect.getargvalues(frame)
#             logging.error("[{0}] {1}".format(inspect.getframeinfo(frame)[2], e))
#             logging.debug(','.join(["{}={}".format(k, values[k]) for k in args]))
            
#             if self.proxy_ip:
#                 self.proxy_ip = next(self.proxy_creator)
#             raise HTTPError(e)
#         except Timeout as e:
#             print("request time out...")
#             return ""
#         except UnicodeDecodeError as e:
#             print("decodec error...")
#             return ""
#         else:
#             return StringIO(buffer)
        
#     #@retry(retry_on_exception=retry_if_url_error, stop_max_attempt_number=3, stop_max_delay=10000, wait_random_min=1000, wait_random_max=5000)
#     def post(self, url, data=None, encoding='utf-8', **kwargs):

#         try:
#             if self.proxy_ip:
#                 proxies = {'http': self.proxy_ip}
#                 response = requests.post(url=url, data=data, proxies=proxies, timeout=180, **kwargs)
#             else:
#                 response = requests.post(url=url, data=data, timeout=180, **kwargs)
                
#             if response.status_code == 200:
#                 buffer = response.content.decode(encoding)
#             else:
#                 print("status code is no 200.")
#                 raise requests.HTTPError("<{} {}>".format(response.status_code, response.reason))
#         except HTTPError as e:
#             frame = inspect.currentframe()
#             args, _, _, values = inspect.getargvalues(frame)
#             logging.error("[{0}] {1}".format(inspect.getframeinfo(frame)[2], e))
#             logging.debug(','.join(["{}={}".format(k, values[k]) for k in args]))
            
#             if self.proxy_ip:
#                 self.proxy_ip = next(self.proxy_creator)
#             raise HTTPError(e)

#         except Timeout as e:
#             print("req timeout...")
#             return ""
#         except UnicodeDecodeError as e:
#             print("decodec error.")
#             return ""
#         else:
#             return StringIO(buffer)
        
if __name__ == "__main__":
    proxy_instance_creator = proxy_server()
    for i in range(7):
        print(next(proxy_instance_creator))
