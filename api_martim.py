from flask import Flask, request, jsonify
from pymongo import MongoClient

from dotenv import load_dotenv
import os

# teste

# Carrega variáveis do arquivo .env
load_dotenv()

# Acessa as variáveis como variáveis de ambiente
mongo_uri = os.getenv("MONGO_URI")

app = Flask(__name__)

client = MongoClient(mongo_uri)
db = client['api_martim']
colecao = db['documentos']

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Nenhum dado recebido'}), 400

    colecao.insert_one(dados)
    return jsonify({'mensagem': 'Documento cadastrado com sucesso!'}), 201

@app.route('/pesquisar_nome', methods=['GET'])
def pesquisar_nome():
    name = request.args.get('nome', '').lower()
    resultado = colecao.find_one({"nome": name})
    if resultado:
        resultado["_id"] = str(resultado["_id"])
        return jsonify(resultado)
    return jsonify({"mensagem": "Nome não encontrado"}), 404

@app.route('/pesquisar_rua', methods=['GET'])
def pesquisar_rua():
    rua = request.args.get('rua', '').lower()
    resultados = colecao.find({"rua": rua})
    saida = []
    for doc in resultados:
        doc["_id"] = str(doc["_id"])
        saida.append(doc)
    return jsonify(saida), 200

@app.route('/pesquisar_compras', methods=['GET'])
def pesquisar_compras():
    produto = request.args.get('produto', '').lower()
    resultados = colecao.find({"compras": {"$elemMatch": {"$regex": produto, "$options": "i"}}})
    saida = []
    for doc in resultados:
        doc["_id"] = str(doc["_id"])
        saida.append(doc)
    return jsonify(saida), 200

if __name__ == '__main__':
    app.run(debug=True)
