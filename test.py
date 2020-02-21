from flask import Flask,render_template,request
import pymongo
from urllib import parse

passwd = parse.quote_plus("MongoDBmima12!")

myclient = pymongo.MongoClient("mongodb+srv://dbuser:{}@xiaobai-vf6jv.gcp.mongodb.net/test?retryWrites=true&w=majority".format(passwd))
# mongodb+srv://dbuser:<password>@cluster0-vf6jv.mongodb.net/test?retryWrites=true&w=majority
# myclient = pymongo.MongoClient("mongodb://localhost:27017/test")
xiaobai = myclient["xiaobai"]
user = xiaobai["user"]
# x = user.find_one()

app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        log_in_username = request.form.get('studentID')
        log_in_passwd = request.form.get('passwd')
        # print([i for i in user.find({'studentID':log_in_username})][-1]['passwd'])
        if bool([i for i in user.find({'studentID':log_in_username})])== True and [i for i in user.find({'studentID':log_in_username})][-1]['passwd'] == log_in_passwd:
            return render_template("card.html",username = [i for i in user.find({'studentID':log_in_username})][-1]['username'])
    return render_template("index.html")
    
@app.route('/test',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        registered_username = request.form.get('name')
        registered_sex = request.form.get('sex')
        registered_studentID = request.form.get('studentID')
        registered_passwd = request.form.get('passwd')
        registered_repasswd = request.form.get('repasswd')
        try:
            # print(bool([i for i in user.find({'studentID':registered_studentID})]),'*************************')
            if len(registered_studentID)==10 and registered_passwd == registered_repasswd and bool([i for i in user.find({'studentID':registered_studentID})])==False:
                userdict = {
                    'username':registered_username,
                    'sex':registered_sex,
                    'studentID':registered_studentID,
                    'passwd':registered_passwd
                }
                user.insert_one(userdict)
                return index()
        except:
            render_template('sign_up.html')

    return render_template('sign_up.html')

@app.route('/release',methods=['POST','GET'])
def release():
    return render_template("release.html")

# @app.route('/name/<order_id>',methods = ['GET','POST'])
# def index(order_id):
#     return '{}'.format(order_id)

# def index():
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/test")
#     mydb = myclient["test"]
#     mycol = mydb["test"]
#     x = mycol.find_one()
#     print(x)
#     return str(x)

if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.run()


 
# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def helloWorld():
#     return "Hello World"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5656, debug=True)

 

 
