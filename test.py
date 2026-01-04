from src.plugin import UpsetGalgame

app = UpsetGalgame()
while True:
    param = input()
    if param == "exit":
        break
    result = app.query(param)
    print(result)