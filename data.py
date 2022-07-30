from flask import Flask,request,render_template,session
import csv
import os
import re
import smtplib as gmail


app=Flask(__name__)
app.debug=True
data1=[]
data=[]
data2=[]
@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')
@app.route("/result",methods=['POST','GET'])
def result():
    data1.clear()
    data.clear()
    data2.clear()
    if not request.files['data']:
        return render_template('index.html')
    if request.method=='POST':
        file=request.files['data']
        target=os.path.join('FILE_UPLOADS',file.filename)
        file.save(target)
        with open(target,"r") as f:
            csv_file=csv.reader(f)
            for row in csv_file:       
                data.append(str(row)[2:-2]) 
        for email in data[1:]:
            if re.fullmatch('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',email):
                data1.append(email)
            else:
                data2.append(email)     

    return render_template('index_detail.html',valid=data1,invalid=data2)
@app.route('/recievedata',methods=['POST','GET'])
def getdata():
    return render_template('index_form.html')
@app.route('/sendmail',methods=['POST','GET'])
def mailsender():
    ob=gmail.SMTP('smtp.gmail.com',587)
    ob.ehlo()
    ob.starttls()
    if request.method=='POST':
        sendermail=request.form['email']
        senderpassword=request.form['password']
        subject=request.form['sub']
        body=request.form['message']
        msg="Subject:{0}\n\n{1}".format(subject,body)
        ob.login(sendermail,senderpassword)

        for email in data1:
            ob.sendmail(sendermail,email,msg)

        ob.quit()
    return render_template('index_form.html',status=True)
if __name__=="__main__":
    app.run(debug=True,port=5001,host='0.0.0.0')

