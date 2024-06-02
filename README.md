# FastAPIでToDoアプリ作成

### 準備
$ cd fast-api-todo

### poetryによるPython仮想環境設定
$ poetry init

$ poetry add fastapi

$ poetry add alembic sqlalchemy

※poetryを使用しない場合

$ pip install fastapi uvicorn sqlalchemy

### FastAPI起動
$ poetry run uvicorn run:app --reload --port 8888

### 起動確認
http://127.0.0.1:8888/

### sqlite3の中身確認方法
$ sqlite3 db.sqlite3

sqlite> .table

task user

sqlite> select * from user;

1|admin|0d32bced91aa5c2ee5696fc7995370ae|mailto:hoge@example.com

sqlite> select * from task;

1|1|〇〇の締め切り|2019-12-25 12:00:00.000000|2019-10-08 17:43:31.321445|0

ctrl+Cで終了

### レスポンス確認URL
http://admin:fastapi@127.0.0.1:8888/get

### 参考：
【第1回】FastAPIチュートリアル: ToDoアプリを作ってみよう【環境構築編】

https://rightcode.co.jp/blogs/8708

チートシート～Bootstrap5設置ガイド

https://bootstrap-guide.com/sample/cheatsheet

Basic認証のあるページにユーザ名とパスワードを書いたURLでブラウザからアクセスしました。

https://qiita.com/pugiemonn/items/a9787ed3063487498e82
