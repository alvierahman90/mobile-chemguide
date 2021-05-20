from flask import Flask
import requests
import re
import redis
import time

app = Flask(__name__)
CHEMGUIDE_BASE="https://chemguide.co.uk/"
PAGE_CACHE_DURATION = 3600 # cache pages for an hour before retrieving again
db = redis.Redis(host='db', port=6379, db=0)

class PathKeyType():
    Data = 1
    Date = 2

def pathkey(path, type):
    if type == PathKeyType.Data:
        return f"{path}:data"
    elif type == PathKeyType.Date:
        return f"{path}:date"

def set_cache(path):
    r = requests.get(CHEMGUIDE_BASE + '/' + path)
    try:
        data =  re.sub(
                    r'<table .* width="480"',
                    '<table style="max-width: 60em; margin: 0 auto; font-size: 16px;"',
                    re.sub(
                        r'</?font.*?>',
                        '',
                        re.sub(
                            r'<head>',
                            """<head>
                            <style>
                            body center table tr td { font-size: 1.2em; }
                            body { margin: 2em; line-height: 1.4; }
                            img {
                            width: 60% !important;
                            height: auto !important;
                            max-height: 15em; display:
                            block; margin: 0 auto;
                            object-fit: contain;
                            }
                            img[src="padding.GIF"] { display: none }
                            img[src="padding.gif"] { display: none }
                            </style>""",
                            re.sub(
                                """(?<=<font color="#[a-f0-9]{6}" size="[0-9]" face="Helvetica, Arial"><b>)[a-zA-z\s]*""",
                                "an unnoficial chemguide mirror",
                                str(r.content, encoding='utf-8')
                            )
                        )
                    )
                )
    except UnicodeDecodeError:
        data =  r.content

    db.set(pathkey(path, PathKeyType.Data), data)
    db.set(pathkey(path, PathKeyType.Date), time.time())

def get_page(path):
    date = db.get(pathkey(path, PathKeyType.Date))
    if date is not None:
        if float(str(date, 'utf-8')) + PAGE_CACHE_DURATION < time.time():
            set_cache(path)
    else:
        set_cache(path)
    return db.get(pathkey(path, PathKeyType.Data))

@app.route('/')
@app.route('/<path:path>')
def path(path='/'):
    return get_page(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
