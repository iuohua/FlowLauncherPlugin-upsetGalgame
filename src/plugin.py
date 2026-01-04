import requests
import webbrowser
import os
from urllib.parse import urljoin

from lxml import etree  # type: ignore[attr-defined]
from flowlauncher import FlowLauncher


class UpsetGalgame(FlowLauncher):
    def query(self, param: str = "") -> list:
        if not param:
            return [
                {
                    "Title": "请输入你要搜索的游戏",
                    "icoPath": "images/search.png"
                }
            ]
        rep = requests.get(f"https://www.shinnku.com/search?q={param}")
        if rep.status_code != 200:
            return [
                {
                    "Title": "无法获取搜索结果",
                    "subTitle": f"服务器返回： {rep.status_code}",
                    "icoPath": "images/fail.png"
                }
            ]
        html = rep.text
        tree = etree.HTML(html)
        
        items = tree.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' p-2 ')]")
        results = []
        for it in items:
            a_nodes = it.xpath('.//a')
            if not a_nodes:
                continue
            a = a_nodes[0]
            href = a.get('href') or ''
            url = urljoin(rep.url, href)
            
            raw_name = (a.text or '').strip()
            name = os.path.splitext(raw_name)[0]
            
            translated_texts = [t.strip() for t in it.xpath(".//div[contains(concat(' ', normalize-space(@class), ' '), ' p-6 ')]//span/text()") if t.strip()]
            translated = translated_texts[0] if translated_texts else ''
            
            size_texts = [t.strip() for t in it.xpath(".//div[contains(concat(' ', normalize-space(@class), ' '), ' p-6 ')]//text()") if t.strip()]
            size = size_texts[-1] if size_texts else ''
            
            results.append({"url": url, "name": name, "size": size, "translated": translated})
        if len(results) == 0:
            return [
                {
                    
                    "Title": "未搜索到相关游戏",
                    "subTitle": "请尝试换个关键词进行搜索",
                    "icoPath": "images/fail.png"
                }
            ]
        query_result = []
        for i in results:
            name = i["name"]
            size = i["size"]
            translated = i.get("translated", "")
            url = i.get("url", "")
            sub = f"类型: {translated} | 文件大小: {size}" if translated else f"文件大小: {size}"
            query_result.append(
                {
                    "Title": name,
                    "subTitle": sub,
                    "jsonRPCAction": {
                        "method": "open_url",
                        "parameters": [url]
                    },
                    "icoPath": "images/zip.png"
                }
            )
        return query_result
        

    def open_url(self, url):
        webbrowser.open(url)
