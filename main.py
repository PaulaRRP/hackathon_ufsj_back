import os
import config
import json
import time
from flask import Flask, jsonify, Response, g, request
import uuid
from blueprints.activities import activities
from models.shift import Shift, ShiftSchema
from pymongo import MongoClient
import bcrypt


# substitua pelo seu user e sua senha
client = MongoClient("mongodb://admin:290500pauly@172.17.0.3:27017/")
db = client["mongo"]
collectionProc = db["processes"]
collectionShift = db["shifts"]
collectionUser = db["users"]

def create_app():
    app = Flask(__name__)

    app.register_blueprint(activities, url_prefix="/api/v1/activities")
    # Error 404 handler
    @app.errorhandler(404)
    def resource_not_found(e):
      return jsonify(error=str(e)), 404
    # Error 405 handler
    @app.errorhandler(405)
    def resource_not_found(e):
      return jsonify(error=str(e)), 405
    # Error 401 handler
    @app.errorhandler(401)
    def custom_401(error):
      return Response("API Key required.", 401)
    
    @app.route("/health")
    def hello_world():
      return "server is running"
    
    @app.route('/signup', methods=['POST'])
    def cadastro():
        # Obter dados de cadastro do corpo da solicitação JSON
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        # Verificar se o usuário já existe no MongoDB
        existing_user = collectionUser.find_one({"email": email})

        if existing_user:
            return jsonify({"message": "Email de usuário já cadastrado."}), 400

        # Criptografar a senha antes de armazená-la
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Armazenar os dados do usuário no MongoDB
        new_user = {
            "email": email,
            "password": hashed_password
        }
        collectionUser.insert_one(new_user)

        return jsonify({"message": "Cadastro bem-sucedido!"}), 201
    
    @app.route('/login', methods=['POST'])
    def login():
        # Obter dados de login do corpo da solicitação JSON
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        # Verificar se o usuário existe no MongoDB
        user = collectionUser.find_one({"email": email})
        
        if user:
            # Verificar a senha usando o Bcrypt
            #if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
          user['_id'] = str(user['_id'])
          return jsonify(user), 200
            #else:
             #   return jsonify({"message": "Senha incorreta."}), 401
        else:
            return jsonify({"message": "Usuário não encontrado."}), 404

    
    @app.route('/store_shift', methods=['POST'])
    def store_shift():
        data = request.json  # Assume que os dados são fornecidos como JSON na solicitação POST
        if data:
            # Insere os dados na coleção do MongoDB
            result = collectionShift.insert_one(data)
            return jsonify({"message": "Dados armazenados com sucesso!", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"message": "Dados ausentes na solicitação."}), 400
        
    @app.route('/edit_shift', methods=['POST'])
    def edit_shift():
        data = request.json  
        if data:
            result = collectionShift.insert_one(data)
            return jsonify({"message": "Dados armazenados com sucesso!", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"message": "Dados ausentes na solicitação."}), 400
        
    @app.route('/shifts', methods=['GET'])
    def get_shifts():
        query_string = request.query_string.decode('utf-8')
        data = query_string.split('=')
        
        if data[1] == '1':
          cursor = collectionShift.find_one(sort=[("_id", -1)])
          resultados = dict(cursor)
          resultados['_id'] = str(resultados['_id'])
        else:
          cursor = collectionShift.find({})
          resultados = list(cursor)
        
          for resultado in resultados:
            resultado['_id'] = str(resultado['_id'])
          

        return jsonify(resultados)
    
    @app.route('/shifts_process', methods=['GET'])
    def get_shifts_process():
        query_string = request.query_string.decode('utf-8')
        data = query_string.split('&')
        process = data[0].split('=')[1]
        date = data[1].split('=')[1]
        date = date.split('T')[0]

        print(process)
        print(date)
        
        filtro = { "process": process }
      
        cursor = collectionShift.find(filtro)
        resultados = list(cursor)
        
        resultados_req = []

        for r in resultados:
           dia = r["date_end"].split('T')[0]
           if dia == date:
              resultados_req.append(r)

        for resultado_req in resultados_req:
          resultado_req['_id'] = str(resultado_req['_id'])
          
        return jsonify(resultados_req)
        
          
    
    @app.route('/store_user', methods=['POST'])
    def store_user():
        data = request.json
        if data:
            result = collectionUser.insert_one(data)
            return jsonify({"message": "Dados armazenados com sucesso!", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"message": "Dados ausentes na solicitação."}), 400
        
    @app.route('/users', methods=['GET'])
    def get_users():
        cursor = collectionUser.find({}) 

        resultados = list(cursor)
        
        for resultado in resultados:
           resultado['_id'] = str(resultado['_id'])

        return jsonify(resultados)
    
    @app.route('/store_process', methods=['POST'])
    def store_process():
        data = request.json  
        if data:
            result = collectionProc.insert_one(data)
            return jsonify({"message": "Dados armazenados com sucesso!", "id": str(result.inserted_id)}), 201
        else:
            return jsonify({"message": "Dados ausentes na solicitação."}), 400
        
    @app.route('/processes', methods=['GET'])
    def get_process():
        cursor = collectionProc.find({}) 
        
        resultados = list(cursor)
        
        for resultado in resultados:
           resultado['_id'] = str(resultado['_id'])

        return jsonify(resultados)
      
    
    @app.before_request
    def before_request_func():
      execution_id = uuid.uuid4()
      g.start_time = time.time()
      g.execution_id = execution_id

      print(g.execution_id, "ROUTE CALLED ", request.url)
    
    return app 
    
app = create_app()

if __name__ == "__main__":
  #    app = create_app()
  print(" Starting app...")
  app.run(host="0.0.0.0", port=5000)