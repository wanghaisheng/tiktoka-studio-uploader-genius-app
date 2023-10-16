# Copyright (C) 2012,2015 Claudio "nex" Guarnieri (@botherder), Optiv, Inc. (brad.spengler@optiv.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import dns.resolver

myresolver = dns.resolver.Resolver()
myresolver.timeout = 5.0
myresolver.lifetime = 5.0
myresolver.domain = dns.name.Name("google-public-dns-a.google.com")
myresolver.nameserver = ['8.8.8.8']


class CheckIP():
    
    name = "recon_checkip"
    description = "Looks up the external IP address"
    severity = 2
    categories = ["recon"]
    authors = ["nex", "Optiv"]
    minimum = "1.2"
    def check_ip(self, pattern, regex=False, all=False):
        """Checks for an IP address being contacted.
        @param pattern: string or expression to check for.
        @param regex: boolean representing if the pattern is a regular
                      expression or not and therefore should be compiled.
        @param all: boolean representing if all results should be returned
                      in a set or not
        @return: depending on the value of param 'all', either a set of
                      matched items or the first matched item
        """

        if all:
            retset = set()

        if not "network" in self.results:
            return None

        hosts = self.results["network"].get("hosts")
        if not hosts:
            return None

        for item in hosts:
            ret = self._check_value(pattern=pattern, subject=item["ip"], regex=regex, all=all, ignorecase=False)
            if ret:
                if all:
                    retset.update(ret)
                else:
                    return item["ip"]

        if all and len(retset) > 0:
            return retset

        return None
    def _get_ip_by_host(self, hostname):
        for data in self.results.get("network", {}).get("hosts", []):
            if data.get("hostname", "") == hostname:
                return [data.get("ip", "")]
        return []

    def _get_ip_by_host_dns(self, hostname):

        ips = list()

        try:
            answers = myresolver.query(hostname, "A")
            print('answers',answers)
            for rdata in answers:
                n = dns.reversename.from_address(rdata.address)
                try:
                    answers_inv = myresolver.query(n, "PTR")
                    for rdata_inv in answers_inv:
                        ips.append(rdata.address)
                except dns.resolver.NoAnswer:
                    ips.append(rdata.address)
                except dns.resolver.NXDOMAIN:
                    ips.append(rdata.address)
        except dns.name.NeedAbsoluteNameOrOrigin:
            print("An attempt was made to convert a non-absolute name to wire when there was also a non-absolute (or missing) origin.")
        except dns.resolver.NoAnswer:
            print("IPs: Impossible to get response")
        except Exception as e:
            # log.info(str(e))
            pass

        return ips

    def check_domain(self, pattern, regex=False, all=False):
        """Checks for a domain being contacted.
        @param pattern: string or expression to check for.
        @param regex: boolean representing if the pattern is a regular
                      expression or not and therefore should be compiled.
        @param all: boolean representing if all results should be returned
                      in a set or not
        @return: depending on the value of param 'all', either a set of
                      matched items or the first matched item
        """

        if all:
            retset = set()

        if not "network" in self.results:
            return None

        domains = self.results["network"].get("domains")
        if not domains:
            return None

        for item in domains:
            ret = self._check_value(pattern=pattern, subject=item["domain"], regex=regex, all=all)
            if ret:
                if all:
                    retset.update(ret)
                else:
                    return item["domain"]

        if all and len(retset) > 0:
            return retset

        return None
    def run(self):
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
        ip_indicators = [
            "23.21.150.121",
        ]

        found_matches = False
        for indicator in dns_indicators:
            if self.check_domain(pattern=indicator):
                self.data.append({"domain" : indicator})
                found_matches = True
        matches = self.check_domain(pattern="^stun[0-9]?\..*", regex=True, all=True)
        if matches:
            found_matches = True
            for match in matches:
                self.data.append({"domain" : match})

        for indicator in ip_indicators:
            if self.check_ip(pattern=indicator):
                self.data.append({"ip" : indicator})
                found_matches = True

        return found_matches

