from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
  return "Olá, <b>tudo bem</b>?"
      
@app.route('/teste')
def teste():
  return "Essa página é um <b>teste do novo comando</b>."

@app.route('/nome')
def nome():
    return 'Digite seu nome: <form method="post"><input type="text" name="nome"><input type="submit" value="Enviar"></form>'