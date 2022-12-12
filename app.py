from flask import Flask, jsonify, request
import os
from flask_restful import Api, Resource
from  pyrebase import *
from flask_cors import CORS

config  = {

  "apiKey": "AIzaSyDvtMJ9KX59L4x6YxDkhv3souAwi6WP9_g",

  "authDomain": "transactions-db870.firebaseapp.com",

  "databaseURL": "https://transactions-db870-default-rtdb.firebaseio.com",

  "projectId": "transactions-db870",

  "storageBucket": "transactions-db870.appspot.com",

  "messagingSenderId": "283759103377",

  "appId": "1:283759103377:web:bec722203b69953c151e30",

  "measurementId": "G-WEB2ZSYYRY"

};
app = Flask(__name__)
api = Api(app)
CORS(app)
firebase = pyrebase.initialize_app(config)

db = firebase.database()
db.child("Network")
class From(Resource):
    def post(self):
        postedData = request.get_json()
        transFrom = postedData["from"]
        if db.child("Network").get().val() is None:

            retJson = {
            "Message": 0,
            "Status Code": 200

            }
            return jsonify(retJson)
        else:

            counter = 0
            for newtrans in db.child("Network").get().each():
                print(newtrans.val())

                check1= str(newtrans.val()['from'])

                if( check1==transFrom ):

                    counter = counter + newtrans.val()['Transactions']


            retJson = {
            "Message": counter,
            "Status Code": 200

            }
            return jsonify(retJson)


class To(Resource):
    def post(self):
        postedData = request.get_json()
        transTo = postedData["to"]
        if db.child("Network").get().val() is None:
            retJson = {
            "Message": 0,
            "Status Code": 200

            }
            return jsonify(retJson)
        else:

            counter = 0
            for newtrans in db.child("Network").get().each():
                print(newtrans.val())

                check1= str(newtrans.val()['to'])

                if( check1==transTo ):

                    counter = counter + newtrans.val()['Transactions']


            retJson = {
            "Message": counter,
            "Status Code": 200

            }
            return jsonify(retJson)
        results = users.find({"to":transTo}).count()
        retJson = {
        "Message": results,
        "Status Code": 200

        }
        return jsonify(retJson)
class FromTo(Resource):
    def post(self):
        postedData = request.get_json()
        transFrom = postedData["from"]
        transTo = postedData["to"]
        if db.child("Network").get().val() is None:
            retJson = {
            "Message": 0,
            "Status Code": 200

            }
            return jsonify(retJson)
        else:

            counter = 0
            for newtrans in db.child("Network").get().each():
                print(newtrans.val())

                check1= str(newtrans.val()['from'])
                check2 = str(newtrans.val()['to'])


                if( check1==transFrom and check2 == transTo ):

                    counter = newtrans.val()['Transactions']
                    break;


            retJson = {
            "Message": counter,
            "Status Code": 200

            }
            return jsonify(retJson)
        results = users.find({"to":transTo}).count()
        retJson = {
        "Message": results,
        "Status Code": 200

        }
        return jsonify(retJson)

class Save(Resource):
    def post(self):
        postedData = request.get_json()
        transFrom =str(postedData["from"])
        transTo = str(postedData["to"])
        hashTrans = str(postedData["hash"])
        historyTrans = {"TransactionHash":hashTrans, "from":transFrom,"to":transTo}
        db.child("Transaction").push(historyTrans)
        
        count = 1
        db.child("Network")
        if db.child("Network").get().val() is None:
            item = {"from":transFrom , "to":transTo,"Transactions":count}
            db.child("Network").push(item)


        else:
            for newtrans in db.child("Network").get().each():
                print(newtrans.val())

                check1= str(newtrans.val()['from'])
                check2 = str(newtrans.val()['to'])
                transcounter = newtrans.val()['Transactions']
                if( check1==transFrom  and check2 == transTo):
                    transcounter += 1
                    db.child("Network").child(newtrans.key()).update({"from": transFrom, "to":transTo, "Transactions":transcounter})
                else:
                    item = {"from":transFrom , "to":transTo,"Transactions":count}
                    db.child("Network").push(item)

        retJson = {
        "Message": "Succesfully Added",
        "Status Code": 200
        }
        return jsonify(retJson)
class TransHistory(Resource):
    def get(self):
        history = []
        if db.child("Network").get().val() is None:
            return jsonify(history)
        else:
            for transhistory in db.child("Transaction").get().each():
                print(transhistory.val())
                history.append(transhistory.val())
            history.reverse()
            return jsonify(history)


api.add_resource(Save, '/save')
api.add_resource(From, '/from')
api.add_resource(FromTo, '/fromto')
api.add_resource(To, '/to')
api.add_resource(TransHistory, '/history')

if __name__=="__main__":
     port = int(os.environ.get('PORT', 33507))
     app.run( port=port, debug=True)
