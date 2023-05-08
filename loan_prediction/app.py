# save this as app.py
from flask import Flask, escape, request, render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if  (request.form['gender']=="Male"):
            Gender=1
        else:
            Gender=0
        if request.form['married']=="Yes":
            Married=1
        else:
            Married=0
        if (request.form['dependents']=="3+"):
            Dependents =3
        elif (request.form['dependents']=="2"):
            Dependents =2
        elif (request.form['dependents'] == "1"):
            Dependents = 1
        else:
            Dependents=0

        if request.form['education']=="Gratuate":
            Education=1
        else:
            Education=0

        if request.form['employed']=="Yes":
            Self_Employed =1
        else:
            Self_Employed =0
        Credit_History = float(request.form['credit'])
        if request.form['area']=="Semiurban":
            Property_Area=1
        elif request.form['area']=="Urban":
            Property_Area=2
        else:
            Property_Area=0

        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])


        ApplicantIncomelog = np.log(ApplicantIncome)
        totalincomelog = np.log(ApplicantIncome + CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)
        pred=model.predict([[Gender,Married,Dependents,Education,Self_Employed,Credit_History,Property_Area,
                             ApplicantIncome,CoapplicantIncome,LoanAmount, Loan_Amount_Term]])
        #pred=np.argmax(pred, axis=-1)
        if pred==0:
            prediction = "No"
        elif pred==1:
            prediction = "Yes"





        return render_template("prediction.html", prediction_text="Loan status is {}".format(prediction))




    else:
        return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=True)