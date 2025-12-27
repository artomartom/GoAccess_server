
import regex as re
import os
import sys

from argparse import ArgumentParser

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from format_parser import  Fields as f

 

addresses_v4 = [
("77.88.9.142",True),
("78.178.85.171",True),
("156.234.180.92",True),
("1.195.198.16",True),
("91.122.53.173",True),
("212.232.55.10",True),
("156.234.180.912",False),
]

addresses_v6 = [
("fd12:3456:789a::1",True),
("2a03:2880:f800:8::",True),
("fdab:cdef:1234:5678:9abc:def0:1234:5678",True),
("fd87:d2e5:2834::feed:1",True),
("fd42:1c0f:7a89::b",True),
("fd99:8877:6655:4433:2211: :ef01:2345",False),
("fdae:1200:4500::1:cad2",True),
("fd47:253f:d91a:0:bevef:cafe:47:11",False),
("fd44:2072:6d31:dead:beef:affe:1d:50da",True),
("fd48:9bda:1f2e:8:0:1234:5678:9abc",True),
("fd40:ec19:3c71:93e1:55aa:fc39:8711:492b",True),
]

time=[
("17/Jul/2025:03:29:00", True),
("08/Jul/2025:13:2s8:59", False),
("022/Jfl/2023:13:28:59", False),
("22/Jfl/2023:13:28:59", True),
("25/Dec/2025:03:35:06", True),
("13/Aug/2025:01:05:02", True),
("13/Aug/2025:00:56:18", True),
("24/Dec/2025:03:11:56", True),
]

http= [
("HTTP/1.1",True),
("HTTP/1.2",True),
("HTTP/2.0",True),
("HTTP/3.0s",False),
("HTTP/3.1",True),
("HTTP/65.1",False),
]

url= [
    ("/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1",True),
    ('''/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1&dfs3="34"''',False),
    ('''/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1&dfs3="''',False),
    ('''/wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1&dfs3=%2234%22''',True),
    ("/.env",True),
    ("/restore.php",True),
    #("/*",False),
    ("*",True),
    ("/ajax/get_local_notifications.php",True),
    ("/?availability=in_stock&filter_automatic-winding=no-power-reserve-38-hours&filter_movement=2414a%2C2403%2C2431-01%2C2415%2C2431&orderby=price-desc&query_type_automatic-winding=or",True),
    ("/заз",False),
    ("/",True),
    ("/product-tag/vostok-amphibia/?filter_movement=2432,2426-12,2431,2416b,2416,2431-12,2415-01,2426-02",True),
    ("/product-category/amphibian-classic/?orderby=date&filter_automatic-winding=no%2Cyes&query_type_automatic-winding=or&filter_movement=2416,2415-01,2416b,2431-12,2415,2409",True),
    ("/?availability=in_stock&filter_movement=2414a%2C2403%2C2431-01%2C2426-12%2C2432-01%2C2415%2C2431-12&orderby=price-des",True),
    (".env",False),

    ]

method=[
    ("GET",True),
    ("HEAD",True),
    ("PUT",True),
    ("POST",True),
    ("DELETE",True),
    ("PATCH",True),
    ("PATCsdH",False),
    ("sd",False),
    ("451",False),
    ("_FSD",False),

]
timezone =[

("+0300", True),
("-0300", True),
("+0000", True),
("+1000", True),
("+0500", True),
("-0500", True),
("-0s500", False),
("+0s00", False),
("+0601", False),
]

refferer =[
    ("https://baikalovostrog.ru/",True),
    ("https://baikalovostrog.ru/",True),
    ("https://5.129.240.78/restore.php",True),
    ("https://5.129.240.78",True),
    ("https://5.129.240.78/",True),
    ("https://dev.megacvet24.ru/rozy/sirenevye/",True),
    ("https://baikalovostrog.ru:443/",True),
    ("http://62.113.44.234",True),
    ("https://maknot.com/",True),
    ("http://185.42.14.195:80/apply.cgi",True),
    ("http://xn--80aatrux.xn--p1ai",True),
    ("http://62.113.44.234:443",True),
    ("http://fd48:9bda:1f2e:8:0:1234:5678:9abc",True),
    ("http://fd48:9bda:1f2e:8:0:1234:5678:9abc:443",True),
    ("http://fd48:9bda:1f2e:8:0:1234:5678:9abc:443/",True),
    ("http://fd48:9bda:1f2e:8:0:1234:5678:9abc:80",True),
    ("https://fd12:3456:789a::1:443",True),
    ("fd48:9bda:1f2e:8:0:1234:5678:9abc:443",False),
    ("https://fd12:3456:789a::1:4sd43",False),
    ("http://s",False    ),
    ("http://baikalovostrogCom:80/",False),
    ("//baikalovostrog.ru/",False),
    ("http://62.113.44.234:44sd3",False),
    ("xn--80aatrux.xn--p1ai",False),

]

x_for = [

    ("156.234.180.92",True),
    ("81.195.198.16",True),
    ("fd87:d2e5:2834::feed:1",True),
    ("2a03:2880:f800:8::, 172.71.194.251",True),
    ("156.234.180.92, 172.71.194.251",True),
    ("2a03:2880:f800:8::,  fd48:9bda:1f2e:8:0:1234:5678:9abc",False),

]

agent= [
("AliyunSecBot/Aliyun(AliyunSecBot@service.alibaba.com)",True),
("-sd",True),
("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",True),
("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",True),
("Mozilla/5.0AppleWebKit/537.36(KHTML,likeGecko;compatible",True),
("Opera/8.79.(X11;Linuxx86_64;et-EE)Presto/2.9.172Version/12.00",True),
('''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0''',True),
('''Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)" "114.119.132.248''',False),
('''Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)" "114.119.132.248"''',False),
('''Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0" "154.209.125.63"''',False),
('''Opera/8.79".(X11;Linuxx86_64;et-EE)Presto/2.9.172Version/12.00''',False),
('''188.170.76.115 - - [14/Aug/2025:00:02:47 +0300 - -] 200 "GET /upload/iblock/6fe/87359048.jpg HTTP/2.0" 4440 "https://kmr10.ru/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36" "-"''', False),
("Python-urllib/3.13",True),
('''Mozilla/5.0 (compatibl"e; YandexRenderResourcesBot/1.0; +http://yandex.com/bots) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0''',False),
("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",True),
("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",True),
("Mozilla/5.0 (Linux; arm_64; Android 12; NCO-LX1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.1823 YaApp_Android/24.120.1 YaSearchBrowser/24.120.1 BroPP/1.0 SA/3 Mobile Safari/537.36",True),
]

log_combined_x_for =[
('''128.71.239.165 - admin [26/Apr/2023:12:52:46 +0300] "GET / HTTP/1.1" 401 195 "https://dev.megacvet24.ru/" "Mozilla/5.0 (Windows NT 5.1; rv:9.0.1) Gecko/20100101 Firefox/9.0.1" "128.71.239.165"''',True      ),
('''177.107.179.208 - - [08/Jul/2025:13:28:59 +0300] "GET /?availability=in_stock&filter_automatic-winding=no-power-reserve-38-hours&filter_movement=2414a%2C2403%2C2431-01%2C2415%2C2431&orderby=price-desc&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0)"''',False      ),
('''188.170.76.115 - - [14/Aug/2025:00:02:47 +0300 - -] 200 "GET /upload/iblock/6fe/87359048.jpg HTTP/2.0" 4440 "https://kmr10.ru/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36" "-"''', False),
('''114.119.132.248 - - [25/Apr/2023:04:09:10 +0300] "GET /image/cache/catalog/7-sirenevyh-roz-60-sm-1-277x277.jpg HTTP/1.1" 401 195 "https://dev.megacvet24.ru/rozy/sirenevye/" "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)" "114.119.132.248"''',True   ),
('''114.119.149.92 - - [25/Apr/2023:13:55:31 +0300] "GET /piony-na-vypisku/ HTTP/1.1" 401 195 "https://dev.megacvet24.ru/rozy/5-kust-pion-roz-miks-50-sm.html" "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)" "114.119.149.92"''',True      ),
('''114.119.149.92 - - [25/Apr/2023:13:55:31 +0300] "GET /piony-na-vypisku/ HTTP/1.1" 401 195 "https://dev.megacvet24.ru/rozy/5-kust-pion-roz-miks-50-sm.html" "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)" "fd48:9bda:1f2e:8:0:1234:5678:9abc"''',True      ),

]
log_combined =[
('''66.249.73.233 - - [08/Jul/2025:13:28:59 +0300] "GET /product/vostok-dial-030934/ HTTP/1.1" 500 2443 "-" "Mozilla/5.0 Safari/537.36 (compatible; Googlebot/2.1; )"''',True      ),
('''114.119.132.248 - - [25/Apr/2023:04:09:10 +0300] "GET /image/cache/catalog/7-sirenevyh-roz-60-sm-1-277x277.jpg HTTP/1.1" 401 195 "https://dev.megacvet24.ru/rozy/sirenevye/" "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)" "114.119.132.248"''',False      ),
('''154.209.125.63 - - [25/Apr/2023:04:47:18 +0300] "GET / HTTP/1.1" 401 195 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0" "154.209.125.63"''',False      ),
('''149.50.96.5 - ffadmin [25/Jul/2025:00:09:58 +0300] "POST /bapply.cgi HTTP/1.1" 499 0 "http://185.42.14.195:80/apply.cgi" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.71 Safari/537.36"''',True      ),
('''177.107.179.208 - - [08/Jul/2025:13:28:59 +0300] "GET /?availability=in_stock&filter_automatic-winding=no-power-reserve-38-hours&filter_movement=2414a%2C2403%2C2431-01%2C2415%2C2431&orderby=price-desc&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0)"''',True      ),
('''103.161.105.25 - - [08/Jul/2025:13:28:59 +0300] "GET /?filter_automatic-winding=no-power-reserve-38-hours&filter_movement=2416b%2Cseiko-vk-73%2C2431%2C2432%2C2414&orderby=rating&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_0 like Mac OS X; it-IT) AppleWebKit/535.50.4 (KHTML, like Gecko) Version/4.0.5 Mobile/8B116 Safari/6535.50.4"''',True      ),
('''18.235.158.19 - - [08/Jul/2025:13:28:59 +0300] "GET /product-tag/vostok-amphibia/?filter_movement=2432,2426-12,2431,2416b,2416,2431-12,2415-01,2426-02 HTTP/1.1" 500 2443 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot) Chrome/119.0.6045.214 Safari/537.36"''',True      ),
('''182.70.166.189 - - [08/Jul/2025:13:28:59 +0300] "GET /?availability=in_stock&filter_movement=2416%2C2426-12%2C2403%2C2415&orderby=price-desc HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/3.0)"''',True      ),
('''212.237.122.243 - - [08/Jul/2025:13:28:59 +0300] "GET /?filter_automatic-winding=yes&filter_movement=2416b%2C2415%2C2409%2C2403%2C2431%2C2414%2Cseiko-nh35&orderby=rating&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (iPod; U; CPU iPhone OS 3_2 like Mac OS X; mag-IN) AppleWebKit/535.5.4 (KHTML, like Gecko) Version/4.0.5 Mobile/8B114 Safari/6535.5.4"''',True      ),
('''66.249.73.233 - - [08/Jul/2025:13:28:59 +0300] "GET /product/vostok-watch-amphibia-amphibian-special-edition-wristwatch-limited-24h-dial-030934/ HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.7151.103 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"''', True),
('''201.79.172.138 - - [08/Jul/2025:13:28:59 +0300] "GET /?availability=in_stock&filter_automatic-winding=no-power-reserve-38-hours&filter_movement=2414a%2C2426-02%2C2426-12%2C2416%2Cseiko-nh35&orderby=popularity&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 11.0; Trident/3.0)"''', True),
('''114.119.144.88 - - [08/Jul/2025:13:28:59 +0300] "GET /product-category/komandirskie-classic/?filter_movement=2432,2416b,2432-01,2415,2426-12 HTTP/1.1" 500 2443 "http://vostok.watch/product-category/komandirskie-classic/?filter_movement=2432%2C2416b%2C2432-01%2C2431%2C2415%2C2426-12" "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)"''', True),
('''136.158.62.14 - - [08/Jul/2025:13:28:59 +0300] "GET /?availability=in_stock&filter_automatic-winding=yes&filter_movement=2426-12%2C2431-01%2C2415-01%2C2414%2Cseiko-nh35%2C2403&orderby=popularity&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (Windows NT 5.01) AppleWebKit/531.1 (KHTML, like Gecko) Chrome/51.0.831.0 Safari/531.1"''', True),
('''177.107.179.208 - - [08/Jul/2025:13:28:59 +0000] "GET /?availability=in_stock&filter_automatic-winding=no-power-reserve-38-hours&filter_movement=2414a%2C2403%2C2431-01%2C2415%2C2431&orderby=price-desc&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0)"''', True),
('''103.161.105.25 - - [08/Jul/2025:13:28:59 +0500] "GET /?filter_automatic-winding=no-power-reserve-38-hours&filter_movement=2416b%2Cseiko-vk-73%2C2431%2C2432%2C2414&orderby=rating&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_0 like Mac OS X; it-IT) AppleWebKit/535.50.4 (KHTML, like Gecko) Version/4.0.5 Mobile/8B116 Safari/6535.50.4"''', True),
('''18.235.158.19 - - [08/Jul/2025:13:28:59 +0300] "GET /product-tag/vostok-amphibia/?filter_movement=2432,2426-12,2431,2416b,2416,2431-12,2415-01,2426-02 HTTP/1.1" 500 2443 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot) Chrome/119.0.6045.214 Safari/537.36"''', True),
('''182.70.166.189 - - [08/Jul/2025:13:28:59 -0600] "GET /?availability=in_stock&filter_movement=2416%2C2426-12%2C2403%2C2415&orderby=price-desc HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.2; Trident/3.0)"''', True),
('''212.237.122.243 - - [08/Jul/2025:13:28:59 +0300] "GET /?filter_automatic-winding=yes&filter_movement=2416b%2C2415%2C2409%2C2403%2C2431%2C2414%2Cseiko-nh35&orderby=rating&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (iPod; U; CPU iPhone OS 3_2 like Mac OS X; mag-IN) AppleWebKit/535.5.4 (KHTML, like Gecko) Version/4.0.5 Mobile/8B114 Safari/6535.5.4"''', True),
('''172.59.112.234 - sds_d212 [08/Jul/2025:13:28:59 +0300] "GET /?filter_automatic-winding=no-power-reserve-38-hours&filter_movement=2416b%2C2415%2C2415-01%2C2416%2Cseiko-vk-73%2C2414%2C2426-02&orderby=rating&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Opera/8.38.(X11; Linux i686; cs-CZ) Presto/2.9.174 Version/10.00"''', True),
('''2a03:2880:f800:8:: - - [08/Jul/2025:13:28:59 +0300] "GET /?filter_movement=2415%2Cseiko-nh35%2C2432%2C2414%2C2414a%2C2432-01&orderby=rating HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (Windows NT 5.01) AppleWebKit/535.0 (KHTML, like Gecko) Chrome/61.0.893.0 Safari/535.0"''', True),
('''18.207.89.138 - - [08/Jul/2025:13:28:59 +0300] "GET /product-tag/vostok-amphibia/?filter_movement=2415-01,2409,2415,2432,2426-12,2426-02,2416,2431,2431-12 HTTP/1.1" 500 2443 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot) Chrome/119.0.6045.214 Safari/537.36"''', True),
('''40.77.167.38 - - [08/Jul/2025:13:28:59 +0300] "GET /?filter_movement=2403,2431-12,seiko-nh35,2416,2426-12,2431,2415,2431-01 HTTP/2.0" 500 2431 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/116.0.1938.76 Safari/537.36"''', True),
('''1.14.14.169 - - [08/Jul/2025:13:28:59 +0300] "POST /xmlrpc.php HTTP/1.1" 200 31 "-" "Apache-HttpClient/4.5.2 (Java/1.8.0_161)"''', True),
('''187.180.167.137 - - [08/Jul/2025:13:28:59 +0300] "GET /product-category/amphibian-classic/?orderby=date&filter_automatic-winding=no%2Cyes&query_type_automatic-winding=or&filter_movement=2416,2415-01,2416b,2431-12,2415,2409 HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (Windows 98) AppleWebKit/536.1 (KHTML, like Gecko) Chrome/19.0.814.0 Safari/536.1"''', True),
('''83.104.125.148 - - [08/Jul/2025:13:28:59 +0300] "GET /?filter_automatic-winding=yes&filter_movement=2416b%2C2415%2C2431%2Cseiko-vk-73%2C31659-3133%2Cseiko-nh35%2C2415-01&orderby=rating&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_0 like Mac OS X; de-BE) AppleWebKit/535.12.6 (KHTML, like Gecko) Version/3.0.5 Mobile/8B112 Safari/6535.12.6"''', True),
('''39.43.4.239 - - [08/Jul/2025:13:28:59 +0300] "GET /?availability=in_stock&filter_automatic-winding=yes%2Cno-power-reserve-38-hours&filter_movement=2414a%2C2415%2C2414%2C2409%2C2415-01%2C2432-01%2C2403&orderby=price-desc&query_type_automatic-winding=or HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/51.0.861.0 Safari/535.2"''', True),
('''187.13.41.123 - - [08/Jul/2025:13:28:59 +0300] "GET /?availability=in_stock&filter_movement=2414a%2C2403%2C2431-01%2C2426-12%2C2432-01%2C2415%2C2431-12&orderby=price-desc HTTP/1.1" 500 2443 "-" "Mozilla/5.0 (compatible; MSIE 5.0; Windows NT 5.2; Trident/3.1)"''', True),
('''207.46.13.127 - - [08/Jul/2025:13:28:59 +0300] "GET /?filter_movement=2426-02,2414,2414a,2415,2431-12 HTTP/2.0" 500 2431 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) Chrome/116.0.1938.76 Safari/537.36"''', True),
('''91.122.53.173 - - [13/Aug/2025:00:56:18 +0300] "GET /.env HTTP/1.0" 404 135796 "-" "Python-urllib/3.13"''', True),
('''4.217.254.58 - - [13/Aug/2025:01:29:36 +0300] "GET /file17.php HTTP/1.0" 404 135740 "-" "-"''', True),
('''188.170.76.115 - - [14/Aug/2025:00:02:47 +0300 - -] 200 "GET /upload/iblock/6fe/87359048.jpg HTTP/2.0" 4440 "https://kmr10.ru/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36" "-"''', False),
('''46.149.67.20 - - [13/Aug/2025:04:28:44 +0300] "GET / HTTP/1.0" 200 40206 "http://baikalovostrog.ru/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"''', True),
('''188.75.207.150 - - [12/Aug/2025:06:25:16 +0300] "GET /wp-content/uploads/2025/01/689x919-0xunt6cm1s-5028848775689678210-siuznr.jpg HTTP/1.1" 200 59001 "https://fashion-likes.ru/beauty/modnye-strizhki-2025-varianty-dlya-lyuboj-dliny-kotorye-zaxochetsya-povtorit/" "Mozilla/5.0 (Linux; Android 12; FOA-LX9 Build/HUAWEIFOA-LX9; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.196 Mobile Safari/537.36 [Pinterest/Android]"''', True),
('''178.125.103.51 - - [12/Aug/2025:06:27:32 +0300] "GET /wp-content/cache/thumb/54/de1a226cd148054_360x181.png HTTP/1.1" 200 123396 "https://fashion-likes.ru/beauty/3-parfyuma-kotorye-paxnut-franciej-ili-kak-pochuvstvovat-sebya-parizhankoj/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"''', True),
('''95.108.213.199 - - [13/Aug/2025:01:05:02 +0300] "GET /wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1 HTTP/1.1" 200 5355 "https://baikalovostrog.ru/" "Mozilla/5.0 (compatible; YandexRenderResourcesBot/1.0; +http://yandex.com/bots) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0"''', True),
('''109.173.96.51 - regru [20/Aug/2025:19:15:40 +0300] "GET /wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1 HTTP/1.1" 200 4894 "https://paltokm.ru/wp-admin/install.php" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0"''', True),
('''46.149.67.20 - - [13/Aug/2025:00:00:40 +0300] "GET / HTTP/1.0" 200 40200 "http://baikalovostrog.ru/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"''', True),
('''91.122.53.173 - - [13/Aug/2025:00:56:18 +0300] "GET /.env HTTP/1.0" 404 135796 "-" "Python-urllib/3.13"''', True),
('''46.149.67.20 - - [13/Aug/2025:04:28:44 +0300] "GET / HTTP/1.0" 200 40206 "http://baikalovostrog.ru/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"''', True),
('''89.113.144.165 - - [11/Aug/2025:00:03:10 +0300] "GET / HTTP/1.1" 200 8526 "https://yandex.ru/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/28.0 Chrome/130.0.0.0 Mobile Safari/537.36"''', True),
('''114.119.144.88 - - [08/Jul/2025:13:28:59 +0300] "GET /product-category/komandirskie-classic/?filter_movement=2432,2416b,2432-01,2415,2426-12 HTTP/1.1" 500 2443 "http://vostok.watch/product-category/komandirskie-classic/?filter_movement=2432%2C2416b%2C2432-01%2C2431%2C2415%2C2426-12" "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)"''', True),
('''188.75.207.150 - - [12/Aug/2025:06:25:16 +0300] "GET /wp-content/uploads/2025/01/689x919-0xunt6cm1s-5028848775689678210-siuznr.jpg HTTP/1.1" 200 59001 "https://fashion-likes.ru/beauty/modnye-strizhki-2025-varianty-dlya-lyuboj-dliny-kotorye-zaxochetsya-povtorit/" "Mozilla/5.0 (Linux; Android 12; FOA-LX9 Build/HUAWEIFOA-LX9; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/114.0.5735.196 Mobile Safari/537.36 [Pinterest/Android]"''', True),
('''178.125.103.51 - - [12/Aug/2025:06:27:32 +0300] "GET /wp-content/cache/thumb/54/de1a226cd148054_360x181.png HTTP/1.1" 200 123396 "https://fashion-likes.ru/beauty/3-parfyuma-kotorye-paxnut-franciej-ili-kak-pochuvstvovat-sebya-parizhankoj/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"''', True),
('''5.255.231.124 - - [15/Aug/2025:13:00:53 +0300] "GET /wp-includes/js/jquery/jquery.min.js?ver=3.7.1 HTTP/1.1" 200 30646 "https://barnaul.tentium.ru/brezent/brezentovye-tenty/" "Mozilla/5.0 (compatible; YandexRenderResourcesBot/1.0; +http://yandex.com/bots) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0"''', True),
('''95.108.213.199 - - [13/Aug/2025:01:05:02 +0300] "GET /wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1 HTTP/1.1" 200 5355 "https://baikalovostrog.ru/" "Mozilla/5.0 (compatible; YandexRenderResourcesBot/1.0; +http://yandex.com/bots) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0"''', True),
('''46.149.67.20 - - [13/Aug/2025:00:59:09 +0300] "POST /wp-cron.php?doing_wp_cron=1755035948.6907539367675781250000 HTTP/1.1" 200 0 "-" "WordPress/6.8.2; https://baikalovostrog.ru"''', True),
('''94.138.132.183 - - [12/Aug/2025:06:25:11 +0300] "GET /wp-content/cache/thumb/43/fc359bb7befa443_370x0.png HTTP/1.1" 200 110823 "https://mama-likes.ru/dizajn-interera/13-samyh-neudachnyh-reshenij-dlya-kuhni.html" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36"''', True),
('''43.157.172.39 - - [22/Jul/2025:03:02:23 +0000] "GET / HTTP/1.1" 404 711 "http://62.113.44.234:443" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"''', True),
('''114.119.157.56 - - [08/Jul/2025:13:29:28 +0300] "GET /product-category/amphibian-classic/?orderby=rating&filter_automatic-winding=no,yes&query_type_automatic-winding=or&filter_movement=2409,2431,2416,2431-12 HTTP/1.1" 499 0 "https://vostok.watch/product-category/amphibian-classic/?orderby=rating&filter_movement=2409%2C2431%2C2416&filter_automatic-winding=no%2Cyes&query_type_automatic-winding=or" "Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://webmaster.petalsearch.com/site/petalbot)"''', True),
('''109.173.96.51 - regru [20/Aug/2025:19:15:40 +0300] "GET /wp-includes/js/jquery/jquery-migrate.min.js?ver=3.4.1 HTTP/1.1" 200 4894 "https://paltokm.ru/wp-admin/install.php" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0"''', True),
#('''''', True),
]

log_bitrixvm_main =[

('''89.111.133.192 - - [18/Aug/2025:04:13:10 +0300 - -] 301 "GET /opinion/ HTTP/1.1" 162 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36" "185.242.122.4"''', True),
('''89.111.133.192 - - [18/Aug/2025:04:13:10 +0300 - -] 301 "GET /opinion/ HTTP/1.1" 162 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"''', False),
('''85.192.11.9 - - [18/Aug/2025:03:51:01 +0300 - 0.031] 200 "GET /details/rss/ HTTP/1.0" 168459 "http://dvinatoday.ru/details/rss/" "Mozilla/5.0 (compatible; Linux; x64; en-us) KHTML/4.3.5 (like Gecko) Chrome/32.3.187.919 Safari/544.81" "-"''', True),
('''65.21.193.198 - - [17/Jul/2025:16:17:51 +0300 - 0.000] 502 "GET / HTTP/2.0" 1135 "https://nasha-set.ru" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" "65.21.193.198"''', True),
('''188.170.76.115 - - [14/Aug/2025:00:02:45 +0300 - 0.062] 200 "GET / HTTP/2.0" 23615 "https://ru.m.wikipedia.org/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36" "-"''', True),
('''188.170.76.115 - - [14/Aug/2025:00:02:47 +0300 - -] 200 "GET /upload/iblock/6fe/87359048.jpg HTTP/2.0" 4440 "https://kmr10.ru/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36" "-"''', True),
('''188.170.76.115 - - [14/Aug/2025:00:02:47 +0300 - -] 200 "GET /upload/iblock/6fe/87359048.jpg HTTP/2.0" 4440 "https://kmr10.ru/" "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36" "fd48:9bda:1f2e:8:0:1234:5678:9abc"''', True),
('''2.57.23.215 - - [11/Aug/2025:00:00:19 +0300 - 0.038] 404 "GET /bitrix/redirect.php?goto=https://kb.smds.us/index.php/User:Conservatory-repair-cost1837 HTTP/1.1" 582 "https://xn--h1algfd.xn--p1ai/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" "-"''', True),
('''185.40.4.92 - - [18/Aug/2025:03:50:12 +0300 - -] 304 "GET /service-worker.js HTTP/2.0" 0 "https://dvinatoday.ru/service-worker.js" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36" "-"''', True),

#('''''', True),

]

log_hestia = [
('''185.111.218.118 - - [17/Aug/2025:00:39:12 +0300] GET / HTTP/1.1 "301" 162 "-" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.2 (KHTML, like Gecko, WEBO Pulsar) Chrome/15.0.874.106 Safari/535.2" "-"''', True),
('''42.236.12.229 - - [17/Aug/2025:09:31:53 +0300] GET / HTTP/1.1 "301" 162 "http://serginnetti.ru/" "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36; 360Spider" "-"''', True),
('''65.109.19.160 - - [17/Aug/2025:11:21:55 +0300] GET /upload/iblock/808/igyz3r4jljq04ceyhjgwx2ys1gaxvz5r.jpg HTTP/1.0 "301" 162 "-" "meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)" "2a03:2880:f800:8::, 172.71.194.251"''', True),
('''143.92.32.30 - - [19/Aug/2025:13:29:29 +0300] GET /api/pages/login HTTP/1.1 "301" 162 "http://serginnetti.ru" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36" "117.66.150.77"''', True),
('''65.109.19.160 - - [20/Aug/2025:21:47:38 +0300] GET /upload/iblock/b8c/b8ccfece7e0fa167f85e5d7ec47e0aa8.jpg HTTP/1.0 "301" 162 "-" "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Amazonbot/0.1; +https://developer.amazon.com/support/amazonbot) Chrome/119.0.6045.214 Safari/537.36" "54.225.98.148, 172.71.127.125"''', True),
('''24.83.200.235 - - [17/Aug/2025:01:21:38 +0300] HEAD /site HTTP/1.1 "301" 0 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36" "-"''', True),
('''1.169.98.245 - - [17/Aug/2025:01:23:20 +0300] GET / HTTP/1.0 "301" 162 "http://serginnetti.ru/" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" "-"''', True),
]

def run_test(regex :str, samples :list):
    for sample in samples:
        pattern = re.compile(regex)
        value, valid = sample
        match = pattern.fullmatch(value)

        if AUTOMATED:
            assert  (match and valid) or (not match and not valid),  f"❌ {value}"
        else:
            if (match and valid) or (not match and not valid):
                print(f"✅ {value}")
            else:
                print(f"❌ {value}")




def run_all():
    ## tokens
    run_test(regex=f.mthd, samples=method)
    run_test(regex=f.a_v4, samples=addresses_v4)
    run_test(regex=f.a_v6, samples=addresses_v6)
    run_test(regex=f.ip, samples=addresses_v4)
    run_test(regex=f.ip, samples=addresses_v6)
    run_test(regex=f.http, samples=http)
    run_test(regex=f.url, samples=url)
    run_test(regex=f.rfr, samples=refferer)
    run_test(regex=f.timzn, samples=timezone)
    run_test(regex=f.agnt, samples=agent)
    run_test(regex=f.datim, samples=time)
    run_test(regex=f.x_for, samples=x_for)
    ## formats
    run_test(regex=f.combined, samples=log_combined)
    run_test(regex=f.bitrixvm_main, samples=log_bitrixvm_main)
    run_test(regex=f.combined_x_for, samples=log_combined_x_for)
    run_test(regex=f.hestia, samples=log_hestia)



if __name__ == '__main__':
    
    parser = ArgumentParser("test_args")
    parser.add_argument("-a","--automated",default=False,action="store_true",help="use asserts instead of console logs")
    args = parser.parse_args()
    AUTOMATED = args.automated
    run_all()
