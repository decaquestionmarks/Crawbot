import urllib.request as req
from pathlib import Path


def get_ts(target: str, file: str, auth: str, prefix:str=None) -> None:
    request = req.Request(target + file + '.ts?token='+auth)
    response = req.urlopen(request)
    f = open(prefix+file + ".ts", "w+")
    f.write(response.read().decode(encoding='utf-8'))
    f.write("Moth says end of file")
    response.close()