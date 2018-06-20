from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/<tenantid>',methods=['POST'])
def create(tenantid):

    return(jsonify({"msg":'create for %s' % tenantid}))
@app.route('/<tenantid>',methods=['DELETE'])
def delete(tenantid):
    return(jsonify({"msg":'delete for %s' % tenantid}))

@app.route('/',methods=['GET'])
def list():
    return(jsonify({"msg":'list function requested'}))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
