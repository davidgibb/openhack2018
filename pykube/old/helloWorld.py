from flask import Flask
from flask import jsonify
from flask import Response
import kubecalls
app = Flask(__name__)

@app.route('/<tenantid>',methods=['POST'])
def create(tenantid):
    ret = kubecalls.create(tenantid)
    return(Response("", status=202, mimetype='application/json'))

@app.route('/<tenantid>',methods=['DELETE'])
def delete(tenantid):
    ret = kubecalls.delete(tenantid)
    return(Response("", status=ret, mimetype='application/json'))

@app.route('/',methods=['GET'])
def list():
    ret = kubecalls.list()
    return(jsonify(ret))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
