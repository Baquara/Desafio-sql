from sqlalchemy import *
from flask import Flask, render_template, request, url_for, flash, redirect, session, jsonify, make_response

app = Flask(__name__)

engine = create_engine('sqlite:///./banco.db?check_same_thread=False')
engine.echo = False
metadata = MetaData(engine)

sql=""

@app.route('/', methods=['GET', 'POST'])
def index():
    global sql
    if request.method=="GET":
        data = engine.execute('SELECT * FROM departamentos')
        headers = ['codigo_departamento','nome_responsavel','login_responsavel','email_responsavel']
        return render_template('template.html', headers=headers,objects=data,sql=sql)
    if request.method=="POST":
        if "sendsql" in request.form:
            codigo = request.form["codigo"]
            nome = request.form["nome"]
            login = request.form["login"]
            email = request.form["email"]
            if email==None:
                sql = ('INSERT INTO departamentos (codigo_departamento, nome_responsavel, login_responsavel) VALUES('+str(codigo)+', \''+str(nome)+'\', \''+str(login)+'\') ON CONFLICT(codigo_departamento) DO UPDATE SET nome_responsavel=\''+str(nome)+'\', login_responsavel=\''+str(login)+'\',email_responsavel=\''+str(email)+'\'')
                with engine.connect() as connection:
                    connection.execute('INSERT INTO departamentos (codigo_departamento, nome_responsavel, login_responsavel) VALUES('+str(codigo)+', \''+str(nome)+'\', \''+str(login)+'\') ON CONFLICT(codigo_departamento) DO UPDATE SET nome_responsavel=\''+str(nome)+'\', login_responsavel=\''+str(login)+'\',email_responsavel=\''+str(email)+'\'')
            else:
                sql = ('INSERT INTO departamentos (codigo_departamento, nome_responsavel, login_responsavel,email_responsavel) VALUES('+str(codigo)+', \''+str(nome)+'\', \''+str(login)+'\', \''+str(email)+'\') ON CONFLICT(codigo_departamento) DO UPDATE SET nome_responsavel=\''+str(nome)+'\', login_responsavel=\''+str(login)+'\',email_responsavel=\''+str(email)+'\'')
                with engine.connect() as connection:
                    connection.execute('INSERT INTO departamentos (codigo_departamento, nome_responsavel, login_responsavel,email_responsavel) VALUES('+str(codigo)+', \''+str(nome)+'\', \''+str(login)+'\', \''+str(email)+'\') ON CONFLICT(codigo_departamento) DO UPDATE SET nome_responsavel=\''+str(nome)+'\', login_responsavel=\''+str(login)+'\',email_responsavel=\''+str(email)+'\'')
        if "recreate" in request.form:
            sql = ('DROP table departamentos;\nCREATE TABLE "departamentos" ("codigo_departamento"	INTEGER UNIQUE,"nome_responsavel"	TEXT,"login_responsavel"	TEXT,"email_responsavel"	TEXT)')
            engine.execute('DROP table departamentos;')
            engine.execute('CREATE TABLE "departamentos" ("codigo_departamento"	INTEGER UNIQUE,"nome_responsavel"	TEXT,"login_responsavel"	TEXT,"email_responsavel"	TEXT)')
        return redirect(url_for('index'))

    



if __name__ == '__main__':
    app.run()
