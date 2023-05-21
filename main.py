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
        page_number = request.args.get("page_number")
        # print(page_number)
        if not(page_number) or int(page_number)==0:
            # print(page_number)
            page_number=1
        start = (int(page_number)*40)-40
        finish = int(page_number)*40
        # TODO::// i have to add page numbers
        rows_number = count_rows_record()[0]['counts']
        # numbers_of_pages = 0
        # print(rows_number)
        number_of_pages = int(rows_number/40)
        
        # if rows_number%10 == rows_number:
            # print("no page")
        # print(rows_number%40)
        recs = get_records(start,finish)
        #print(recs)
        # print(request.args)
        if request.args.get("select")=="p_name":
            input_text=request.args.get("input_text")
            recs = search_in_records_p_name(input_text,start,finish)
            # rows_number = count_search_in_records_p_name(input_text)[0]['counts']
            rows_number = count_search_in_records_p_name(input_text)
            if rows_number:
                rows_number=rows_number[0]['counts']
        elif request.args.get("select")=="p_phone_number":
            input_text=request.args.get("input_text")
            recs = search_in_records_phone_number(input_text,start,finish)
            rows_number = count_search_in_records_phone_number(input_text)
            if rows_number:
                rows_number=rows_number[0]['counts']

        elif request.args.get("select")=="code":
            input_text=request.args.get("input_text")
            recived_code = search_in_code(input_text)
            # print(recived_code)
            if len(recived_code)>0:
                # print(recived_code)
                p_phone_number = recived_code[0]["p_phone_number"]
                # print(p_phone_number)
                recs = search_in_records_phone_number(p_phone_number,start,finish)
                rows_number = count_search_in_records_phone_number(p_phone_number)[0]['counts']
                # print(count_search_in_records_phone_number(p_phone_number))
                # print(recs)
        number_of_pages = int(int(rows_number)/40)
        # print(recs)
        for each in recs:
            # print(each['p_phone_number'])
            # print(get_code_by_phone_number(each['p_phone_number'])[0]['p_access_code'])
            # print(get_code_by_phone_number(each['p_phone_number']))
            each['p_access_code']=get_code_by_phone_number(each['p_phone_number'])[0]['p_access_code']
            # print(each)
        print(recs)
        return render_template("tables.html",result=recs,number_of_pages=range(0,number_of_pages))
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
        # print(codes)
        # print(str(request.values.get("patient_phone_number")))
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
        # for every in range(0,40):
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

from glob import glob
from io import BytesIO
from zipfile import ZipFile
import os

@app.route('/download/<jdate>/<uuid>',methods = [ 'GET'])
def download_files(jdate, uuid):
    target = "upload_dir/"+jdate+"/"+uuid
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for file in glob(os.path.join(target, '*.dcm')):
            zf.write(file, os.path.basename(file))
    stream.seek(0)
    return send_file(
        stream,
        as_attachment=True,
        download_name='uuid.zip'
    )
    # return {"h":"s"}
# todo :: search in list
# todo :: add patient recipt code


@app.route('/plist',methods = ["POST", 'GET'])
def patient_records():
    if request.method=="GET":
        return render_template("add_code.html")
    if request.method=="POST":
        input_text=request.values.get("code")
        return redirect("/p_list?code="+input_text)
        # page_number = request.args.get("page_number")

        # print(request.values)
        # input_text=request.values.get("code")
        # recived_code = search_in_code(input_text)
        # if not(page_number) or int(page_number)==0:
            # print(page_number)
            # page_number=1
        # start = (int(page_number)*40)-40
        # finish = int(page_number)*40
        # if len(recived_code)>0:
            # p_phone_number = recived_code[0]["p_phone_number"]
            # recs = search_in_records_phone_number(p_phone_number,start,finish)
            # rows_number = count_search_in_records_phone_number(p_phone_number)[0]['counts']
            # number_of_pages = int(int(rows_number)/40)
    # return render_template("tables.html",result=recs,number_of_pages=range(0,number_of_pages))
            # print(number_of_pages)
            # print(recs)
            # start = (int(page_number)*40)-40
            # finish = int(page_number)*40
            # return render_template("ptables.html",result=recs,number_of_pages=range(0,number_of_pages))
        # else:
            # error="کد وارد شده در سیستم موجود نمیباشد"
            # print(error)
        # return render_template("add_code.html",error=error)


@app.route('/p_list',methods = [ 'GET'])
def patient_records_get():
    page_number = request.args.get("page_number")

    # print(request.values)
    input_text=request.args.get("code")
    recived_code = search_in_code(input_text)
    if not(page_number) or int(page_number)==0:
        # print(page_number)
        page_number=1
    start = (int(page_number)*40)-40
    finish = int(page_number)*40
    if len(recived_code)>0:
        p_phone_number = recived_code[0]["p_phone_number"]
        recs = search_in_records_phone_number(p_phone_number,start,finish)
        rows_number = count_search_in_records_phone_number(p_phone_number)[0]['counts']
        number_of_pages = int(int(rows_number)/40)
# return render_template("tables.html",result=recs,number_of_pages=range(0,number_of_pages))
        # print(number_of_pages)
        # print(recs)
        # start = (int(page_number)*40)-40
        # finish = int(page_number)*40
        return render_template("ptables.html",result=recs,number_of_pages=range(0,number_of_pages))
    else:
        error="کد وارد شده در سیستم موجود نمیباشد"
        print(error)
        return render_template("add_code.html",error=error)


@app.route('/help',methods = [ 'GET'])
def help():
    return render_template("help.html")
    
@app.route("/testlist", methods=["GET"])
def testlist():
    return render_template("demo_teables.html")



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    #app = create_app()
    app.run(debug=True,port=2727)

