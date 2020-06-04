# PENGUIN
この Web アプリケーションは、11 月祭に関する事務手続きを補助します。
……っていうアプリを 2 年前に開発した人です。
事務局をやめたので何の権限もありませんが、勉強も兼ねてちゃんと作り直します。

* デプロイしました！！ master ブランチの内容を手動で push します。
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
この度はご興味を持っていただき誠にありがとうございます。
私自身にはプログラミング経験がほとんどないため、PR やコメントを
いただき知見を共有していただくと幸いです。

今のところブランチの命名規則や PR を送る際のポリシーなど
何も決めておりませんので、PR 等ご自由にお送りください。


## Contact
Zuya ([twitter](https://twitter.com/Zoniichan))
