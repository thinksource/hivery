from flask import Flask, current_app, jsonify, request
#from flask_debugtoolbar import DebugToolbarExtension
import json
import codecs
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
#STATIC_FOLDER=os.path.join(APP_ROOT, 'resources')
#app.config['UPLOAD_FOLDER'] = STATIC_FOLDER
print(APP_ROOT)
# set FLASK_APP=main.py
app = Flask(__name__, root_path=APP_ROOT)

JSON_ERROR = {"error": "wrong format of json data received"}
NOTFINDPERSON = {
    "error": "can not find the person with the same data you input"}
JSON_NOPERSON = {
    "error": "can not find correct person with provided person's name"}
JSON_IDERROR = {
    "error": "the person id you input is out of the range of people.json's id"}
app.debug = True
app.config['SECRET_KEY'] = "\xcf\xa6\xe20P&\xd8\x86\xcf'\x863\x7f\xfb\xf9\x16\xd4\xf0\x9bj0\x07$`"
#toolbar = DebugToolbarExtension(app)


def takeset(peoplelist):
    result = set()
    for i in peoplelist:
        result.add(i['index'])
    return result


def loadjson(filename):
    reader = codecs.getreader("utf-8")
    with app.open_resource(filename) as f:
        return json.load(reader(f))


def check_persondata(data):
    if('name' in data and 'age' in data and 'address' in data and 'phone' in data):
        if(data['age'] > 0):
            return True
        else:
            return False
    else:
        return False


@app.route("/")
def hello():
    return "The service is working"

# Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
@app.route("/company/<name>")
def getcompany(name):
    people = app.config["people"]
    companies = app.config["companies"]
    index = -1
    l = len(companies)
    re = []
    for i in range(l):
        if(companies[i]['company'] == name):
            index = companies[i]['index']
            break
    if(index == -1):
        return jsonify({"error": "wrong company name"}), 400
    else:
        for i in range(len(people)):
            if (people[i]['company_id'] == index):
                re.append(people[i])
        return jsonify(re)

# Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends\
# in common which have brown eyes and are still alive.
@app.route("/common",  methods=['GET', 'POST'])
def getcommon():
    people = app.config["people"]
    if request.is_json:
        p_data = request.get_json()
        if(len(p_data) != 2):
            return jsonify(JSON_ERROR), 400
        if not (check_persondata(p_data[0]) and check_persondata(p_data[1])):
            return jsonify(JSON_ERROR), 400
        l = len(people)
        p1 = None
        p2 = None
        for i in range(l):
            if(people[i]['name'] == p_data[0]['name'] and people[i]['age'] == p_data[0]['age']
               and people[i]['address'] == p_data[0]['address'] and people[i]['phone'] == p_data[0]['phone']):
                p1 = people[i]
            if(people[i]['name'] == p_data[1]['name'] and people[i]['age'] == p_data[1]['age']
               and people[i]['address'] == p_data[1]['address'] and people[i]['phone'] == p_data[1]['phone']):
                p2 = people[i]
        if (p1 and p2):
            # app.logger.debug(p1['friends'])
            common_index = takeset(p1['friends']) & takeset(p2['friends'])
            result = []
            for i in range(l):
                if i in common_index:
                    if(people[i]["has_died"] == False and people[i]["eyeColor"] == "brown"):
                        result.append(people[i])
            return jsonify(result)
        else:
            return jsonify(NOTFINDPERSON), 400
    else:
        return jsonify(JSON_ERROR), 400


@app.route("/commonid/<strid1>/<strid2>")
def getidcommon(strid1, strid2):
    people = app.config["people"]
    l = len(people)
    id1 = int(strid1)
    id2 = int(strid2)
    if(id1 < l and id1 >= 0 and id2 < l and id2 >= 0):
        p1 = people[id1]
        p2 = people[id2]
        common_index = takeset(p1['friends']) & takeset(p2['friends'])
        result = []
        for i in range(l):
            if i in common_index:
                if(people[i]["has_died"] == False and people[i]["eyeColor"] == "brown"):
                    result.append(people[i]['name'])
        return jsonify(result)
    return jsonify(JSON_IDERROR), 400

# Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output:
# { "username": "Ahi", "age":"30", "fruits":["banana", "apple"], "vegetables":["beetroot", "lettuce"]}
@app.route("/user/<name>")
def person(name):
    fruits = set(['apple', 'orange', 'strawberry', 'banana'])
    vegetables = set(['celery', 'cucumber',  'carrot', 'beetroot'])
    people = app.config["people"]
    for i in people:
        if i['name'] == name:
            food = i["favouriteFood"]
            f = []
            v = []
            for j in food:
                if j in fruits:
                    f.append(j)
                elif j in vegetables:
                    v.append(j)
            return jsonify({'name': i['name'], 'age': i['age'],  "fruits": f, "vegetables": v})
    return jsonify(JSON_NOPERSON), 400


if __name__ == "__main__":
    # with app.app_context():
    #     people=loadjson("./resources/people.json")
    #     companies=loadjson("resources\\companies.json")
    #
    #     #for(int i=0; i<len(companies);i++):
    #
    #     setattr(g,'people', people)
    #     setattr(g, 'companies', companies)
    #app.config['DEBUG'] = True
    app.config["people"] = loadjson("./resources/people.json")
    app.config["companies"] = loadjson("resources/companies.json")
    # food=set()
    # for i in app.config["people"]:
    #     app.logger.debug(i["favouriteFood"])
    #     food |=set(i["favouriteFood"])
    # print(food)
    # print(current_app.name)
# print(g.companies[0]['index'])
#    print(len(people))
    app.run()
