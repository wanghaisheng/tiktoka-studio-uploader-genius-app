批量导入帐号

注意：填写完成后，请删除示例行

4.1 name：浏览器环境名称， 自定义填写，便于管理（选填）

4.2 remark：备注，自定义填写，便于管理（选填）

4.3 tab：填写启动浏览器时需要打开的标签页（选填）

4.4 platform：填写平台的域名（选填）

4.5 username：用户账号，填写平台登录账号（选填）

4.6 password：用户密码，填写平台登录密码 （选填）

4.7 fakey:填写2FA密钥。适用于网站的二次验证码生成，类似Google身份验证器（选填）

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

4.18 ua：填写UserAgent，如无需指定使用的ua则不填写，由系统随机分配（详情可参考如何导入账号）（选填）

4.19 resolution：填写分辨率，如无需指定使用的分辨率则不填写，默认跟随当前电脑（选填）


批量导入代理




1. 使用本地网络直连，则填写 noproxy 即可。
2. 使用 HTTP\HTTPS\SSH\Socks5\Luminati 代理类型，则根据所需类型填写相应的选项。
    a. 选项：http、https、socks5、ssh、luminati、luminatihttps、luminatisocks5
    b. 若选择该类型，则必须填写【proxy】列

proxy list should be one proxy oneline,and each proxy in such format:
socks5://127.0.0.1:1080;tiktok
socks5://127.0.0.1:1088;youtube



代理类型：socks5

代理主机：127.0.0.1

代理端口：4000

代理账号：user

代理密码：password

填写（中间使用英文符号隔开）：

socks5://127.0.0.1:4000:user:password



3. 使用 Lumauto\Oxylabsauto\IPhtmlauto\IPideaauto\922S5auto\IPFoxyauto 代理类型，则根据所需类型填写相应的选项。
    a. 选项：lumauto、oxylabsauto、iphtmlauto、ipideaauto、922S5、ipfoxyauto。
    b. 若选择该类型，则必须填写【ip】或【countrycode】列，任选其一。




Luminati代理配置

打开已下载TXT文件，可查看您获取的代理信息，每个代理信息均为：zproxy.lum-superproxy.io开头，如下图
```
zproxy.lum-superproxy.io:22225:lum-customer-hl_87123456-zone-static-ip-123.12.123.12:boy123456789
zproxy.lum-superproxy.io:22225:lum-customer-hl_87123456-zone-staticip-123.258.46.172:boy123456789
zproxy.lum-superproxy.io:22225:lum-customer-hl_87123456-zone-statio-ip-15.46.13.14:boy123456789
zproxy.lum-superproxy.io:222225:lum-customer-hl_87123456-zone-statiic-ip-16.47.23.14:boy123456789

```


Lumauto（luminati动态住宅）

