# ITsec_BypassSOP
旁繞同源，瓦解 WWW 唯一的集中管理。

SOP 目的是限制不相關來源介面之間的互動，例如不同 Domain Names 是無法相互存取資訊的，除非被駭客跨域的方式存取，那就另當別論了！

SOP 元件如果沒有即時更新，可能會有漏洞，需要修補，而駭客藉由 ByPass 旁繞技術，將 Hooked 的瀏覽器當成 HTTP 代理，存取不同的來源，那就是跨域和跨站的行為了！

是強制網路最重要的安全控制，可惜因為它也會遭遇被繞過或是打破，導致此一集中管理規範被瓦解。

實作旁繞技術，請詳 code。這些惡意代碼可能隱藏在 PDF Reader & Parser 這個 Plugin 或是 Adobe Flash 的 XML 檔案，藉以幫助駭客 Cross Domain，做出跨域行為，存取非同源的資訊。

https://github.com/QueenieCplusplus/ITsec_BypassSOP/blob/master/selenium.py (控制瀏覽器參數設定的套件，將其中沙盒改成 false)

https://github.com/QueenieCplusplus/ITsec_BypassSOP/blob/master/javaByPassSOP.java (jave code)

當然可能以 CORs 或是藉由瀏覽器來跨域，另外，也可能以雲端存儲裝置如 Google Drive 或是 DropBox 來跨域的。

# Code Base

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

# Google Drive (雲端存儲)範例

雲端裝置啟用本地端檔案到雲端的同步作業，讓這些雲端存儲軟體的使用者們的任何裝置都能存取它。

         file://var/mobile/Application/APP_UUID
         
攻擊屆有以上特權區域的檔案作為進入點。倘若使用者被駭客誘騙以其 APP 載入 HTML 檔，而檔案內藏著 JS 腳本，將這有惡意代碼的檔案 Load 至特權區的客觀事實允許了 JS 惡意腳本執行，藉此存取了行動裝置的本地端檔案系統。

也因為檔案系統已經遭到入侵，所以也沒有任何安全機制可以防止此惡意代碼從中開始發展，存取另一檔案，節外生枝。

# IE (瀏覽器)範例

瀏覽器也是軟體，可能存在些許漏洞，倘若使用者沒有即時版本更新，可能也會遭逢駭客利用旁繞技術，藉由瀏覽器當作 HTTP 代理，實行跨域存取技術。

           var document;
           document = {};
           document.domain = ''; // 寫入網域名稱
           alert(document.domain); // 惡意代碼能執行於瀏覽器舊版本，打開 SOP，實行跨域存取

# Phising, 社交釣魚的範例

透過 file 方案 load 頁面（非 http ），並從 domain name 這伺服器請求某 html 檔案後，XHR 這物件就能讀取回應。

    <html>
    <body>
    <script>
        
        xhr = new XMLHttpRequest();
        
        xhr.open("GET", "http://domainName.com/pocs/different_origin.html");
        
        xhr.send();
       
    </script>
    </body>
    </html>

# CORs, 跨域資源共享的範例

跨域資源共享能鬆開 SOP 的限制，所以使用者在設定上，要多加注意喔～ 如下設定為通用字元 * ，就是無異於允許網路上其他網站提交『跨域請求』至該站點，從中讀取回應，返回至駭客主控台。

總之，這一切災難都是由允許不同源頭的 Hook Browser 開始的！只要使用者強制執行 SOP 政策，便可遠離之後所述的很多駭客行為產生的各種不從人願的後果。

      Access-Control-Allow-Origin: *





