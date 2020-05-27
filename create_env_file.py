import random
import string

env_db = {
    'POSTGRES_DB': {
        'description': 'postgresql のデータベース名',
        'default': 'penguin_db'
    },
    'POSTGRES_USER': {
        'description': 'postgresql のユーザー名',
        'default': 'penguin'
    },
    'POSTGRES_PASSWORD': {
        'description': 'postgresql のパスワード',
        'default': 'penguin_db_password'
    },
}


env_web = {
    'SECRET_KEY': {
        'description': '絶対にバレてはいけない値',
        'random': True
    },
    'DB_NAME': {
        'description': 'postgresql のデータベース名',
        'read': 'POSTGRES_DB'
    },
    'DB_USER': {
        'description': 'postgresql のユーザー名',
        'read': 'POSTGRES_USER'
    },
    'DB_PASSWORD': {
        'description': 'postgresql のパスワード',
        'read': 'POSTGRES_PASSWORD'
    },
    'DB_HOST': {
        'description': 'postgresql のホスト',
        'fixed': 'db'
    },
    'DB_PORT': {
        'description': 'postgresql のポート',
        'default': 5432
    },
    'EMAIL_HOST': {
        'description': 'smtp サーバーのホスト。（DEBUG=True の場合プロンプトに出力するので None でも可）',
        'default': None
    },
    'EMAIL_PORT': {
        'description': 'smtp サーバーのポート（DEBUG=True の場合プロンプトに出力するので None でも可）',
        'default': None
    },
    'EMAIL_HOST_USER': {
        'description': 'メールの送信元アドレス',
        'default': 'hoge@hoge.com'
    },
    'EMAIL_HOST_PASSWORD': {
        'description': 'メールサーバーのパスワード（DEBUG=True の場合プロンプトに出力するので None でも可）',
        'default': None
    },
    'EMAIL_USE_TLS': {
        'description': 'TLS を使用するか？（DEBUG=True の場合プロンプトに出力するので None でも可）',
        'default': 1
    },
    'BASE_URL': {
        'description': 'サイトのアドレスを入力',
        'default': 'http://127.0.0.1:8000'
    },
    'SLACK_TOKEN': {
        'description': 'xoxb から始まる token を入力（DEBUG=True の場合プロンプトに出力するので None でも可）',
        'default': None
    },
    'REDIS_LOCATION': {
        'description': 'redis の場所を指定',
        'fixed': 'redis://redis:6379/0'
    },
    'DEBUG': {
        'description': 'DEBUG モード',
        'default': 1
    }
}


def output_file(data, path, storage):
    """env file を作成する

    args:
        data(dict): 環境変数名→（description→説明, detault→デフォルト値）
        path(str): 環境変数ファイル名
        storage(dict): 今までのデータを保存。環境変数名→環境変数
    """
    print('---file: %s を作成します---' % path)

    output = []

    for key, value in data.items():
        # create prompt
        if value.get('default'):
            prompt = '%s (%s) (Default: %s)> ' % (
                key, value['description'], value['default']
            )
        else:
            prompt = '%s (%s)> ' % (key, value['description'])

        if 'read' in value:
            # すでに入力済みのデータを使用
            element = storage[value['read']]
        elif 'fixed' in value:
            # 変更する必要がない値
            element = value['fixed']
        elif 'random' in value:
            # ランダムな値
            element = ''.join(
                random.choices(string.ascii_letters +
                               string.digits + '-*#=$!^', k=50)
            )
        else:
            element = input(prompt)

        # apply default value
        if element == '' and 'default' in value:
            element = value['default']

        # apply data
        if element != '':
            output.append(
                '%s=%s' % (key, element)
            )

        # append storage
        storage[key] = element

    # final line
    output.append('')

    # output .env.db file
    with open(path, mode='w') as f:
        f.write('\n'.join(output))

    print('---file: %s を作成しました！---' % path)


def main():
    storage = dict()
    output_file(env_db, '.env.db', storage)
    output_file(env_web, '.env.web', storage)


main()
