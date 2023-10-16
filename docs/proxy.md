4.8 cookie：填写平台账号cookie（选填）

4.9 proxytype：填写代理类型，如：HTTP\HTTPS\SSH\Socks5\Luminati（必填）

4.10 ipchecker：填写IP查询渠道，如：IP2Location，不填则使用全局设置的IP查询渠道预设值（选填）

4.11 proxy：填写由供应商提供的代理信息，格式为：代理主机:代理端口:代理账号:代理密码（注：为英文分号）（必填）

4.12 proxyurl：可填写移动代理的刷新URL。该URL仅用于移动代理。（选填）

4.13 proxyid：填写代理管理中的代理ID（选填）

4.14 ip：填写匹配动态代理地区的IP（选填）

4.15 countrycode：填写动态代理的国家/地区（选填）

4.16 regioncode：填写动态代理的州/省（选填）

4.17 citycode：填写动态代理的城市（选填）



原生IP：是指能看到DNS和IP地址是一个国家的，基本可以认为是原生的，但也有特殊情况就是，如东南亚、欧洲一些国家，DNS会被解析到附近国家。像我使用的IPFoxy家的代理IP，ISP代理测下来基本是纯原生的，在业务层面基本上用起来没有遇到过问题。

双ISP：常提及的双ISP就是指里面查询到的Asn和Company的type属性。有的所谓住宅IP其中的ASN是属于运营商的所以是ISP，但是company不是，这种就是单ISP，而真正的住宅IP无论是ASN还是运营的公司都应该是当地的运营商，像我检测的IPFoxy的这条IP就是双ISP，理论上这样的IP更加稳定。


ASN：自治系统，实现IP到ASN的映射和ASN查找；
company：拥有这个ip的公司或组织，通常分为ISP、企业或托管；
private：检测用于掩盖用户真实IP地址的各种方法；
vpn：虚拟网络；proxy：代理；tor：Tor（一种代理类型）；relay：中继使用；service：服务



ref

https://github.com/berstend/puppeteer-extra/issues/254

https://help.adspower.net/docs/pdB11b


https://zhuanlan.zhihu.com/p/657546441



https://whoer.net/blog/how-to-hide-your-dns/


https://github.com/berstend/puppeteer-extra/issues/454



1. access bot detection companies url

know the details


2. access their client website to know yes or no

PerimeterX: https://www.usa-people-search.com/names/a_1_150_0

https://www.westernunion.com/us/en/web/send-money/start?ReceiveCountry=MX&SendAmount=100
@berstend These sites (well, most of them) are clients of bot detection companies. If you visit them with, say, window.callPhantom exposed, you will get redirected to a page that will make you do a captcha.
