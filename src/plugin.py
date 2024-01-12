import requests
import webbrowser
from flowlauncher import FlowLauncher


class UpsetGalgame(FlowLauncher):
    def query(self, param: str = "") -> list:
        if not param:
            return [
                {
                    "Title": "请输入你要搜索的游戏"
                }
            ]
        rep = requests.get(f"https://www.shinnku.com/api/search?q={param}")
        if rep.status_code != 200:
            return [
                {
                    "Title": "无法获取搜索结果",
                    "subTitle": f"服务器返回： {rep.status_code}",
                }
            ]
        results = rep.json()
        if len(results) == 0:
            return [
                {
                    
                    "Title": "未搜索到相关游戏",
                    "subTitle": "请尝试换个关键词进行搜索"
                }
            ]
        query_result = []
        for i in results:
            name = i["name"]
            size = i["size"]
            query_result.append(
                {
                    "Title": name,
                    "subTitle": f"文件大小: {size}",
                    "jsonRPCAction": {
                        "method": "open_url",
                        "parameters": [f"https://www.shinnku.com/api/download{name}"]
                    }
                }
            )
        return query_result
        

    def open_url(self, url):
        webbrowser.open(url)
