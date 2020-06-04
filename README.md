# PENGUIN
[![django](https://img.shields.io/badge/django-3.0.6-214c33.svg?style=flat)](https://djangoproject.com/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![CircleCI](https://circleci.com/gh/Zoniisan/penguin.svg?style=shield)](https://circleci.com/gh/Zoniisan/penguin)
[![Maintainability](https://api.codeclimate.com/v1/badges/47f3158caa24c86ea009/maintainability)](https://codeclimate.com/github/Zoniisan/penguin/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/47f3158caa24c86ea009/test_coverage)](https://codeclimate.com/github/Zoniisan/penguin/test_coverage)

この Web アプリケーションは、11 月祭に関する事務手続きを補助します。
……っていうアプリを 2 年前に開発した人です。
事務局をやめたので何の権限もありませんが、勉強も兼ねてちゃんと作り直します。

* デプロイしました！！ **master に push した時点で変更が反映されます**。
    * https://penguin.zoniichan.com
    * メールは実際には送信されません。slack は検証用の slack workspace に
    実際に届きます。参加したい方はご連絡ください。
* Wiki を立てました！！詳しい情報はこちらでご参照ください！
    * https://wiki.zoniichan.com/penguin/

## Prerequirements
* docker-compose

## How to install and run
1. `git clone git@github.com:Zoniisan/penguin.git`
1. **環境変数ファイルを作成する必要があります**。
    * `./envfile.sh` を実行してください。
    * 何も変更しなくても大丈夫ですが、slack を実際に送りたい場合は
    `.env.web.local` の `SLACK_TOKEN` の値を変更してください。

1. `docker-compose up -f docker-compose.local.yml`
    * ビルドからやり直す場合は `--build` を付加してください
    * デタッチモードで起動する場合は `-d` を付加してください
1. `127.0.0.1:8000` にアクセスすれば PENGUIN が起動します


## Post-install
* 開発環境を整えたい方など、詳しい情報を知りたい方は、wiki をご覧ください。
    * https://wiki.zoniichan.com/penguin/


## Current Situation
* ユーザー認証
* プロフィール確認
* 一般京大生→事務局員への「お問い合わせ」
* 事務局員→一般京大生への「通知」
* 管理サイト
* ページトップに表示される「お知らせ」の管理

などの基本的な機能を実装しています。
ここから 11 月祭特有の機能の実装に入る予定です。

## Caution
* **この作品は 11 月祭および 11 月祭事務局とは一切関係ありません**。
* このアプリに関してなにか損害を被るようなことがあったとしても、一切対応しません。
* 適当に pull して遊ぶなど好きにしてもらって構いません。
    * ただし、それっぽいドメインを取得し 11 月祭事務局が運営する
    （本物の）PENGUIN と判別が難しい状態を作るのは控えたほうがいいと思います。
    個人使用の範囲内でお楽しみください。
    * `templates/base.html` に記載されたクレジット「`Bootstrapious.com`」
    については、削除することができないことになっています。


## Contribution
万が一 PR などを送ってくださるなどということがあるのであれば、
[Wiki](https://wiki.zoniichan.com/penguin/) の「開発」の項を
お読みください。

この度は興味を持っていただき、誠にありがとうございます。


## Contact
Zuya ([twitter](https://twitter.com/Zoniichan))
