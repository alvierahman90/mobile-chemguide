from flask import Flask
import requests
import re

app = Flask(__name__)
CHEMGUIDE_BASE="https://chemguide.co.uk/"

@app.route('/')
@app.route('/<path:path>')
def path(path='/'):
    r = requests.get(CHEMGUIDE_BASE + '/' + path)
    try:
        return re.sub(
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
        return r.content

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
