from flask import Flask, jsonify, request

app = Flask(__name__)

# Route to take input and return it
@app.route('/echo', methods=['POST'])
def echo():
    data =  request.form.get('text')
    print('data', data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
