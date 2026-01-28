from flask import Flask,render_template,request,redirect,url_for,session

from werkzeug.utils import secure_filename
import pymysql
from MyLib import *
import time
import os
app = Flask(__name__)
app.secret_key='my secret key'
app.config['UPLOAD_FOLDER']='./static/photos'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        medname = request.form['T1']
        cur = create_connection()

        # ✅ Safe query using parameterized SQL
        sql = "SELECT * FROM medical_medicine WHERE medicine_name LIKE '%"+medname+"%'"
        cur.execute(sql)
        n=cur.rowcount
    
        if n>0:
            data = cur.fetchall()
            return render_template('welcome.html', data=data, mname=medname, msg=None)
        else:
            return render_template('welcome.html', msg="No medicine found", mname=medname)
    else:
        # ✅ Always define all template variables
        return render_template('welcome.html', data=None, mname="", msg=None)



@app.route('/login',methods=['GET','POST'])
def login():
    print("Welcome to login")
    if request.method == 'POST':
        email = request.form['T1']
        password = request.form['T2']
        cur=create_connection()
        sql="select * from logindata where email='"+email+"' and password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            data=cur.fetchone()
            ut=data[2] #fetch usertype from index 2
            #create session
            session["email"]=email
            session["usertype"]=ut
            #goto page
            if(ut=="admin"):
                return redirect(url_for('admin_home'))
            elif(ut=="medical"):
                return redirect(url_for('medical_home'))
            else:
                return render_template('login.html',msg="Contact to admin")
        else:
            return render_template('login.html',msg="Either email or password is incorrect")
    else:
        return render_template('login.html')

@app.route('/auth_error')
def auth_error():
    return render_template('auth_error.html')

@app.route('/admin_profile',methods=['GET','POST'])
def admin_profile():
    # check the session
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "admin"):
            if(request.method == "POST"):
                cur=create_connection()
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                sql="update admindata set name='"+name+"', address='"+address+"', contact='"+contact+"' where email='"+e1+"'"
                cur.execute(sql)
                n = cur.rowcount
                if(n==1):
                    return render_template('admin_profile.html',msg="Saved")
                else:
                    return render_template('admin_profile.html',msg="Not Saved")
            else:
                cur=create_connection()
                sql="select * from admindata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template('admin_profile.html',data=data)
                else:
                    return render_template('admin_profile.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/medical_profile',methods=['GET','POST'])
def medical_profile():
    # check the session
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "medical"):
            if(request.method == "POST"):
                cur=create_connection()
                medical_name=request.form['T1']
                owner_name=request.form['T2']
                address=request.form['T3']
                contact=request.form['T4']
                licence_no=request.form['T5']
                sql="update medicaldata set medical_name='"+medical_name+"',owner_name='"+owner_name+"',address='"+address+"',contact='"+contact+"',licence_no='"+licence_no+"' where email='"+e1+"'"

                cur.execute(sql)
                n = cur.rowcount
                if(n==1):
                    return render_template('medical_profile.html',msg="Saved")
                else:
                    return render_template('medical_profile.html',msg="Not Saved")
            else:
                cur=create_connection()
                sql="select * from medicaldata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template('medical_profile.html',data=data)
                else:
                    return render_template('medical_profile.html',msg="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/admin_home')
def admin_home():
    #check the session
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if ut=="admin":
            data=admin_data(e1)
            photo=check_photo(e1)
            if(data==None):
                return render_template('admin_home.html',msg="No data found")
            else:
                return render_template('admin_home.html',photo=photo,data=data)

        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/medical_home')
def medical_home():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        photo = check_photo(e1)
        if ut=="medical":
            data=medical_data(e1)
            if(data==None):
                return render_template('medical_home.html',msg="No data found")
            else:
                return render_template('medical_home.html',photo=photo,data=data)

        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/adminphoto')
def adminphoto():
    return render_template('uploadAdminPhoto.html')

@app.route('/adminphoto1',methods=['GET','POST'])
def adminphoto1():
    if'usertype' in session:
        ut=session["usertype"]
        email=session["email"]
        if ut=="admin":
            if request.method == "POST":
                file=request.files['F1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cur=create_connection()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('uploadAdminPhoto1.html',result="success")
                        else:
                            return render_template('uploadAdminPhoto1.html',result="No failure")
                    except :
                        return render_template('uploadAdminPhoto1.html',result="duplicate")
            else:
                return render_template('uploadAdminPhoto.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/change_adminphoto')
def change_adminphoto():
    if 'usertype' in session:
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            photo=check_photo(email)
            cur=create_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                os.remove("./static/photos/"+photo)
                return render_template('ChangeAdminPhoto.html',data="success")
            else:
                return render_template('ChangeAdminPhoto.html',data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/medicalphoto')
def medicalphoto():
    return render_template('uploadMedicalPhoto.html')


@app.route('/medicalphoto1',methods=['GET','POST'])
def medicalphoto1():
    if'usertype' in session:
        ut=session["usertype"]
        email=session["email"]
        if ut=="medical":
            if request.method == "POST":
                file=request.files['F1']
                if file:
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cur=create_connection()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('uploadMedicalPhoto1.html',result="success")
                        else:
                            return render_template('uploadMedicalPhoto1.html',result="No failure")
                    except :
                        return render_template('uploadMedicalPhoto1.html',result="duplicate")
            else:
                return render_template('uploadMedicalPhoto.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/change_medicalphoto')
def change_medicalphoto():
    if 'usertype' in session:
        ut=session["usertype"]
        email=session["email"]
        if(ut=="medical"):
            photo=check_photo(email)
            cur=create_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n = cur.rowcount
            if n > 0:
                os.remove("./static/photos/"+photo)
                return render_template('ChangeMedicalPhoto.html',data="success")
            else:
                return render_template('ChangeMedicalPhoto.html',data="failure")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/logout')
def logout():
    if "email" in session or "usertype" in session:
        session.pop("email")
        session.pop("usertype")
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/change_pass_admin',methods=['GET','POST'])
def change_pass_admin():
    # check the session
    if "email" in session:
        ut = session["usertype"]
        if (ut == "admin"):
            if request.method == 'POST':
                old_password = request.form['T1']
                new_password = request.form['T2']
                email = session["email"]
                cur = create_connection()
                sql = "update logindata set password='" + new_password + "' where email='" + email + "'and password='" + old_password + "'"
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    msg = "Password changed successfully"
                    return render_template('change_pass_admin.html', msg=msg)
                else:
                    msg = "Incorrect old password"
                    return render_template('change_pass_admin.html', msg=msg)
            else:
                return render_template('change_pass_admin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/change_pass_medical',methods=['GET','POST'])
def change_pass_medical():
    if "email" in session:
        ut = session["usertype"]
        if (ut == "medical"):
            if request.method == 'POST':
                old_password = request.form['T1']
                new_password = request.form['T2']
                email = session["email"]
                cur = create_connection()
                sql="update logindata set password='"+new_password+"' where email='"+email+"'and password='"+old_password+"'"
                cur.execute(sql)
                n = cur.rowcount
                if (n == 1):
                    msg = "Password changed successfully"
                    return render_template('change_pass_medical.html', msg=msg)

                else:
                    msg = "Incorrect old password"
                    return render_template('change_pass_medical.html', msg=msg)
            else:
                return render_template('change_pass_medical.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/admin_reg',methods=['GET','POST'])
def admin_reg():
    if request.method == 'POST':
        print("This is post request")
        #receive form data
        name=request.form['T1']
        address=request.form['T2']
        contact = request.form['T3']
        email = request.form['T4']
        password=request.form['T5']
        confirm = request.form['T6']
        usertype="admin"
        cur = create_connection()
        s1="insert into admindata values('"+name+"','"+address+"','"+contact+"','"+email+"')"
        s2="insert into logindata values('"+email+"','"+password+"','"+usertype+"')"
        msg=""
        try:
            cur.execute(s1)
            n1=cur.rowcount
            cur.execute(s2)
            n2 = cur.rowcount
            cur.rowcount
            if (n1==1 and n2==1):
                msg="data saved and login created"
            elif(n1==1):
                msg="only data is saved"
            elif(n2==1):
                msg="only login is created"
            else:
                msg="Already registered,use other email"
        except pymysql.err.IntegrityError:
            msg="already registered,use other email"
        return render_template('AdminReg.html',project=msg)
    else:
        return render_template('AdminReg.html')

@app.route("/show_admins")
def show_admins():
    cur = create_connection()
    sql="select * from admindata"
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        data=cur.fetchall()
        return render_template('Admins.html',project=data)
    else:
        msg="no data found"
        return render_template('Admins.html',msg=msg)


@app.route("/medical_reg",methods=['GET','POST'])
def medical_reg():
    if "email" in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="admin"):
            if (request.method == 'POST'):
                print("This is POST request")
                # receive form data
                medical_name = request.form['T1']
                owner_name = request.form['T2']
                address = request.form['T3']
                contact = request.form['T4']
                licence_no = request.form['T5']
                email = request.form['T6']
                password = request.form['T7']
                confirm = request.form['T8']
                usertype = "medical"
                cur = create_connection()
                s1 = "insert into medicaldata values('" + medical_name + "','" + owner_name + "','" + address + "','" + contact + "','" + licence_no + "','" + email + "')"
                s2 = "insert into logindata values('" + email + "','" + password + "','" + usertype + "')"
                try:
                    cur.execute(s1)
                    n1 = cur.rowcount
                    cur.execute(s2)
                    n2 = cur.rowcount
                    if (n1 == 1 and n2 == 1):
                        msg = "data saved and login created"
                    elif (n1 == 1):
                        msg = "only data is saved"
                    elif (n2 == 1):
                        msg = "only login is created"
                    else:
                        msg = "no data saved and no login created"
                except pymysql.err.IntegrityError:
                    msg = "already registered,use other email"
                return render_template('medicaladmin.html', project=msg)
            else:
                return render_template('medicaladmin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route ("/show_medical")
def show_medical():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "admin"):
            cur = create_connection()
            sql = "select * from medicaldata"
            cur.execute(sql)
            n = cur.rowcount
            if (n > 0):
                data = cur.fetchall()
                return render_template('medical_admin2.html', project=data)
            else:
                msg = "no data found"
                return render_template('medical_admin2.html', msg=msg)

        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route ("/show_stores")
def show_stores():
    cur = create_connection()
    sql = "select * from medicaldata"
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        data=cur.fetchall()
        return render_template('medicalstores.html',project=data)
    else:
        msg="no data found"
        return render_template('medicalstores.html',msg=msg)

@app.route("/edit_medical",methods=['GET','POST'])
def edit_medical():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "admin"):
            if (request.method == 'POST'):
                email = request.form['H1']
                cur = create_connection()
                sql = "select * from medicaldata where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if (n > 0):
                    data = cur.fetchone()
                    return render_template('EditMedical.html', project=data)
                else:
                    return render_template('EditMedical.html', msg="no data found")
            else:
                return redirect(url_for('show_medical'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route("/edit_medical1",methods=['GET','POST'])
def edit_medical1():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "admin"):
            if (request.method == 'POST'):
                medical_name = request.form['T1']
                owner_name = request.form['T2']
                address = request.form['T3']
                contact = request.form['T4']
                licence_no = request.form['T5']
                email = request.form['T6']
                cur = create_connection()
                sql = "update medicaldata set medical_name='" + medical_name + "',owner_name='" + owner_name + "',address='" + address + "',contact='" + contact + "',licence_no='" + licence_no + "'where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if (n > 0):
                    return render_template("EditMedical1.html", msg="data saved")
                else:
                    return render_template('EditMedical1.html', msg="no data found")
            else:
                return redirect(url_for('show_medical'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route("/delete_medical",methods=['GET','POST'])
def delete_medical():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "admin"):
            if (request.method == 'POST'):
                email = request.form['T1']
                cur = create_connection()
                sql = "select * from medicaldata where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if (n > 0):
                    data = cur.fetchone()
                    return render_template('DeleteMedical.html', project=data)
                else:
                    return render_template('DeleteMedical.html', msg="no data found")
            else:
                return redirect(url_for('show_medical'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route("/delete_medical1",methods=['GET','POST'])
def delete_medical1():
    if "email" in session:
        ut = session["usertype"]
        e1 = session["email"]
        if (ut == "admin"):
            if (request.method == 'POST'):
                email = request.form['T1']
                cur=create_connection()
                sql1 = "delete  from medicaldata where email='" + email + "'"
                sql2 = "delete from logindata where email='" + email + "'"
                cur.execute(sql1)
                cur.execute(sql2)
                n1 = cur.rowcount
                n2 = cur.rowcount
                if (n1 == 1 and n2 == 1):
                    return render_template('DeleteMedical1.html', msg="data deleted")
                else:
                    return render_template('DeleteMedical1.html', msg="no data found")
            else:
                return redirect(url_for('show_medical'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route("/medicine_reg",methods=['GET','POST'])
def medicine_reg():
    if(request.method == 'POST'):

        #recieve from data
        medicine_name = request.form['T1']
        medicine_type = request.form['T2']
        company_name = request.form['T3']
        unit_price = request.form['T4']
        description = request.form['T5']
        med_id = request.form['T6']

        e1 = session["email"]



        cur=create_connection()
        s1="insert into medicinedata values('"+med_id+"','"+medicine_name+"','"+medicine_type+"','"+company_name+"','"+unit_price+"','"+description+"','"+e1+"')"

        try:
            cur.execute(s1)
            n=cur.rowcount
            if(n>0):
                msg="data saved"
            else:
                msg="no data saved"
        except pymysql.err.IntegrityError:
            msg="data already exist"
        return render_template('medicine_reg.html',msg=msg)
    else:

        return render_template('medicine_reg.html')

@app.route("/show_medicine")
def show_medicine():
    if "email"in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            cur=create_connection()
            sql="select * from medicinedata where medical_email='"+e1+"'"
            cur.execute(sql)
            n = cur.rowcount
            if (n>0):
                data = cur.fetchall()
                return render_template('show_medicine.html',project=data)
            else:
                msg="no data found"
                return render_template('show_medicine.html',msg=msg)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route("/edit_medicine",methods=['GET','POST'])
def edit_medicine():
    if "email"in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            if(request.method == 'POST'):
                med_id=request.form['M1']
                cur=create_connection()

                sql = "SELECT med_id, medicine_name, medicine_type, company_name, unit_price, description, medical_email FROM medicinedata WHERE med_id='" + med_id + "'"
                cur.execute(sql)
                n = cur.rowcount
                if (n>0):
                    data = cur.fetchone()
                    return render_template('edit_medicine.html',project=data)
                else:
                    return render_template('edit_medicine.html',msg="no data found")
            else:
                return redirect(url_for('show_medicine'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))


@app.route("/edit_medicine1",methods=['GET','POST'])
def edit_medicine1():
    if "email"in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            if(request.method == 'POST'):

                # recieve from data
                medicine_name = request.form['T1']
                medicine_type = request.form['T2']
                company_name = request.form['T3']
                unit_price = request.form['T4']
                description = request.form['T5']
                med_id = request.form['T6']
                cur=create_connection()
                sql = "UPDATE medicinedata SET medicine_name='" + medicine_name + "', medicine_type='" + medicine_type + "', company_name='" + company_name + "', unit_price='" + unit_price + "', description='" + description + "' WHERE med_id='" + med_id + "'"

                cur.execute(sql)
                n=cur.rowcount
                if (n>0):
                    return render_template("edit_medicine1.html",msg="data saved")
                else:
                    return render_template('edit_medicine1.html',msg="no data found")
            else:
                return redirect(url_for('show_medicine'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))



@app.route("/delete_medicine",methods=['GET','POST'])
def delete_medicine():
    if "email"in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            if(request.method == 'POST'):
                med_id = request.form['D1']
                cur=create_connection()
                sql = "select * from medicinedata where med_id='"+med_id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if (n>0):
                    data = cur.fetchone()
                    return render_template('delete_medicine.html',project=data)
                else:
                    return render_template('delete_medicine.html',msg="no data found")
            else:
                return redirect(url_for('show_medicine'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route("/delete_medicine1",methods=['GET','POST'])
def delete_medicine1():
    if "email"in session:
        ut=session["usertype"]
        e1=session["email"]
        if(ut=="medical"):
            if(request.method == 'POST'):
                med_id = request.form['D1']
                cur=create_connection()
                sql="delete from medicinedata where med_id='"+med_id+"'"
                cur.execute(sql)
                n = cur.rowcount
                if (n>0):
                    return render_template('delete_medicine1.html',msg="data deleted")
                else:
                    return render_template('delete_medicine1.html',msg="no data found")
            else:
                return redirect(url_for('show_medicine'))
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

if __name__ == '__main__':
    app.run(debug=True)