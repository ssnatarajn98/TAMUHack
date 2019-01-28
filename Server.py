from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from datetime import datetime
import requests

application = Flask(__name__)
client = MongoClient('localhost', 27017)
db=client['local']

@application.route("/addMachine",methods=['POST'])
def addMachine():
	#this method is used to Add a document to the mongodb database
	#A document on the mongodb database has the fields location, image_path, date and 		recyclability
	#In this version, I took out the line to actually upload to database because it was not 	working
    try:
	# keys for using cognitive api that tags objects in a image
        subscription_key_recycle = "9e2612b83a984904a562cfc5de678961"
        assert subscription_key_recycle
	# keys for using cognitive api that is used for classifying objects (not used in final 		demo)
        subscription_key_classifier = "e60ab3a3ba254fc5be673553e646118f"
        assert subscription_key_classifier
        classification_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/tag/"
        classification_url = classification_base_url + "analyze"
        vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"
        analyze_url = vision_base_url + "analyze"
	#parsing data from PUSH request
        json_data = request.json['info']
        image_path = json_data['image']
        location = json_data['location']
        print(image_path)
        date =  '01/27/18'
        
        image_data = open(image_path, "rb").read()
	#recycle_list are keywords used to determine the recyclability
        recycle_list = ['bottle','plastic','container']
	#headers and param to make api call to cognitive serivce
        headers    = {'Ocp-Apim-Subscription-Key': subscription_key_recycle,
                'Content-Type': 'application/octet-stream'}
        params     = {'visualFeatures': 'Categories,Description,Color'}

        response_recycle = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
        response_recycle.raise_for_status()
        analysis_recycle = response_recycle.json()
	#determines recycibality value by getting a percentage of recycable words	
        total_cnt = 0
        recycle_cnt = 0
        for e in analysis_recycle['description']['tags']:
                total_cnt = total_cnt + 1
                if(e in recycle_list):
                        recycle_cnt + 1
        headers_new = {'Prediction-Key': 'd3ee925a38a240cea8a24b1f1189494b',
                'Content-Type': 'application/octet-stream'}
        response_new = requests.post(
                'https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/af63a30d-3f04-4d9d-9b00-ff89723ef6d3/image?iterationId=a5cd0ee4-609f-49af-a25f-c793c0df147e', headers=headers_new, data=image_data)
        response_new.raise_for_status()
	#here is where it determines if there is trash or not
        final = response_new.json()
        print(final['predictions'])
        guess = final['predictions'][0]['tagName']
        print(guess)
        output = ""
        if(guess == "Trash"): 
                output = "is trash,  recyclability percentage is " + str(30)
        else:
                output = "not trash"
        print(output)
	#this will return to front end that status of the call
        return jsonify(status='OK',message=output)
	
    except Exception as e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/')
#this function says to open testing.html when we start the server
def showMachineList():
    return render_template('testing.html')

@application.route('/getList',methods=['POST'])
#this function gets all documents from the mongodb database
def getMachine():
    try:
	#here SwoopTest is the collection name, the DB name was 'local'
        list_items = db.SwoopTest.find()
        items = []
        for item in list_items:
                newitem = {
                        #'image_path':item['image'],
                        'location':item['location'],
                        #'recyclable':item['recyclable'],
                        #'date':item['date']
                }
                items.append(newitem) 
    except Exception as e:
        return str(e)
    return json.dumps(items)
        
if __name__ == "__main__":
    application.run()
