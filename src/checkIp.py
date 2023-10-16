#Whoer#

import requests
import socks
import socket

# Set the SOCKS proxy settings
proxy_host = 'your_proxy_host'
proxy_port = 'your_proxy_port'
proxy_type = socks.PROXY_TYPE_SOCKS5  # Adjust as needed
ipoptions = [
            "https://browserleaks.com/ip",
            "https://ipapi.co",
            "https://jsonip.com",
            "http://ifconfig.me/ip",
            "http://ip111.cn/",
        ]
ipfullinfooptions = [
            "https://ipapi.co/json/",
            "https://db-ip.com/23.80.5.90",
            "http://ip-api.com/json/",
        ]
ipchecklist = [
            "https://niespodd.github.io/browser-fingerprinting/",
            "https://bgp.he.net/",
            "https://browserleaks.com/",
            "https://ip.voidsec.com/",
            "https://ipinfo.io/",
            "https://ipleak.com/",
            "https://ipleak.net/",
            "https://ipleak.org/",
            "https://ipx.ac/run",
            "https://nstool.netease.com/",
            "https://test-ipv6.com/",
            "https://whatismyipaddress.com/blacklist-check",
            "https://whoer.net/",
            "https://www.astrill.com/dns-leak-test",
            "https://www.astrill.com/ipv6-leak-test",
            "https://www.astrill.com/port-scan",
            "https://www.astrill.com/vpn-leak-test",
            "https://www.astrill.com/what-is-my-ip",
            "https://www.deviceinfo.me/",
            "https://www.dnsleaktest.com/",
            "https://www.doileak.com/",
            "https://www.expressvpn.com/webrtc-leak-test",
            "https://bot.incolumitas.com/proxy_detect.html",
            "https://corretor.portoseguro.com.br/corretoronline/",
            "https://ipapi.co/json/",
            "https://jsonip.com/",
            "https://ipinfo.io/json",
            "https://jsonip.com/",
            "https://api64.ipify.org/",
        ]

dns_indicators = [
                "checkip.dyndns.com",
                "checkip.dyndns.org",
                "whatismyip.org",
                "whatsmyipaddress.com",
                "getmyip.org",
                "get-myip.com",
                "getmyip.co.uk",
                "icanhazip.com",
                "whatismyipaddress.com",
                "bot.whatismyipaddress.com",
                "myipaddress.com",
                "ip-addr.es",
                "api.ipify.org",
                "ipinfo.info",
                "myexternalip.com",
                "curlmyip.com",
                "ip4.telize.com",
                "ip.xss.ru",
                "ipinfo.io",
                "myip.ru",
                "myip.com.ua",
                "myip.com.br",
                "showmyip.gr",
                "trackip.net",
                "showmemyip.com",
                "wtfismyip.com",
                "checkmyip.com",
                "myexternalip.com",
                "ipchicken.com",
                "whatismypublicip.com",
                "ip-detect.net",
                "ip-whois.net",
                "www.ip.cn",
                "ip2location.com",
                "showip.net",
                "cmyip.com",
                "iplocation.net",
                "ip-tracker.org",
                "ip.samuraj-cz.com",
                "ipleak.net",
                "myip.dnsomatic.com",
                "whoer.net",
                "ip.42.pl",

                # public stun server list, from http://olegh.ftp.sh/public-stun.txt (could make this a feed I suppose)
                # all servers not matching our generic stun[0-9]?.* pattern below
                "iphone-stun.strato-iphone.de",
                "numb.viagenie.ca",
                "s1.taraba.net",
                "s2.taraba.net",
                "stunserver.org",
            ]
language_dict = {
            "AF": ["pr-AF", "pr"],
            "AX": ["sw-AX", "sw"],
            "AL": ["sq-AL", "sq"],
            "DZ": ["ar-DZ", "ar"],
            "AS": ["en-AS", "en"],
            "AD": ["ca-AD", "ca"],
            "AO": ["po-AO", "po"],
            "AI": ["en-AI", "en"],
            "AG": ["en-AG", "en"],
            "AR": ["gr-AR", "gr"],
            "AM": ["hy-AM", "hy"],
            "AW": ["nl-AW", "nl"],
            "AU": ["en-AU", "en"],
            "AT": ["ba-AT", "ba"],
            "AZ": ["az-AZ", "az"],
            "BS": ["en-BS", "en"],
            "BH": ["ar-BH", "ar"],
            "BD": ["be-BD", "be"],
            "BB": ["en-BB", "en"],
            "BY": ["be-BY", "be"],
            "BE": ["de-BE", "de"],
            "BQ": ["en-BQ", "en"],
            "BZ": ["bj-BZ", "bj"],
            "BJ": ["fr-BJ", "fr"],
            "BM": ["en-BM", "en"],
            "BT": ["dz-BT", "dz"],
            "BO": ["ay-BO", "ay"],
            "BA": ["bo-BA", "bo"],
            "BW": ["en-BW", "en"],
            "BV": ["no-BV", "no"],
            "BR": ["po-BR", "po"],
            "IO": ["en-IO", "en"],
            "BN": ["ms-BN", "ms"],
            "BG": ["bu-BG", "bu"],
            "BF": ["fr-BF", "fr"],
            "BI": ["fr-BI", "fr"],
            "KH": ["kh-KH", "kh"],
            "CM": ["en-CM", "en"],
            "CA": ["en-CA", "en"],
            "CV": ["po-CV", "po"],
            "KY": ["en-KY", "en"],
            "CF": ["fr-CF", "fr"],
            "TD": ["ar-TD", "ar"],
            "CL": ["sp-CL", "sp"],
            "CN": ["zh-CN", "zh"],
            "CX": ["en-CX", "en"],
            "CC": ["en-CC", "en"],
            "CO": ["sp-CO", "sp"],
            "KM": ["ar-KM", "ar"],
            "CG": ["fr-CG", "fr"],
            "CD": ["fr-CD", "fr"],
            "CK": ["en-CK", "en"],
            "CR": ["sp-CR", "sp"],
            "CI": ["fr-CI", "fr"],
            "HR": ["hr-HR", "hr"],
            "CU": ["sp-CU", "sp"],
            "CW": ["en-CW", "en"],
            "CY": ["el-CY", "el"],
            "CZ": ["ce-CZ", "ce"],
            "DK": ["da-DK", "da"],
            "DJ": ["ar-DJ", "ar"],
            "DM": ["en-DM", "en"],
            "DO": ["sp-DO", "sp"],
            "EC": ["sp-EC", "sp"],
            "EG": ["ar-EG", "ar"],
            "SV": ["sp-SV", "sp"],
            "GQ": ["fr-GQ", "fr"],
            "ER": ["ar-ER", "ar"],
            "EE": ["es-EE", "es"],
            "ET": ["am-ET", "am"],
            "FK": ["en-FK", "en"],
            "FO": ["da-FO", "da"],
            "FJ": ["en-FJ", "en"],
            "FI": ["fi-FI", "fi"],
            "FR": ["fr-FR", "fr"],
            "GF": ["fr-GF", "fr"],
            "PF": ["fr-PF", "fr"],
            "TF": ["fr-TF", "fr"],
            "GA": ["fr-GA", "fr"],
            "GM": ["en-GM", "en"],
            "GE": ["ka-GE", "ka"],
            "DE": ["de-DE", "de"],
            "GH": ["en-GH", "en"],
            "GI": ["en-GI", "en"],
            "GR": ["el-GR", "el"],
            "GL": ["ka-GL", "ka"],
            "GD": ["en-GD", "en"],
            "GP": ["fr-GP", "fr"],
            "GU": ["ch-GU", "ch"],
            "GT": ["sp-GT", "sp"],
            "GG": ["en-GG", "en"],
            "GN": ["fr-GN", "fr"],
            "GW": ["po-GW", "po"],
            "GY": ["en-GY", "en"],
            "HT": ["fr-HT", "fr"],
            "HM": ["en-HM", "en"],
            "VA": ["it-VA", "it"],
            "HN": ["sp-HN", "sp"],
            "HK": ["en-HK", "en"],
            "HU": ["hu-HU", "hu"],
            "IS": ["is-IS", "is"],
            "IN": ["en-IN", "en"],
            "ID": ["in-ID", "in"],
            "IR": ["fa-IR", "fa"],
            "IQ": ["ar-IQ", "ar"],
            "IE": ["en-IE", "en"],
            "IM": ["en-IM", "en"],
            "IL": ["ar-IL", "ar"],
            "IT": ["it-IT", "it"],
            "JM": ["en-JM", "en"],
            "JP": ["jp-JP", "jp"],
            "JE": ["en-JE", "en"],
            "JO": ["ar-JO", "ar"],
            "KZ": ["ka-KZ", "ka"],
            "KE": ["en-KE", "en"],
            "KI": ["en-KI", "en"],
            "KP": ["ko-KP", "ko"],
            "KR": ["ko-KR", "ko"],
            "KW": ["ar-KW", "ar"],
            "KG": ["ki-KG", "ki"],
            "LA": ["la-LA", "la"],
            "LV": ["la-LV", "la"],
            "LB": ["ar-LB", "ar"],
            "LS": ["en-LS", "en"],
            "LR": ["en-LR", "en"],
            "LY": ["ar-LY", "ar"],
            "LI": ["de-LI", "de"],
            "LT": ["li-LT", "li"],
            "LU": ["de-LU", "de"],
            "MO": ["po-MO", "po"],
            "MK": ["mk-MK", "mk"],
            "MG": ["fr-MG", "fr"],
            "MW": ["en-MW", "en"],
            "MY": ["en-MY", "en"],
            "MV": ["di-MV", "di"],
            "ML": ["fr-ML", "fr"],
            "MT": ["en-MT", "en"],
            "MH": ["en-MH", "en"],
            "MQ": ["fr-MQ", "fr"],
            "MR": ["ar-MR", "ar"],
            "MU": ["en-MU", "en"],
            "YT": ["fr-YT", "fr"],
            "MX": ["sp-MX", "sp"],
            "FM": ["en-FM", "en"],
            "MD": ["ro-MD", "ro"],
            "MC": ["fr-MC", "fr"],
            "MN": ["mo-MN", "mo"],
            "MS": ["en-MS", "en"],
            "MA": ["ar-MA", "ar"],
            "MZ": ["po-MZ", "po"],
            "MM": ["my-MM", "my"],
            "NA": ["af-NA", "af"],
            "NR": ["en-NR", "en"],
            "NP": ["ne-NP", "ne"],
            "NL": ["nl-NL", "nl"],
            "NC": ["fr-NC", "fr"],
            "NZ": ["en-NZ", "en"],
            "NI": ["sp-NI", "sp"],
            "NE": ["fr-NE", "fr"],
            "NG": ["en-NG", "en"],
            "NU": ["en-NU", "en"],
            "NF": ["en-NF", "en"],
            "MP": ["ca-MP", "ca"],
            "NO": ["nn-NO", "nn"],
            "OM": ["ar-OM", "ar"],
            "PK": ["en-PK", "en"],
            "PW": ["en-PW", "en"],
            "PS": ["ar-PS", "ar"],
            "PA": ["sp-PA", "sp"],
            "PG": ["en-PG", "en"],
            "PY": ["gr-PY", "gr"],
            "PE": ["ay-PE", "ay"],
            "PH": ["en-PH", "en"],
            "PN": ["en-PN", "en"],
            "PL": ["po-PL", "po"],
            "PT": ["po-PT", "po"],
            "PR": ["en-PR", "en"],
            "QA": ["ar-QA", "ar"],
            "RE": ["fr-RE", "fr"],
            "RO": ["ro-RO", "ro"],
            "RU": ["ru-RU", "ru"],
            "RW": ["en-RW", "en"],
            "SH": ["en-SH", "en"],
            "KN": ["en-KN", "en"],
            "LC": ["en-LC", "en"],
            "PM": ["fr-PM", "fr"],
            "VC": ["en-VC", "en"],
            "WS": ["en-WS", "en"],
            "SM": ["it-SM", "it"],
            "ST": ["po-ST", "po"],
            "SA": ["ar-SA", "ar"],
            "SN": ["fr-SN", "fr"],
            "SC": ["cr-SC", "cr"],
            "SL": ["en-SL", "en"],
            "SG": ["zh-SG", "zh"],
            "SK": ["sl-SK", "sl"],
            "SI": ["sl-SI", "sl"],
            "SB": ["en-SB", "en"],
            "SO": ["ar-SO", "ar"],
            "SS": ["en-SS", "en"],
            "SX": ["en-SX", "en"],
            "ZA": ["af-ZA", "af"],
            "GS": ["en-GS", "en"],
            "ES": ["sp-ES", "sp"],
            "LK": ["si-LK", "si"],
            "SD": ["ar-SD", "ar"],
            "SR": ["nl-SR", "nl"],
            "SJ": ["no-SJ", "no"],
            "SZ": ["en-SZ", "en"],
            "SE": ["sw-SE", "sw"],
            "CH": ["fr-CH", "fr"],
            "SY": ["ar-SY", "ar"],
            "TW": ["zh-TW", "zh"],
            "TJ": ["ru-TJ", "ru"],
            "TZ": ["en-TZ", "en"],
            "TH": ["th-TH", "th"],
            "TL": ["po-TL", "po"],
            "TG": ["fr-TG", "fr"],
            "TK": ["en-TK", "en"],
            "TO": ["en-TO", "en"],
            "TT": ["en-TT", "en"],
            "TN": ["ar-TN", "ar"],
            "TR": ["tu-TR", "tu"],
            "TM": ["ru-TM", "ru"],
            "TC": ["en-TC", "en"],
            "TV": ["en-TV", "en"],
            "UG": ["en-UG", "en"],
            "UA": ["uk-UA", "uk"],
            "AE": ["ar-AE", "ar"],
            "GB": ["en-GB", "en"],
            "US": ["en-US", "en"],
            "UM": ["en-UM", "en"],
            "UY": ["sp-UY", "sp"],
            "UZ": ["ru-UZ", "ru"],
            "VU": ["bi-VU", "bi"],
            "VE": ["sp-VE", "sp"],
            "VN": ["vi-VN", "vi"],
            "VG": ["en-VG", "en"],
            "VI": ["en-VI", "en"],
            "WF": ["fr-WF", "fr"],
            "EH": ["be-EH", "be"],
            "YE": ["ar-YE", "ar"],
            "ZM": ["en-ZM", "en"],
            "ZW": ["bw-ZW", "bw"],
            "RS": ["sr-RS", "sr"],
            "ME": ["cn-ME", "cn"],
            "XK": ["sq-XK", "sq"],
        }
class CheckIP:
    """
    Args:
        proxy: username:password@ip:port / ip:port
    Returns:
        {
            "server": "ip:port"
            "username": username,
            "password": password,
        }
        server: http://ip:port or socks5://ip:port. Short form ip:port is considered an HTTP proxy.
    """

    def __init__(self, proxy_string=None,http_proxy=None,https_proxy=None):
        self.proxy_string = proxy_string.strip() if proxy_string else None
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy

        self.ip = None
        self.port = None
        self.username = None
        self.password = None
        if self.http_proxy  and self.https_proxy:
            self.httpx_proxy = (
                {"http": self.http_proxy, "https": self.http_proxy}
            )
        else:
            if self.proxy_string:
                if "socks5" in self.proxy_string:
                    # context_proxy = ProxySettings(server=self.proxy_string)
                    self.http_proxy = self.proxy_string
                    self.httpx_proxy = {"http": self.http_proxy, "https": self.http_proxy}
                else:
                    self.split_proxy()
                    self.proxy_string = (
                        f"{self.username}:{self.password}@{self.ip}:{self.port}"
                        if self.username
                        else f"{self.ip}:{self.port}"
                    )
                    self.http_proxy = f"http://{self.proxy_string}"
                    self.httpx_proxy = (
                        {"http": self.http_proxy, "https": self.http_proxy}
                        if self.proxy_string
                        else None
                    )
            else:
                print('you should either provider proxy_string or pair of protocol,http_proxy,https_proxy')
        # self.check, self.reason = self.check_proxy()
    # Shit Method To Get Locale of Country code
    async def locale_sync(self, country_code="US"):
        url = f"https://restcountries.com/v3.1/alpha/{country_code}"
        r = requests.get(url)
        data = r.json()[0]
        self.languages = data.get("languages")
        self.language_code = list(self.languages.keys())[0][:2]
        self.locale = f"{self.language_code.lower()}-{country_code.upper()}"

    async def locale(self, country_code="US") -> None:

        # country_code = self.proxy_string.country_code
        country_code = country_code

        if country_code in language_dict:
            self.locale, self.language_code = language_dict[country_code]
        else:
            raise ValueError("Proxy Country not supported")

    def split_helper(self, splitted):
        if not any([_.isdigit() for _ in splitted]):
            raise GeneratorExit("No ProxyPort could be detected")
        if splitted[1].isdigit():
            self.ip, self.port, self.username, self.password = splitted
        elif splitted[3].isdigit():
            self.username, self.password, self.ip, self.port = splitted
        else:
            if "socks5" in self.proxy_string:
                # context_proxy = ProxySettings(server=self.proxy_string)
                print(self.proxy_string)
            else:
                raise GeneratorExit(f"Proxy Format ({self.proxy_string}) isnt supported")

    def split_proxy(self):
        splitted = self.proxy_string.split(":")
        if len(splitted) == 2:
            self.ip, self.port = splitted
        elif len(splitted) == 3:
            if "@" in self.proxy_string:
                helper = [_.split(":") for _ in self.proxy_string.split("@")]
                splitted = [x for y in helper for x in y]
                self.split_helper(splitted)
            # else:
            #     if "socks5" in self.proxy_string:
            #         context_proxy = ProxySettings(server=self.proxy_string)
            #     else:
            #         raise GeneratorExit(f"Proxy Format ({self.proxy_string}) isnt supported")
        elif len(splitted) == 4:
            self.split_helper(splitted)
        # else:
        #     if "socks5" in self.proxy_string:
        #         context_proxy = ProxySettings(server=self.proxy_string)
        #     else:
        #         raise GeneratorExit(f"Proxy Format ({self.proxy_string}) isnt supported")

    def getip_ifconfig(self):
        url = "http://ifconfig.me/ip"
        print("1")
        try:
            response = requests.get(url)
            print("ip: {}".format(response.text.strip()))

            response = requests.get(url, proxies=self.httpx_proxy)
            print("tor ip: {}".format(response.text.strip()))
            ip = response.text.strip()
            return ip
        except:
            print(f"can not access: {url}")

            return None

    def check_ip_ip111(self):
        url = "http://ip111.cn/"
        print("1")
        try:
            ip_request = requests.get(url, proxies=self.httpx_proxy)
            local_ip = (
                re.search(
                    r"<p>\s*(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b.*?)</p>",
                    ip_request.text,
                )
                .group(1)
                .split(" ")[0]
            )
            # your local ip is: 124.89.116.178 中国 西安
            print(f"your local ip is: {local_ip}")
            # print(ip_request.text)
            result = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", ip_request.text)
            # pattern = re.compile("\d{0,3}\.\d{0.3}\.\d{0,3}\.\d{0,3}")
            # result = re.search(r"<body.*?>(.*?)</body>", ip_request.text).group(1)
            print(f"your all ip is: {result}")
            result = list(set(result))
            if local_ip in result:
                print(f"processing duplicate ip entry:{result}")
                result.remove(local_ip)
                print(f"processing duplicate ip entry:{result}")

            if len(result) >= 1:
                ip = result[-1]
                return ip
            else:
                return None
        except:
            print(f"can not access: {url}")

            return None

    def searchIPWithFile(self, ip):
        # 1. 创建查询对象
        dbPath = "ip2region.xdb"
        dbPath = os.path.join(os.path.dirname(__file__), "txt/" + dbPath)
        searcher = XdbSearcher(dbfile=dbPath)

        # 2. 执行查询
        ip = "1.2.3.4"
        region_str = searcher.searchByIPStr(ip)
        print(region_str)

        # 3. 关闭searcher
        searcher.close()

    def valid_ipv4(self, IP):
        segement = IP.split(".")
        if len(segement) == 4:
            for s_str in segement:
                if 0 < len(s_str) < 4:
                    for s in s_str:
                        if not s.isdigit():
                            return False
                    if len(s_str) > 1 and s_str[0] == "0" or int(s_str) > 255:
                        return False
                else:
                    return False
        else:
            return False

        return True


    def url_ok(proxies,url):


        try:
            response = requests.head(url,proxies=proxies if proxies else None)
        except Exception as e:
            # print(f"NOT OK: {str(e)}")
            return False
        else:
            if response.status_code == 400 or response.status_code==404:
                # print("OK")
                print(f"NOT OK: HTTP response code {response.status_code}")

                return False
            else:

                return True   
    def valid_ipv6(self, IP):
        set_chars = "0123456789abcdefABCDEF"
        segement = IP.split(":")
        if len(segement) == 8:
            for seg_str in segement:
                if 0 < len(seg_str) < 5:
                    for s in seg_str:
                        if s not in set_chars:
                            return False

                    # make sure no multi '0'
                    #   not sure why test case didn't check '0000'
                    if len(seg_str) > 1 and seg_str[0] == "0" and seg_str[1] == "0":
                        print(2)
                        return False

                else:
                    return False

        else:
            return False

        return True

    def check_proxy(self):


        for option in ipoptions:
            ok = self.url_ok(
                proxies=self.httpx_proxy if self.httpx_proxy else None, url=option
            )
            if ok == False:
                ipoptions.remove(option)
        for option in ipfullinfooptions:
            ok = self.url_ok(
                proxies=self.httpx_proxy if self.httpx_proxy else None, url=option
            )
            if ok == False:
                ipfullinfooptions.remove(option)

        print(f"available ipoptions: {ipoptions} ")
        print(f"available ipoptions: {ipfullinfooptions}")

        # we need to test against optionslist to auto choose best url instead of try catch
        ip = None
        try:
            print("self.httpx_proxy,", type(self.httpx_proxy), self.httpx_proxy)
            ip_request = requests.get(
                "https://jsonip.com",
                proxies=self.httpx_proxy if self.httpx_proxy else None,
            )

            print(ip_request.status_code)
            if ip_request.status_code == 200:
                ip = ip_request.json().get("ip")
                if self.valid_ipv4(ip) == False:
                    res = self.searchIPWithFile(ip)
                    print("{}")
                else:
                    print(f"whooo~jsonip~~~~{ip}")
            else:
                print(
                    f"access ip from jsonip failed,status code:{ip_request.status_code}"
                )
                print(f"start access ip from getip_ip111")

                ip = self.getip_ip111()
                print(f"whooo~getip_ip111:{ip}")
                if ip is None:
                    print(f"start access ip from getip_ifconfig")

                    ip = self.getip_ifconfig()
                    print(f"whooo~getip_ifconfig:{ip}")
                    if ip is None:
                        print(
                            f"access ip from getip_ifconfig failed,use the last solution"
                        )
                        ip = self.get_IP_ip_api_com()
                        if ip is None:
                            return (
                                False,
                                "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                            )
        except:
            print(f"access ip from jsonip failed")
            print(f"start access ip from getip_ip111")

            ip = self.getip_ip111()
            print(f"whooo~getip_ip111:{ip}")
            if ip is None:
                print(f"start access ip from getip_ifconfig")

                ip = self.getip_ifconfig()
                print(f"whooo~getip_ifconfig:{ip}")
                if ip is None:
                    print(f"access ip from getip_ifconfig failed,use the last solution")
                    ip = self.get_IP_ip_api_com()
                    if ip is None:
                        return (
                            False,
                            "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                        )

        print(f"start to get full info of ip:{ip}")

        self.get_IP_fullinfo_ip_api_com(ip)
        if self.country_code is None:
            self.get_IP_fullinfo_ip_api_co(ip)
            self.get_IP_fullinfo_db_ip_com(ip)
            if self.country_code is None:
                return (
                    False,
                    "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                )
        return True, "placeholder"

    def country_to_country_code(country_name):
        try:
            country = pycountry.countries.get(name=country_name)
            if country:
                return country.alpha_2
            else:
                return None
        except LookupError:
            return None

    def check_db_ip_com(self, ip_address):
        try:
            url = f"https://db-ip.com/{ip_address}"
            response = requests.get(
                url,
                proxies=self.httpx_proxy if self.httpx_proxy else None,
            )

            soup = BeautifulSoup(response.text, "html.parser")
            # print("===========", soup)

            # Extract the desired information from the HTML response
            country = soup.find(
                "div", class_="card-text text-white bg-primary mb-2"
            ).text.strip()
            city = soup.find("div", class_="card-text bg-light mb-2").text.strip()
            latitude = soup.find("span", class_="text-monospace").text.strip()
            longitude = soup.find(
                "span", class_="text-monospace", style="margin-left: 15px;"
            ).text.strip()
            timezone = soup.find("div", class_="card-text bg-info mb-2").text.strip()
            local_time = soup.find(
                "div", class_="card-text bg-warning mb-2"
            ).text.strip()
            print("IP Information:")
            print("IP Address:", ip_address)
            print("Country:", country)
            print("City:", city)
            print("Latitude:", latitude)
            print("Longitude:", longitude)
            print("Timezone:", timezone)
            print("Local Time:", local_time)
            self.country = country
            self.country_code = self.country_to_country_code(country)
            self.city = city
            self.latitude = latitude
            self.longitude = longitude
            self.timezone = timezone
            # Print the IP information

            if not self.country:
                return (
                    False,
                    "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                )
            return True, "placeholder"
        except:
            return (
                False,
                "Could not access https://db-ip.comto get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
            )

    def get_IP_ip_api_com(self):
        try:
            ip_request = requests.get(
                f"http://ip-api.com/json",
                proxies=self.httpx_proxy if self.httpx_proxy else None,
            )

            data = ip_request.json()
            ip = data["query"]
            return ip
        except:
            print("we can not parse ip from http://ip-api.com/json")

    def check_ip_api_com(self, ip):
        session = requests.Session()

        session.proxies = self.httpx_proxy
        data={}
        target_url=f"http://ip-api.com/json/{ip}"
        try:
            response = session.get(target_url)


            data = response.json()

            # print("====1====", ip_request.content)
            # print("====2====", ip_request.text)
            # {"status":"success",
            # "country":"United States",
            # "countryCode":"US",
            # "region":"CA",
            # "regionName":"California",
            # "city":"San Jose",
            # "zip":"95113",
            # "lat":37.3342,
            # "lon":-121.892,
            # "timezone":"America/Los_Angeles",
            # "isp":"PEG TECH INC",
            # "org":"PEG TECH INC",
            # "as":"AS54600 PEG TECH INC",
            # "query":"38.26.191.97"}
            self.country = data.get("country")
            self.country_code = data.get("countryCode")
            self.region = data.get("regionName")
            self.city = data.get("city")
            self.zip = data.get("zip")
            self.latitude = data.get("lat")
            self.longitude = data.get("lon")
            self.timezone = data.get("timezone")
            print(f"finish to get full info of ip:{data}")
            if not self.country:
                return (
                    False,
                    "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                )
            return True, "placeholder"
        except:
            return (
                False,
                "Could not access http://ip-api.com/json to get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
            )

    def check_ip_api_co(self, ip):
        try:
            r = requests.get(
                f"https://ipapi.co/json/{ip}",
                proxies=self.httpx_proxy if self.httpx_proxy else None,
            )

            data = r.json()
            #     {
            #     "ip": "38.26.191.97",
            #     "network": "38.26.128.0/17",
            #     "version": "IPv4",
            #     "city": "San Jose",
            #     "region": "California",
            #     "region_code": "CA",
            #     "country": "US",
            #     "country_name": "United States",
            #     "country_code": "US",
            #     "country_code_iso3": "USA",
            #     "country_capital": "Washington",
            #     "country_tld": ".us",
            #     "continent_code": "NA",
            #     "in_eu": false,
            #     "postal": "95054",
            #     "latitude": 37.3931,
            #     "longitude": -121.962,
            #     "timezone": "America/Los_Angeles",
            #     "utc_offset": "-0700",
            #     "country_calling_code": "+1",
            #     "currency": "USD",
            #     "currency_name": "Dollar",
            #     "languages": "en-US,es-US,haw,fr",
            #     "country_area": 9629091.0,
            #     "country_population": 327167434,
            #     "asn": "AS54600",
            #     "org": "PEGTECHINC"
            # }
            self.country = data.get("country")
            self.country_code = data.get("country_code")
            self.region = data.get("region")
            self.city = data.get("city")
            self.zip = data.get("postal")
            self.latitude = data.get("latitude")
            self.longitude = data.get("longitude")
            self.timezone = data.get("timezone")
            print(f"finish to get full info of ip:{data}")
            if not self.country:
                return (
                    False,
                    "Could not get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
                )
            return True, "placeholder"
        except:
            return (
                False,
                "Could not access http://ip-api.com/json to get GeoInformation from proxy (Proxy is Invalid/Failed Check)",
            )

    def get_ip_ipinfo_io(self):
        target_url="https://ipinfo.io/json"
        session = requests.Session()

        session.proxies = self.httpx_proxy
        data={}
        
        try:
            response = session.get(target_url)
            if response.status_code == 200:
                    data = response.json()
            else:
                    print('Failed to retrieve the public IP address get_ip_ipinfo_io.')
        except:
            print('Failed to retrieve the public IP address get_ip_ipinfo_io.')

            # Close the session
        session.close()
        return data

    # Ipapi、Ip2location、Whoer、Ipinfo
    # Create a session with SOCKS proxy


    def get_location_data_ipinfo_io(ip_address):
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url)
        data = response.json()
        return data
    def check_api64ipify(self):
            # Make a request to the target URL to detect your public IP
    # Set the target URL for IP detection
        target_url = 'https://api64.ipify.org?format=json'        
        session = requests.Session()

        session.proxies = self.httpx_proxy
        data={}
        
        try:
            response = session.get(target_url)
            if response.status_code == 200:
                    data = response.json()
                    public_ip = data['ip']
                    print(f'Your public IP address is: {public_ip}')
            else:
                    print('Failed to retrieve the public IP address.')
        except:
            print('Failed to retrieve the public IP address.')

            # Close the session
        session.close()
        return data

    # import IP2Location
    def  ip2location(ip_address):
        # Specify the path to your IP2Location database file (BIN file)
        db_path = 'path/to/your/database_file.BIN'

        # Initialize the IP2Location object with the database file
        ip2location = IP2Location.IP2Location(db_path)

        # IP address you want to look up
        ip_address = '8.8.8.8'

        # Perform the IP lookup
        record = ip2location.get_all(ip_address)
        data=''
        # Extract information from the result
        country = record.country_short
        region = record.region
        city = record.city
        latitude = record.latitude
        longitude = record.longitude

        # Print the location information
        print(f"IP Address: {ip_address}")
        print(f"Country: {country}")
        print(f"Region: {region}")
        print(f"City: {city}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        return data
# Ipapi、 Ip2location、Whoer、Ipinfo
    def check_whoer(self):
        # ip country         
        # # https://whoer.net/v2/geoip2-city
        # {"city_name":"Amsterdam","continent_code":"EU","continent_name":"Europe","country_code":"NL","country_name":"Netherlands","european_union":1,"geoname":2759794,"latitude":52.3807,"longitude":4.903,"metro_code":null,"network":"154.84.1.0\/24","postal_code":"1031","register_country_code":null,"register_country_name":null,"represent_country_code":null,"represent_country_name":null,"subdivision1_code":"NH","subdivision1_name":"North Holland","subdivision2_code":null,"subdivision2_name":null,"time_zone":"Europe\/Amsterdam"}

        target_url = 'https://whoer.net/v2/geoip2-city'        
        session = requests.Session()

        session.proxies = self.httpx_proxy
        data={}
        
        try:
            response = session.get(target_url)
            if response.status_code == 200:
                    data = response.json()
                    country_code = data['country_code']
                    print(f'Your  IP address country_code is: {country_code}')
            else:
                    print('Failed to retrieve the public IP address country_code.')
        except:
            print('Failed to retrieve the public IP address country_code.')

            # Close the session
        session.close()
        return data
# https://whoer.net/v2/geoip2-isp
# {"as_number":54600,"as_organization":"PEG-SV","isp":"Peg Tech","network":"137.175.32.0\/19","organization":"Peg Tech"}

# IP地址：显示目前上网的IP，可以查看代理是否生效；
# 提供商ISP：简单理解，就是像国内的中国联通、移动、电信等运营商；
# Host主机名：主机名就是服务器的名称；
# OS操作系统：就是你手机或者电脑的系统；
# Browser浏览器：你用的什么浏览器打开的就显示什么浏览器；
# DNS：计算机首先寻址DNS服务器，然后才寻址站点本身。同一个域名在各地的DNS分配不同的IP，如果IP所在区域的DNS不稳定或者说繁忙无法马上处理请求，会被自动解析到附近最优的DNS节点；
# Proxy代理服务器：指上网是否使用了代理服务器；
# Anonymizer匿名服务器：它可以隐藏IP地址而不会保存IP连接数据；
# Blacklist黑名单：表示检测到代理IP在这个检测网站数据库中被列为黑名单。比如发垃圾邮件，非法行为的ip。
    def check_ipinfo():
        data={}
        
        return data
# ASN：自治系统，实现IP到ASN的映射和ASN查找；
# company：拥有这个ip的公司或组织，通常分为ISP、企业或托管；
# private：检测用于掩盖用户真实IP地址的各种方法；
# vpn：虚拟网络；proxy：代理；tor：Tor（一种代理类型）；relay：中继使用；service：服务
# Abuse：滥用IP地址的联系信息，帮助研究追踪反击滥用者或盗用者的行为
    def check_iptype(self,ip):
        # 原生IP：是指能看到DNS和IP地址是一个国家的，基本可以认为是原生的，但也有特殊情况就是，如东南亚、欧洲一些国家，DNS会被解析到附近国家。像我使用的IPFoxy家的代理IP，ISP代理测下来基本是纯原生的，在业务层面基本上用起来没有遇到过问题。
        # 双ISP：常提及的双ISP就是指里面查询到的Asn和Company的type属性。有的所谓住宅IP其中的ASN是属于运营商的所以是ISP，但是company不是，这种就是单ISP，而真正的住宅IP无论是ASN还是运营的公司都应该是当地的运营商，像我检测的IPFoxy的这条IP就是双ISP，理论上这样的IP更加稳定。
        data={}
        # dns country ==ip country


        # asn.type==isp  company.type==isp
        # https://ipinfo.io/
        return data

# https://ipdb.ipcalc.co/ipdata
# {"continent":{"name":"Asia","region_name_1":"Asia","region_name_2":"Asia","name_translations":{"de":"Asien","en":"Asia","es":"Asia","fa":" \u0622\u0633\u06cc\u0627","fr":"Asie","ja":"\u30a2\u30b8\u30a2\u5927\u9678","ko":"\uc544\uc2dc\uc544","pt-BR":"\u00c1sia","ru":"\u0410\u0437\u0438\u044f","zh-CN":"\u4e9a\u6d32"}},"country":{"isoCode":"CN","name":"China","name_translations":{"de":"China, Volksrepublik","en":"China","es":"China","fa":"\u0686\u06cc\u0646","fr":"Chine","ja":"\u4e2d\u56fd","ko":"\uc911\uad6d","pt-BR":"China","ru":"\u041a\u0438\u0442\u0430\u0439","zh-CN":"\u4e2d\u56fd"},"flagUrls":{"16":"https:\/\/ipcalc.co\/img\/flags\/16\/cn.png","24":"https:\/\/ipcalc.co\/img\/flags\/24\/cn.png"}},"city":{"name":"Jinrongjie (Xicheng District)","name_translations":{"en":"Jinrongjie (Xicheng District)"}},"postal_code":null,"location":{"latitude":39.8919,"longitude":116.377},"isp":{"asn":4837,"asn_organization":"CHINA UNICOM China169 Backbone","name":"CNC Group CHINA169 Shanxi Province Network","organization":null,"connection_type":"Corporate"}}
    def check_asn_type(self):
        data=self.get_ip_ipinfo_io()   
        print('-',data)     
    def check_ip_coutry(self,ip):
        try:
            data=self.check_whoer(ip)
            if 'country_code' in data:
                return data['country_code']
        except:
            pass
    def check_dns_country(self,ip):

        #  60.215.138.245 China 
        try:
            data=self.check_ip_api_com(ip)
            if 'countryCode' in data:
                return data['countryCode']
        except:
            pass