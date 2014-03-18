import re

__author__ = 'grainierp'
from pyquery import PyQuery as pq

user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'
proxy_table = pq(
    'https://hidemyass.com/proxy-list/search-226783',
    headers={'User-Agent': user_agent}
)('#listtable')


webIdExtractPattern = re.compile(r"<td><span>([\s\S]*?)(\d+)</td>")
for match in webIdExtractPattern.findall(proxy_table.html()):
    ip = match.groups(1)
    port = match.groups(2)
    print port
