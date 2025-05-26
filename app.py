
from flask import Flask,render_template,request
import pickle




#object for class
app=Flask(__name__)

with open("stroke-svc-model.pkl","rb")as file:
    stroke_model=pickle.load(file)

with open("lb-smoking.pkl","rb")as file:
    lb_smoke=pickle.load(file)
    


def predict_stroke(gender="Male",age=67.0,hypertension="Yes",heart_disease="Yes",avg_glucose_level=234.46,bmi=67.34,smoking_status="smokes",Residence_type="Rural"):
    lst=[]
    if gender=="Male":
        lst=lst+[1]
    elif gender=="Female":
        lst=lst+[0]
    elif gender=="Other":
        lst=lst+[2]

    lst=lst+[age]

    if hypertension=="Yes":
        lst=lst+[1]
    elif hypertension=="No":
        lst=lst+[0]

    if heart_disease=="Yes":
        lst=lst+[1]
    elif heart_disease=="No":
        lst=lst+[0]

    lst=lst+[avg_glucose_level,bmi]

    smoking_status=lb_smoke.transform([smoking_status])
    lst=lst+list(smoking_status)
    print(smoking_status)

    if Residence_type=="Urban":
        lst=lst+[0,1]
    elif Residence_type=="Rural":
        lst=lst+[1,0]


    result=stroke_model.predict([lst])
    print(result)
    if result==[1]:
        return "person is having stroke"
    else:
        return "person is not having stroke"


#routing
@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/contact",methods=["GET"])
def contact():
    return render_template("contact.html")


@app.route("/about",methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/predict",methods=["GET","POST"])
def predict():
    if request.method=="POST":
        gender=request.form.get("gender")
        age=float(request.form.get("age"))
        bmi=float(request.form.get("bmi"))
        hypertension=request.form.get("hypertension")
        heart_disease=request.form.get("heart_disease")
        avg_glucose_level=request.form.get("avg_glucose_level")
        smoking_status=request.form.get("smoking_status")
        residence_type=request.form.get("residence_type")

        result=predict_stroke(gender=gender,age=age,hypertension=hypertension,heart_disease=heart_disease,avg_glucose_level=avg_glucose_level,bmi=bmi,smoking_status=smoking_status,Residence_type=residence_type)
        print(result)
        return render_template("predict.html",prediction=result)
    return render_template("predict.html")
    









if __name__=="__main__":
    app.run(debug=True)