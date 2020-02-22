from flask import Flask,render_template,request
from flask_pymongo import PyMongo
from urllib import parse
import os
from PIL import Image


app = Flask(__name__)

passwd = parse.quote_plus("MongoDBmima12!")
app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = "mongodb+srv://dbuser:{}@xiaobai-vf6jv.gcp.mongodb.net/test?retryWrites=true&w=majority".format(passwd)
mongo = PyMongo(app)
user = mongo.db.user
file = mongo.db.file

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        log_in_username = request.form.get('studentID')
        log_in_passwd = request.form.get('passwd')
        if bool([i for i in user.find({'studentID':log_in_username})])== True and [i for i in user.find({'studentID':log_in_username})][-1]['passwd'] == log_in_passwd:
            return render_template("card.html",username = [i for i in user.find({'studentID':log_in_username})][-1]['username'],commodity = file.find())
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
    if request.method == 'POST':
        commodity_name = request.form.get('commodity_name')
        commodity_about = request.form.get('commodity_about')
        contact_way = request.form.get('contact_way')
        name = request.form.get('name')
        studentID = request.form.get('studentID')
        money = request.form.get('money')
        photograph = request.files.get('photograph')
        if bool(commodity_name) == bool(commodity_about) == bool(contact_way) == bool(name) == bool(studentID) == bool(money) == True:
            UPLOAD_DIC = 'static/upload'
            file_path = os.path.join(UPLOAD_DIC,photograph.filename)
            photograph.save(file_path)
            im = Image.open(file_path)
            # Resize图片大小，入口参数为一个tuple，新的图片大小
            imBackground = im.resize((1024,1024))
            #处理后的图片的存储路径，以及存储格式
            imBackground.save(file_path,'JPEG')
            commodityinfo = {
                'commodity_name':commodity_name,
                'commodity_about':commodity_about,
                'contact_way':contact_way,
                'name':name,
                'studentID':studentID,
                'money':money,
                'path':'static/upload/'+photograph.filename
            }
            file.insert_one(commodityinfo)
            return render_template("release.html",success='success')
    return render_template("release.html",success='请诚实填写')

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

 

 
