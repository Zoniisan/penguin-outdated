"""settings_env.py を作成する

    * settings_env.py は下記内容を含む。
        * GitHub に上げるべきでない情報（SECRET_KEY など）
        * settings.py から分離しておきたい情報
    * GitHub から pull した場合は、まずこのファイルを実行すること。
"""


import random
import string


# SECRET_KEY はランダム生成
secret_key = ''.join(
    random.choices(string.ascii_letters + string.digits + '-*#=$!^', k=50)
)


# settings_env.py に具体的に書き込みたいデータはここに追記すること。
data = [
    "SECRET_KEY = '%s'" % secret_key,
    "DEBUG = True",
    "DB_NAME = (Your Database Name)",
    "DB_USER = (Your Database Username)",
    "DB_PASSWORD = (Your Database Password)",
    ""
]

# 実際にファイルを作成する
path = 'penguin/settings_env.py'
with open(path, mode='w') as f:
    f.write('\n'.join(data))
