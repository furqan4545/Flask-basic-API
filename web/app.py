# Working code

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
# db is the name of the database that we defined in the container and 27017 is the default port no.
# the above command is just simply making connection with the database
db = client.aNewDB # here  I m creating my database, its the name
UserNum = db["UserNum"]   # its the table name

UserNum.insert({
    "num_of_users":0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        # find all users and fetch the one who is stored on 0th location, with the label num of users
        new_num = prev_num + 1
        UserNum.update({}, {"$set": {"num_of_users":new_num}})
        return "Hello user " + str(new_num)


def checkPostedData(postedData, functionName):
    if functionName == "add" or functionName == "sub" or functionName == "mult":
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif functionName == "divide":
        if "x" not in postedData or "y" not in postedData:
            return  301
        elif int(postedData["y"]) != 0:
            return 200
        else:
            return 302

class Add(Resource):
    def post(self):
        # IF i am here, then the resource Add was requested using the method POST
        # Step 1: Get posted data
        postedData = request.get_json()
        # Step 1b : verify validity of posted data
        status_code = checkPostedData(postedData, "add")
        if status_code != 200:
            retJson = {
                "Message" : "Missing x or y value",
                "status" : status_code
            }
            return jsonify(retJson)
        # if i am here then error code = 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x + y
        retMap = {
            "Message" : ret,
            "status": status_code
        }
        return jsonify(retMap)

#    def get(self):
#        # If I am here, then the resource add was requested using get
#    def put(self):
#        pass
#    def delete(self):
#        pass

class Subtract(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "sub")
        if status_code != 200:
            retJson = {
                "message": "Missing  x or y value",
                "Status" : status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x - y
        retMap = {
            "Message": ret,
            "Status code" : status_code
        }
        return jsonify(retMap)

class Multiply(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "mult")
        if status_code != 200:
            retJson = {
                "Message" : "Missing x or y value",
                "status" : status_code
            }
            return jsonify(retJson)
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x*y
        retMap = {
            "Message": ret,
            "status" : status_code
        }
        return jsonify(retMap)


class Divide(Resource):
    def post(self):
        postedData = request.get_json()
        status_code = checkPostedData(postedData, "divide")
        if status_code == 301:
            retJson = {
                "message" : "missing x or y value",
                "status" : status_code
            }
            return jsonify(retJson)
        elif status_code == 302:
            retJson = {
                "message" : "Y can not be 0",
                "status" : status_code
            }
            return jsonify(retJson)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = (x*1.0) / y
        retMap = {
            "message" : ret,
            "Status" : status_code
        }
        return jsonify(retMap)

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/sub")
api.add_resource(Multiply, "/mult")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")

@app.route("/")
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
