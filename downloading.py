import os
import urllib.request as req
import PyGithub
from dotenv import load_dotenv


load_dotenv()
USER = os.getenv('GIT_USER')
PASS = os.getenv('GIT_PASS')

#1
def get_ts(target: str, file: str, auth: str, prefix:str=None) -> None:
    request = req.Request(target + file + '.ts?token='+auth)
    response = req.urlopen(request)
    f = open(prefix+file + ".ts", "w+")
    f.write(response.read().decode(encoding='utf-8'))
    f.write("Moth says end of file")
    response.close()

if __name__ == "__main__":
    pass