from flask import Flask, render_template, request
import sqlite3
app = Flask('app')

class post:
  def __init__(self, name, body, _time):
    self.name = name
    self.time = _time
    self.body = body

def db():
  return sqlite3.connect("post.db")

db().cursor().executescript("CREATE TABLE IF NOT EXISTS posts(\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\
        name VARCHAR(25),\
        body VARCHAR(300),\
        time TIMESTAMP DEFAULT (datetime(CURRENT_TIMESTAMP,'+9 hours'))\
    )")

@app.route('/')
def index():
  cursor = db().cursor()
  posts = cursor.execute("SELECT * FROM posts").fetchall()
  tmp = []
  for _post in posts:
    tmp.append(post(_post[1], _post[2], _post[3]).__dict__)

  return render_template("index.html", posts=tmp)

@app.route("/post", methods=["POST"])
def msgpost():
  try:
    name = request.form.get("name", type=str)
    body = request.form.get("body", type=str)
    if not (type(name) is str and type(body) is str) or name == "" or body == "":
      raise Exception("名前または本文が入力されていません")
    cursor = db()
    cursor.execute("INSERT INTO posts(name, body) VALUES(?, ?)", (name, body))
    cursor.commit()
    msg = "メッセージを投稿しました"
  except Exception as e:
    msg = e.args[0]
  return render_template("post.html", msg=msg)

app.run(host='0.0.0.0', port=8080)