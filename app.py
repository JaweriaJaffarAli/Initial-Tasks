from flask import Flask, request
import functools
app = Flask(__name__)
reverseOp = {"+": "-", "-": "+", "*": "/", "/": "*"}
def mydecorator(f):
    @functools.wraps(f)
    def reverseCal(*args, **kwargs):
        req_data = request.get_json()
        req_data['op'] = reverseOp[req_data['op']]
        result = f(*args, **kwargs)
        return result
    return reverseCal


@app.route( '/calc', methods = ['POST', 'GET'] )
@mydecorator
def calc(*args, **kwargs):
    req_data = request.get_json()
    op1 = str(req_data['op1'])
    op2 = str(req_data['op2'])
    op = req_data['op']
    return 'result: {}'.format(eval(op1 + op + op2))

if __name__ == '__main__':
    app.run(debug=True, port=5000)