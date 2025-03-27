from flask import Flask, jsonify, request
from Blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/new_patient', methods=['POST'])
def new_patient():
    data = request.json
    block = blockchain.create_block(patient_id=data['patient_id'], doctor_id=data['doctor_id'], action="Patient Visit")
    return jsonify(block), 201

@app.route('/add_test_result', methods=['POST'])
def add_test_result():
    data = request.json
    block = blockchain.create_block(patient_id=data['patient_id'], doctor_id=data['doctor_id'], action="Test Result", test_results=data['test_results'])
    return jsonify(block), 201

@app.route('/add_prescription', methods=['POST'])
def add_prescription():
    data = request.json
    block = blockchain.create_block(patient_id=data['patient_id'], doctor_id=data['doctor_id'], action="Prescription", prescription=data['prescription'])
    return jsonify(block), 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain.chain), 200

@app.route('/get_incentives', methods=['GET'])
def get_incentives():
    return jsonify(blockchain.get_incentives()), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
