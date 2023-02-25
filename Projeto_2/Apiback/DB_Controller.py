import psycopg2
import json


class DBController:
    def __init__(self):
        self.db_config = self.load_confing()

    def connect_db(self, database):
        db_config = self.db_config
        db_config["database"] = database
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                database=db_config["database"], user=db_config["user"], password=db_config["password"], host=db_config["host"],
                port=db_config["port"])
            print('Database connectada.')

        except:
            print('Database não conectada.')

        if self.connection is not None:
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

    def connection_db(self):
        db_config = self.db_config
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                user=db_config["user"], password=db_config["password"], host=db_config["host"],
                port=db_config["port"])
            print('Database conectada.')

        except:
            print('Database não conectada.')

        if self.connection is not None:
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

    def create_db(self, name):
        name = name.lower()
        self.connection_db()
        cursor = self.cursor

        cursor.execute("SELECT datname FROM pg_database;")
        list_database = cursor.fetchall()

        list_string = []
        for list in list_database:
            list_string.append(f'{list}')

        if (name) in list_database or (f"('{name}',)") in list_string:
            print("'{}' Database já existe".format(name))
        else:
            print("'{}' Database não existe.".format(name))

            sql = f'''CREATE database {name};'''
            try:
                cursor.execute(sql)
                print("Database criação sucedida........")
                print('Done')
                return True
            except:
                print("Database criação falha........")
                return False

    def create_tables(self):
        self.connect_db(self.db_config["database"])
        sql = self.load_db_script()
        try:
            self.cursor.execute(sql)
            print("Tabelas criadas........")

        except:
            print("Tables não criadas........")

        print('Done')

    def insert_equipamento(self, equipamento):
        self.connect_db(self.db_config["database"])
        print(self.db_config["database"])
        sql = (f'''INSERT INTO Equipamentos (nome, preco_aquisicao, numero_serie, data_fabricacao, fabricante)'''
               f''' VALUES ('{equipamento["nome"]}','''
               f'''{equipamento["preco_aquisicao"]},'''
               f'''{equipamento["numero_serie"]},'''
               f''''{equipamento["data_fabricacao"]}','''
               f''''{equipamento["fabricante"]}');''')
        print(sql)
        try:
            self.cursor.execute(sql)
            print("Insert realizado........")
            return True

        except:
            print("Insert não realizado........")
            return False

    def update_equipamento(self, equipamento):
        self.connect_db(self.db_config["database"])
        sql = (f'''UPDATE Equipamentos'''
               f''' SET nome = '{equipamento["nome"]}','''
               f''' preco_aquisicao = {equipamento["preco_aquisicao"]},'''
               f''' numero_serie = {equipamento["numero_serie"]},'''
               f''' data_fabricacao ='{equipamento["data_fabricacao"]}','''
               f''' fabricante = '{equipamento["fabricante"]}' '''
               f'''WHERE id = {equipamento["id"]};''')
        try:
            self.cursor.execute(sql)
            print("Update realizado........")
            return True

        except:
            print("Update não realizado........")
            return False

    def remove_equipamento(self, id):
        self.connect_db(self.db_config["database"])
        sql = (f'''DELETE FROM Equipamentos'''
               f''' WHERE id = {id};''')
        try:
            self.cursor.execute(sql)
            print("Delete realizado........")
            return True

        except:
            print("Delete não realizado........")
            return False

    def select_equipamento(self, id):
        self.connect_db(self.db_config["database"])
        sql = (f'''SELECT * FROM Equipamentos'''
               f''' WHERE id = {id};''')
        try:
            self.cursor.execute(sql)
            list = self.cursor.fetchall()
            list_string = []
            string = f'{list}'
            size = len(string)
            string = string[2:size-2]
            list_string = string.split(",")
            print("Select realizado........")
            return list_string

        except:
            print("Select não realizado........")

    def select_all_equipamento(self):
        self.connect_db(self.db_config["database"])
        sql = '''SELECT * FROM Equipamentos'''
        try:
            self.cursor.execute(sql)
            list_select = self.cursor.fetchall()
            list_string = []
            for list in list_select:
                string = f'{list}'
                size = len(string)
                string = string[1:size-1]

                list_string.append(string)
            print("Select realizado........")
            return list_string

        except:
            print("Select não realizado........")

    def return_equipamento_list(self):
        list_equipamento = self.select_all_equipamento()
        list_obj = []
        try:
            for list in list_equipamento:
                equipamento = list.split(",")
                equipamento = self.select_formating(equipamento)
                obj = {}
                obj["id"] = equipamento[0].strip()
                obj["nome"] = equipamento[1].strip()
                obj["preco_aquisicao"] = equipamento[2].strip()
                obj["numero_serie"] = equipamento[3].strip()
                obj["data_fabricacao"] = equipamento[4].strip()
                obj["fabricante"] = equipamento[5].strip()
                list_obj.append(obj)
            return list_obj

        except:
            print("Falha em retornar objetos selecionados...")
            return list_obj

    def return_equipamento_obj(self, id):
        obj = {}
        try:
            equipamento = self.select_equipamento(id)
            equipamento = self.select_formating(equipamento)
            obj["id"] = equipamento[0]
            obj["nome"] = equipamento[1]
            obj["preco_aquisicao"] = equipamento[2]
            obj["numero_serie"] = equipamento[3]
            obj["data_fabricacao"] = equipamento[4]
            obj["fabricante"] = equipamento[5]
            return obj
        except:
            print("Falha em retornar o objeto...")
            return obj

# chamados

    def insert_chamado(self, chamado):
        self.connect_db(self.db_config["database"])
        print(self.db_config["database"])
        sql = (f'''INSERT INTO Chamados (titulo, descricao, data_abertura, Equipamentos_id)'''
               f''' VALUES ('{chamado["titulo"]}','''
               f''''{chamado["descricao"]}','''
               f''''{chamado["data_abertura"]}','''
               f'''{chamado["Equipamentos_id"]});''')
        try:
            self.cursor.execute(sql)
            print("Insert realizado........")
            return True

        except:
            print("Insert não realizado........")
            return False

    def update_chamado(self, chamado):
        self.connect_db(self.db_config["database"])
        sql = (f'''UPDATE Chamados'''
               f''' SET titulo = '{chamado["titulo"]}','''
               f''' descricao = '{chamado["descricao"]}','''
               f''' data_abertura = '{chamado["data_abertura"]}','''
               f''' Equipamentos_id = {chamado["Equipamentos_id"]}'''
               f''' WHERE id = {chamado["id"]};''')
        try:
            self.cursor.execute(sql)
            print("Update realizado........")
            return True

        except:
            print("Update não realizado........")
            return False

    def remove_chamado(self, id):
        self.connect_db(self.db_config["database"])
        sql = (f'''DELETE FROM Chamados'''
               f''' WHERE id = {id};''')
        try:
            self.cursor.execute(sql)
            print("Delete realizado........")
            return True

        except:
            print("Delete não realizado........")
            return False

    def select_chamado(self, id):
        self.connect_db(self.db_config["database"])
        sql = (f'''SELECT * FROM Chamados'''
               f''' WHERE id = {id};''')
        try:
            self.cursor.execute(sql)
            list = self.cursor.fetchall()
            list_string = []
            string = f'{list}'
            size = len(string)
            string = string[2:size-2]
            list_string = string.split(",")
            print("Select realizado........")
            return list_string

        except:
            print("Select não realizado........")

    def select_all_chamado(self):
        self.connect_db(self.db_config["database"])
        sql = '''SELECT * FROM Chamados'''
        try:
            self.cursor.execute(sql)
            list_select = self.cursor.fetchall()
            list_string = []
            for list in list_select:
                string = f'{list}'
                size = len(string)
                string = string[1:size-1]

                list_string.append(string)
            print("Select realizado........")
            return list_string

        except:
            print("Select não realizado........")

    def return_chamado_list(self):
        list_chamados = self.select_all_chamado()
        list_obj = []
        try:
            for list in list_chamados:
                chamado = list.split(",")
                chamado = self.select_formating(chamado)
                obj = {}
                obj["id"] = chamado[0]
                obj["titulo"] = chamado[1]
                obj["descricao"] = chamado[2]
                obj["data_abertura"] = chamado[3]
                obj["Equipamentos_id"] = chamado[4]
                list_obj.append(obj)
            return list_obj

        except:
            print("Falha em retornar objetos selecionados...")
            return list_obj

    def return_chamado_obj(self, id):
        try:
            obj = {}
            chamado = self.select_chamado(id)
            chamado = self.select_formating(chamado)
            obj["id"] = chamado[0]
            obj["titulo"] = chamado[1]
            obj["descricao"] = chamado[2]
            obj["data_abertura"] = chamado[3]
            obj["Equipamentos_id"] = chamado[4]
            return obj
        except:
            print("Falha em retornar o objeto selecionado...")
            return obj

    def select_formating(self, list):
        formated_list = []
        for item in list:
            item = item.strip()
            if item[0] == "'":
                item = item[1:-1]
            formated_list.append(item)
        return formated_list

    def load_confing(self):
        file = open("db_config.txt", "r")
        db_config_string = file.read().strip()
        db_config = json.loads(db_config_string)
        return db_config

    def load_db_script(self):
        file = open("db_script.txt", "r")
        db_script = file.read().strip()
        return db_script
