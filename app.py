from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Jenkins!',
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'ok'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/greet/<name>')
def greet(name):
    return jsonify({
        'greeting': f'Hello, {name}!',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/v1/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    if not data or 'operation' not in data or 'a' not in data or 'b' not in data:
        return jsonify({'error': 'Missing parameters'}), 400
    
    operation = data['operation']
    a = float(data['a'])
    b = float(data['b'])
    
    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            return jsonify({'error': 'Division by zero'}), 400
        result = a / b
    else:
        return jsonify({'error': 'Invalid operation'}), 400
    
    return jsonify({
        'operation': operation,
        'a': a,
        'b': b,
        'result': result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)