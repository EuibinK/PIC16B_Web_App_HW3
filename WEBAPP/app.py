from flask import Flask, g, render_template, request
import io
import sqlite3

app = Flask(__name__)

def get_message_db():
  try:
    return g.message_db
  except:
    g.message_db = sqlite3.connect("message_db.sqlite")
    cmd = "CREATE TABLE IF NOT EXISTS messages (id integer PRIMARY KEY AUTOINCREMENT, name text, message text)"
    cursor = g.message_db.cursor()
    cursor.execute(cmd)
    cursor.close()
    return g.message_db

def insert_message(request):
  input_name = request.form['name']
  input_message = request.form['message']

  db = get_message_db()
  cursor = db.cursor()
  
  cursor.execute(f"INSERT INTO messages (name, message) VALUES (?, ?)", (input_name, input_message))

  db.commit()
  db.close()

def random_messages(limit=5):
  db = get_message_db()
  cursor = db.cursor()
  messages = cursor.execute(f"SELECT message, name FROM messages ORDER BY RANDOM() LIMIT {limit}").fetchall()

  db.close()
  return messages

@app.route('/')
# main page
def main():
  return render_template('main.html')

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
  if request.method == 'GET':
    return render_template('submit.html')
  else:
    try:
      insert_message(request)
      return render_template('submit.html', thanks=True)
    except:
      return render_templaste('submit.html', error=True)


  return render_template('submit.html')

@app.route('/view/', methods=['GET'])
def view():
  return render_template('view.html', messages=random_messages())


