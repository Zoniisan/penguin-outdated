# PENGUIN
この Web アプリケーションは、11 月祭に関する事務手続きを補助します。
……っていうアプリを 2 年前に開発した人です。
事務局をやめたので何の権限もありませんが、勉強も兼ねてちゃんと作り直します。

* デプロイしました！！ master ブランチの内容を ~~CircleCI~~ 手動で push します。
    * https://penguin.zoniichan.com

## Prerequirements
* docker-compose
* python3 (環境変数ファイルを作成するのに使います)

## How to install and run
1. `git clone git@github.com:Zoniisan/penguin.git`
1. **環境変数ファイルを作成する必要があります**。
    * `python3 create_env_file.py` を実行すればいい感じに作ってくれます。
    * 本番環境でなければ何も考えずに Enter を連打すればいいはずです。
    * `DEBUG=True` の場合はメールと slack で送信されるべき情報が標準出力に
    流れるので、メールや slack に関する設定は適当で大丈夫です。
1. `docker-compose up`

* 残念ながら Zuya は docker のことを何も知らないので（適当に調べて Dockerfile などを
作りました）、何か不備があったらごめんなさい。
* ~~現時点では本番環境での動作を想定していません。本番環境で使用するのは危険なのでやめましょう。~~
    * ~~具体的には、gunicorn, nginx 関連の設定をまだしていません。~~
    * 本番環境では Shibboleth 認証を用いることを想定していますが、現時点で対応していません。
    * **祝** デプロイしました→ https://penguin.zoniichan.com
        * 後述の学生番号・パスワードでログインできます
        * 適当に遊んでもらって構いません（**京都大学 11 月祭とは何の関係もない点に注意**）。
        * ただしメール送信機能については無効にしてあります（迷惑メールの送信を防ぐため）
        * SLACK については `nf-penguin-test.slack.com` に実際に届きます。参加したい人は Twitter にどうぞ。

## Post-install
* 最初は何もデータが入っていません。
* まずは `docker-compose exec web python manage.py createsuperuser` でシステム管理者を作ります
* 次に `docker-compose exec web python manage.py create_many_users` でユーザーを作ります
    * この操作は開発用に架空のユーザーを作るコマンドで、実運用で使用する見込みはありません。
* システム管理者でログインし、メニューから CSV 処理→Group, GroupInfo を選択します
* このリポジトリの `csv/initial_group.csv` をアップロードして OK を押します
    * 事務局の部局担当が登録されます
    * そのあと `docker-compose exec web python manage.py reorder home.GroupInfo` します
* 次に CSV 処理→ContactKind を選択し、`csv/initial_contact_kind` をアップロードします
    * お問い合わせの種類が登録されます
    * そのあと `docker-compose exec web python manage.py reorder home.ContactKind` します
* 次に CSV 処理→Staff登録 を選択し、`csv/initial_staff` をアップロードします
    * `username = 30000000[0-9]{2}` のユーザーがスタッフになり、部局担当に所属します
* 実際の運用でもこの方法でデータ登録を行う見込みです
    * 最初だけ大変だけどあまり変化のないデータの登録はこの方法でやりたい
    * 何か他にいい方法があればおしえてください

### 入力されるデータ
* `home.User`
    * パスワードはすべて `hogehoge` です
    * 学生番号 `9000000000` でスーパーユーザーとしてログインできます
        * 全権を持ちます
        * システム担当に所属します
    * 学生番号 `10000000[0-9]{2}` は一般ユーザー（生徒）です
    * 学生番号 `20000000[0-9]{2}` は一般ユーザー（先生）です
        * 本番環境においては、生徒/先生を Shibboleth 認証の IDP から送信される
        データにより判別していました。
        * 「生徒以外は統一テーマ投票に投票できなくする」などの条件分岐の実装が必要になります。
    * 学生番号 `30000000[0-9]{2}` はスタッフユーザー（事務局員）です。
* `auth.Group`
    * 事務局内の部局です
* `home.OfficeGroup`
    * `auth.Group` を拡張する OneToOne モデルです
    * 各部局に対応するメールアドレスと slack ch. が登録されます
* `home.ContactKind`
    * お問い合わせの種類を登録します

## Current Situation
* ユーザー認証
* プロフィール確認
* 一般京大生→事務局員への「お問い合わせ」
* 事務局員→一般京大生への「通知」
    * ただし現時点ではメールの送信が非同期処理になっていないため、
    大量同時送信については実用性がありません。
* 管理サイト
* ページトップに表示される「お知らせ」の管理

などの基本的な機能を実装しています。
ここから 11 月祭特有の機能の実装に入る予定です。

ここまでの機能に関するドキュメントについては近いうちに構成します。

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
