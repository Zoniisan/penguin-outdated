# PENGUIN
この Web アプリケーションは、11 月祭に関する事務手続きを補助します。
……っていうアプリを 2 年前に開発した人です。
事務局をやめたので何の権限もありませんが、勉強も兼ねてちゃんと作り直します。

## Prerequirements
* Python 3.8.2
* Postgresql
    * `psql (PostgreSQL) 12.2 (Ubuntu 12.2-4)` で動作確認しています

## How to install and run
1. `git clone git@github.com:Zoniisan/nf-penguin.git` 
1. `pip install requirements.txt` (仮想環境を作ったほうがいいと思います)
1. postgresql のデータベースを作る
    * https://qiita.com/shigechioyo/items/9b5a03ceead6e5ec87ec
    * 「はじめに」〜「パスワード認証へ変更する」まで行えば OK
    * 「Django の設定を変更する」「スーパーユーザーの作成」について、ここではやらなくて良い
1. `python create_settings_env.py`
1. 生成された `settings_env.py` に記載された必要事項を埋める
    * 3.で作成したデータベース関連の情報を `DB_NAME`, `DB_USER`, `DB_PASSWORD` に記載すること
1. `python manage.py migrate`
1. `python manage.py collectstatic`
1. `python manage.py runserver`

## Contact
Zuya ([twitter](https://twitter.com/Zoniichan))
