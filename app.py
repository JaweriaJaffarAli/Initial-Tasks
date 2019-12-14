from flask import Flask, request
import functools
app = Flask(__name__)

def mydecorator(f):
    @functools.wraps(f)
    def reverseCal(*args, **kwargs):
        req_data = request.get_json()
        if req_data['op'] == '+':
            req_data['op'] = '-'
        f()
    return reverseCal


@app.route( '/calc', methods = ['POST', 'GET'] )
@mydecorator
def calc(*args, **kwargs):
    req_data = request.get_json()
    op1 = str(req_data['op1'])
    op2 = str(req_data['op2'])
    op = req_data['op']
    return 'result: {}'.format(eval(op1 + op + op2))

"""@app.route('/calc', methods = ['POST', 'GET'])
def calc():
    if request.method == 'POST':
        op1 = request.form.get('op1')
        op2 = request.form.get('op2')
        op = request.form.get('op')
        if op == '+':
            res = int(op1) + int(op2)
            return '<p> result: {}</p>'.format(res)

    return ''' <form method = "POST">
            op1 <input type = "number" name = "op1"> 
            op2 <input type = "number" name = "op2">
            op <input type = "text" name = "op" >
            <input type = "submit"> 
            </form>''' 
"""

if __name__ == '__main__':
    app.run(debug=True, port=5000)