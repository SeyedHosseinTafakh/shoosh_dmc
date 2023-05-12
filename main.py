from pydicom import dcmread
from flask import Flask , send_file , request,render_template
from funs.funcs import *
import pydicom
import uuid
import os
app = Flask(__name__, template_folder="html")


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


@app.route("/<path:filename>")
def hello_world(filename):
#    path = "LIDC-IDRI-0001.json"
#    print(filename)
    return {"hello":"world"}

# @app.route("/login")
# def log_in():
@app.route('/login',methods = ['POST', 'GET'])
def login():
    # if request.method == 'POST':
      #user = request.form['nm']
      # return redirect(url_for('success',name = user))
    if request.method=="GET":
       user = request.args.get('nm')
       return render_template("login.html")
    return {"hello":"worls"}
    

@app.route('/list',methods = [ 'GET'])
def show_list():
    if request.method=="GET":
       requests = request.args.get("page_number")
       # TODO::// i have to add page numbers
       recs = get_records(0,20)
       print(recs)
       return render_template("tables.html",result=recs)
@app.route('/upload_list',methods = [ 'GET', 'POST'])
def show_upload_form():
    if request.method=="GET":
       return render_template("upload_form.html")
    if request.method=="POST":
        print(request.data)
        print(request.values.get("patient_name"))
        print(request.values.get("patient_phone_number"))
        files = request.files.getlist("files")
        for each in files:
            each.save(os.path.join('upload_dir',each.filename))
            print(each.name)
        print(files)
        return render_template("upload_form.html")
if __name__ == "__main__":
    #app = create_app()
    app.run(debug=True,port=2727)
