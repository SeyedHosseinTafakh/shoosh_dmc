from pydicom import dcmread
from flask import Flask , send_file , request, render_template, make_response, redirect , g , send_from_directory
from funs.funcs import *
import pydicom
import uuid
import os
from datetime import date
import jdatetime
from functools import wraps


app = Flask(__name__, template_folder="html")

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        my_cookie = request.cookies.get('id')
        if not my_cookie:
            return render_template("login.html")
        user = get_user_by_id(my_cookie)
        if len(user) == 0:
            return render_template("login.html")
        g.user = user[0]
        
        return f(*args, **kwargs)
    return decorator





# def show_dataset(ds, indent):
    # for elem in ds:
      # if elem.VR == "SQ":
    # indent += 4 * " "
    # for item in elem:
    # show_dataset(item, indent)
    # indent = indent[4:]
    # print(indent + str(elem))

# def print_dataset(file_name):
    # ds = dcmread(file_name)
    # show_dataset(ds, indent="")


# @app.route("/<path:filename>")
# def hello_world(filename):
   # path = "LIDC-IDRI-0001.json"
   # print(filename)
    # return {"hello":"world"}

# @app.route("/login")
# def log_in():
# @app.route('/login',methods = ['POST', 'GET'])
# def login():
    # if request.method == 'POST':
      # user = request.form['nm']
      # return redirect(url_for('success',name = user))
    # if request.method=="GET":
       # user = request.args.get('nm')
       # return render_template("login.html")
    # return {"hello":"worls"}
    

@app.route('/list',methods = [ 'GET'])
@token_required
def show_list():
    if request.method=="GET":
       requests = request.args.get("page_number")
       # TODO::// i have to add page numbers
       recs = get_records(0,20)
       #print(recs)
       print(request.args)
       return render_template("tables.html",result=recs)
@app.route('/upload_list',methods = [ 'GET', 'POST'])
@token_required
def show_upload_form():
    if request.method=="GET":
       return render_template("upload_form.html")
    if request.method=="POST":
        # print(request.data)
        # print(request.values.get("patient_name"))
        # print(request.values.get("patient_phone_number"))
        # print(request.values.get("more_text"))
        codes = get_code_by_phone_number(str(request.values.get("patient_phone_number")))
        print(codes)
        print(str(request.values.get("patient_phone_number")))
        if len(codes)<=0:
            # code = random_char()
            upload_code(request.values.get("patient_phone_number"))
        files = request.files.getlist("files")
        for each in range(len(files)):
            if files[each].content_type == "application/octet-stream":
                del(files[each])
        file_dir=""
        generated_uuid = str(uuid.uuid4())

        if len(files) > 0:
            generated_uuid = str(uuid.uuid4())
            os.makedirs('upload_dir/'+str(jdatetime.datetime.now().strftime('%Y-%m-%d'))+"/"+generated_uuid+"/")    
            file_dir = 'upload_dir/'+str(jdatetime.datetime.now().strftime('%Y-%m-%d'))+"/"+generated_uuid+"/"
            for each in files:
                if each.content_type =="application/octet-stream":
                    pass
                else:
                # # todo::// add error handeling
                    each.save(os.path.join('upload_dir/'+str(jdatetime.datetime.now().strftime('%Y-%m-%d'))+"/"+generated_uuid+"/",each.filename))
        insert_record(request.values.get("patient_name"),
                        request.values.get("patient_phone_number"),
                        request.values.get("more_text"),
                        file_dir+str(files),
                        generated_uuid,str(jdatetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        return render_template("upload_form.html")

@app.route('/login',methods = [ 'GET', 'POST'])
def sign_in():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        print(request.values.get("username"))
        print(request.values.get("password"))
        user_data = dblogin(request.values.get("username"),
                            request.values.get("password"))
        print(user_data)
        if len(user_data)>0:
            print("we have user")
        
            response = make_response(redirect("/list"))
            response.set_cookie("id",user_data[0]["uid"])
            return response
        else:
            error = "اطلاعات وارد شده اشتباه میباشد"
            return render_template("login.html",error = error)



# @app.route('/download/<path:filename>',methods = [ 'GET'])
# def download_files(filename):
    # return send_from_directory(directory='upload_dir/2023-05-14/01cbb620-1b76-451b-a7c4-d578b2b646a3', path=filename,as_attachment=True)

# todo :: search in list
# todo :: add patient recipt code


if __name__ == "__main__":
    #app = create_app()
    app.run(debug=True,port=2727)

