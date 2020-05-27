# PENGUIN
この Web アプリケーションは、11 月祭に関する事務手続きを補助します。
……っていうアプリを 2 年前に開発した人です。
事務局をやめたので何の権限もありませんが、勉強も兼ねてちゃんと作り直します。

## Prerequirements
* docker-compose
* python (環境変数ファイルを作成するのに使います)

## How to install and run
1. `git clone git@github.com:Zoniisan/nf-penguin.git`
1. **環境変数ファイルを作成する必要があります**。
    * `python create_env_file.py` を実行すればいい感じに作ってくれます。
    * ただし本番環境でなければ何も考えずに Enter を連打すればいいはずです。
    * `DEBUG=True` の場合はメールと slack で送信されるべき情報が標準出力に
    流れるので、メールや slack に関する設定は適当で大丈夫です。
1. `docker-compose up`

* 残念ながら Zuya は docker のことを何も知らないので（適当に調べて Dockerfile などを
作りました）、何か不備があったらごめんなさい。
* 現時点では本番環境での動作を想定していません。本番環境で使用するのは危険なのでやめましょう。
    * 具体的には、gunicorn, nginx 関連の設定をまだしていません。
    * 本番環境では Shibboleth 認証を用いることを想定していますが、現時点で対応していません。

## Caution
* **この作品は 11 月祭および 11 月祭事務局とは一切関係ありません**。
* このアプリに関してなにか損害を被るようなことがあったとしても、一切対応しません。
* 適当に pull して遊ぶなど好きにしてもらって構いません。
    * ただし、それっぽいドメインを取得し 11 月祭事務局が運営する
    （本物の）PENGUIN と判別が難しい状態を作るのは控えたほうがいいと思います。
    個人使用の範囲内でお楽しみください。
    * `templates/base.html` に記載されたクレジット「`Bootstrapious.com`」
    については、削除することができないことになっています。


## Contact
Zuya ([twitter](https://twitter.com/Zoniichan))
