import requests
import webbrowser
from flowlauncher import FlowLauncher


class UpsetGalgame(FlowLauncher):
    def query(self, param: str = "") -> list:
        rep = requests.get(f"https://www.shinnku.com/api/search?q={param}")
        if rep.status_codes != 200:
            return [
                {
                    "Title": "Can not fetch search result",
                    "SubTitle": f"Server return {rep.status_code}",
                }
            ]
            
    def open_url(self, url):
        webbrowser.open(url)
