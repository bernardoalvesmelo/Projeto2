from flask import Flask, request, jsonify
from flask_cors import CORS
from markupsafe import escape
import psycopg2
from DB_Controller import DBController

app = Flask(__name__)
CORS(app)
db_controller = DBController()
if db_controller.create_db("equipamentos_bd"):
    db_controller.create_tables()


@app.route('/equipamentos', methods=['GET'])
def EQUIP():
    equip = db_controller.return_equipamento_list()
    return jsonify(equip)


@app.route('/equipamentos/<id>', methods=['GET'])
def EQUIPALL(id):
    if not id.isdigit():
        return jsonify("Header inválido")
    id = int(id)
    equip = db_controller.return_equipamento_obj(id)
    return jsonify(equip)


@app.route('/equipamentos/update', methods=['POST'])
def EQUIPUPDATE():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify("Body inválido")
    update = purge(data)
    if db_controller.update_equipamento(update):
        return jsonify("Update completado")
    else:
        return jsonify("Update não completado")


@app.route('/equipamentos/insert', methods=['POST'])
def EQUIPINSERT():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify("Body inválido")
    insert = purge(data)
    if db_controller.insert_equipamento(insert):
        return jsonify("Insert completado")
    else:
        return jsonify("Insert não completado")


@app.route('/equipamentos/remove/<id>', methods=['GET'])
def EQUIPREMOVE(id):
    if not id.isdigit():
        return jsonify("Header inválido")
    id = int(id)
    if db_controller.remove_equipamento(id):
        return jsonify("Equipamento removido")
    else:
        return jsonify("Equipamento não removido")

# chamados


@app.route('/chamados', methods=['GET'])
def CHAM():
    cham = db_controller.return_chamado_list()
    return jsonify(cham)


@app.route('/chamados/<id>', methods=['GET'])
def CHAMALL(id):
    if not id.isdigit():
        return jsonify("Header inválido")
    id = int(id)
    cham = db_controller.return_chamado_obj(id)
    return jsonify(cham)


@app.route('/chamados/update', methods=['POST'])
def CHAMUPDATE():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify("Body inválido")
    update = purge(data)
    if db_controller.update_chamado(update):
        return jsonify("Update completado")
    else:
        return jsonify("Update não completado")


@app.route('/chamados/insert', methods=['POST'])
def CHAMINSERT():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify("Body inválido")
    insert = purge(data)
    if db_controller.insert_chamado(insert):
        return jsonify("Insert completado")
    else:
        return jsonify("Insert não completado")


@app.route('/chamados/remove/<id>', methods=['GET'])
def CHAMREMOVE(id):
    if not id.isdigit():
        return jsonify("Header inválido")
    id = int(id)
    if db_controller.remove_chamado(id):
        return jsonify("Chmado removido")
    else:
        return jsonify("Chamado não removido")


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
