from flask import Flask, request, jsonify, session
from flask_cors import CORS
from markupsafe import escape
from DB_Controller import DBController
import hashlib

app = Flask(__name__)
CORS(app, supports_credentials=True)
db_controller = DBController()
if db_controller.create_db("equipamentos_bd"):
    db_controller.create_tables()

#!!!Change the secret_key and passwords, the default ones are public as the code is public on git!!!
#!!!Mude o secret_key e passwords, as de padrão estão públicas no git!!!
app.secret_key = '_5#y3L"F4Q8z\n\xec]/'
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['CORS_SUPPORTS_CREDENTIALS'] = True

users = {
    "admin": {"username": "admin", "password": "admin"},
    "user": {"username": "user", "password": "password"}
}

for user in users:
    password = users[user]["password"]
    users[user]["password"] = hashlib.sha256(password.encode()).hexdigest()


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = users.get(username)
    if user and hashlib.sha256(password.encode()).hexdigest() == user["password"]:
        session["username"] = username
        return jsonify("Login sucedido!")
    else:
        return jsonify("Erro no usário ou senha!")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return jsonify("Logout sucedido")

@app.route('/equipamentos', methods=['GET'])
def EQUIP():
    if "username" in session:
        equip = db_controller.return_equipamento_list()
        return jsonify(equip)
    else:
        return jsonify("Necessário login")


@app.route('/equipamentos/<id>', methods=['GET'])
def EQUIPALL(id):
    if "username" in session:
        if not id.isdigit():
            return jsonify("Header inválido")
        id = int(id)
        equip = db_controller.return_equipamento_obj(id)
        return jsonify(equip)
    else:
        return jsonify("Necessário login")


@app.route('/equipamentos/update', methods=['POST'])
def EQUIPUPDATE():
    if "username" in session:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify("Body inválido")
        update = purge(data)
        if db_controller.update_equipamento(update):
            return jsonify("Update completado")
        else:
            return jsonify("Update não completado")
    else:
        return jsonify("Necessário login")


@app.route('/equipamentos/insert', methods=['POST'])
def EQUIPINSERT():
    if "username" in session:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify("Body inválido")
        insert = purge(data)
        if db_controller.insert_equipamento(insert):
            return jsonify("Insert completado")
        else:
            return jsonify("Insert não completado")
    else:
        return jsonify("Necessário login")


@app.route('/equipamentos/remove/<id>', methods=['GET'])
def EQUIPREMOVE(id):
    if "username" in session:
        if not id.isdigit():
            return jsonify("Header inválido")
        id = int(id)
        if db_controller.remove_equipamento(id):
            return jsonify("Equipamento removido")
        else:
            return jsonify("Equipamento não removido")
    else:
        return jsonify("Necessário login")

# chamados


@app.route('/chamados', methods=['GET'])
def CHAM():
    if "username" in session:
        cham = db_controller.return_chamado_list()
        return jsonify(cham)
    else:
        return jsonify("Necessário login")


@app.route('/chamados/<id>', methods=['GET'])
def CHAMALL(id):
    if "username" in session:
        if not id.isdigit():
            return jsonify("Header inválido")
        id = int(id)
        cham = db_controller.return_chamado_obj(id)
        return jsonify(cham)
    else:
        return jsonify("Necessário login")


@app.route('/chamados/update', methods=['POST'])
def CHAMUPDATE():
    if "username" in session:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify("Body inválido")
        update = purge(data)
        if db_controller.update_chamado(update):
            return jsonify("Update completado")
        else:
            return jsonify("Update não completado")
    else:
        return jsonify("Necessário login")


@app.route('/chamados/insert', methods=['POST'])
def CHAMINSERT():
    if "username" in session:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify("Body inválido")
        insert = purge(data)
        if db_controller.insert_chamado(insert):
            return jsonify("Insert completado")
        else:
            return jsonify("Insert não completado")
    else:
        return jsonify("Necessário login")


@app.route('/chamados/remove/<id>', methods=['GET'])
def CHAMREMOVE(id):
    if "username" in session:
        if not id.isdigit():
            return jsonify("Header inválido")
        id = int(id)
        if db_controller.remove_chamado(id):
            return jsonify("Chamado removido")
        else:
            return jsonify("Chamado não removido")
    else:
        return jsonify("Necessário login")


def purge(data):
    purged_data = {}
    for key, value in data.items():
        cleaned_value = value.replace('<', '').replace('>', '')
        escaped_value_html = escape(cleaned_value)
        purged_data[key] = escaped_value_html
    return purged_data


if __name__ == "__main__":
    app.run()
    #app.run(host='0.0.0.0', debug=False)
