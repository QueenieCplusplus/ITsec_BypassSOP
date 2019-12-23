# ITsec_BypassSOP
旁繞同源，瓦解 WWW 唯一的集中管理。

SOP 目的是限制不相關來源介面之間的互動，例如不同 Domain Names 是無法相互存取資訊的，除非被駭客跨域的方式存取，那就另當別論了！

SOP 元件如果沒有即時更新，可能會有漏洞，需要修補，而駭客藉由 ByPass 旁繞技術，將 Hooked 的瀏覽器當成 HTTP 代理，存取不同的來源，那就是跨域和跨站的行為了！

是強制網路最重要的安全控制，可惜因為它也會遭遇被繞過或是打破，導致此一集中管理規範被瓦解。

實作旁繞技術，請詳 code。

