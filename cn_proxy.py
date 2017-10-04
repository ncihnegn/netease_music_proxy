from lxml import etree
# import concurrent.futures
import paco
# import time
import requests
# import asyncio
import aiohttp

async def check(proxy):
    timeout = 1
    try:
        # start = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://ip111.cn', proxy='http://'+proxy,
                                   timeout=timeout) as res:
                t = await res.text()
                # elapse = time.perf_counter() - start
                # print(elapse)
                return 'China' in t
    except:
        return False

def extract(tr):
    tds = tr.xpath('td')
    return tds[0].text+':'+tds[1].text

def fetch_list():
    page = requests.get('http://cn-proxy.com')
    tree = etree.HTML(page.content)
    proxies = tree.xpath('//tbody/tr')
    return list(map(extract, proxies))

async def filtered_list():
    l = fetch_list()
    # print(l)
    return await (l | paco.filter(check))

cn_proxies = paco.run(filtered_list())
print(cn_proxies)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
