from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def start_database():
    # cria database se não existir, do contrário apenas conecta
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()

    # cria tabela em database user.db
    # cursor.execute('CREATE TABLE tb_users(id INTEGER PRIMARY KEY, nome TEXT NOT NULL, email TEXT NOT NULL)')
    cursor.execute('PRAGMA table_info(tb_users)')
    columns = [col[1] for col in cursor.fetchall()]

    if 'status' not in columns:
        cursor.execute('ALTER TABLE tb_users ADD COLUMN status TEXT DEFAULT "saiu"')
        print('coluna adicionada')

    cursor.execute('UPDATE tb_users SET status = "saiu"')
    print('usuários atualizados')

    # insere dados na tabela tb_users
    # cursor.execute('INSERT INTO tb_users (id, nome, email) VALUES (?, ?, ?)',(1, 'Sara', 's@gmail.com'))
    connection.commit()
    connection.close()

@app.route('/users', methods=['GET'])
def get_users():
    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id, nome, email, status FROM tb_users')
    rows = cursor.fetchall()

    users = [{}]
    for row in rows:
        users = [{'id': row[0], 'nome': row[1], 'email': row[2], 'status': row[3] }]

    connection.close()
    return render_template('users.html', users = users)

@app.route('/users/<int:id>/status', methods=['POST'])
def update_status(id):
    new_status = request.form.get('status')

    connection = sqlite3.connect('user.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE tb_users SET status = ? WHERE id = ?', (new_status, id))
    connection.commit()
    connection.close()

    return redirect(url_for('get_users'))

if __name__ == '__main__':
    start_database()
    app.run(debug=True)