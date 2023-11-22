import os
import io

import pandas as pd
import pdfrw
from pdfrw import PdfName, PdfWriter, PdfReader
import copy
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, stock_portfolio, stock_history

# Configure application
app = Flask(__name__)
df =''
#pdf_template = "static/temp.pdf"
from pathlib import Path
THIS_FOLDER = Path(__file__).parent.resolve()
pdf_template = THIS_FOLDER / "static/temp.pdf"

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")

def index():
    """Show upload page by default"""

    return render_template(
        "upload.html"
    )
def ExtractAlphanumeric(InputString):
    from string import ascii_letters, digits
    return "".join([ch for ch in InputString if ch in (ascii_letters + digits)])

@app.route('/uploaded', methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        print(request.form['action'])
        if request.form['action'] == "upload":
            # FileStorage object wrapper
            f = request.files['file']
            data = f.read()
            filename = f.filename
            file_object = io.BytesIO(data)
            values = []
            vid = 0
            df = pd.read_excel(file_object, header=None)

            df.columns = df.columns.astype(str)
            df = df.rename(columns={"0": "id", "1": "function", "2": "name", "3":"title", "4":"company", "5": "desc", "6":"text" })
            #print(df)
            html_table = df.to_html(classes='table table-striped table-bordered table-hover', index=False, header=False, escape=False)


            html_table = html_table.replace('<th>', '<th style="border-bottom: 0;">')
            dict = df.to_dict(orient='records')
            #print(dict)

            ff = 4097
            #ff = 1


            ### field_names
            text_function = 'text_function'
            text_name = 'text_name'
            text_desc = 'text_desc'
            text_company = 'text_company'

            new_page=''
            values = dict
            i=0
            result=[]
            pdfs = pdfrw.PdfWriter()
            pdf_output = ''
            ppage = ''

            for value in values:
                pdf = pdfrw.PdfReader(pdf_template)
                page = pdf.pages[0]
                i = i + 1
                p = 0


                annotations = page['/Annots']
                for annotation in annotations:
                    if annotation['/Subtype']=='/Widget':
                        if not annotation['/T']:
                            annotation=annotation['/Parent']
                            #print (annotation)
                            if annotation['/T']:
                                #print(annotation['/T'])
                                #print(type(annotation['/T']))
                                key = annotation['/T'].strip('()')
                                mkey = ''.join(filter(lambda z: not z.isdigit(), key))

                                if mkey==text_function:
                                    annotation.update(pdfrw.PdfDict(V='{}'.format(value['function'].upper()),Ff=ff))
                                    annotation.update(pdfrw.PdfDict(T=(mkey+str(i))))
                                    print(value['function'])
                                if mkey==text_name:
                                    annotation.update(pdfrw.PdfDict(V='{}'.format(value['name']),Ff=ff))
                                    annotation.update(pdfrw.PdfDict(T=(mkey+str(i))))
                                    print(value['name'])
                                if mkey==text_desc:
                                    text = ''
                                    print(str(value['desc']))
                                    if pd.isnull(str(value['desc'])) or str(value['desc'])=='nan':
                                        text = str(value['text']) + "\n"
                                    else:
                                        text = str(value['text']) + "\n" + str(value['desc'])
                                    annotation.update(pdfrw.PdfDict(V='{}'.format(text),Ff=ff))
                                    annotation.update(pdfrw.PdfDict(T=(mkey+str(i))))
                    ppage = page


                result = pdfs.addpage(ppage)
                print(result)
            buf = io.BytesIO()
            result.write(buf)
            buf.seek(0)

            reopen = pdfrw.PdfReader(buf)

            reopen.Root.AcroForm = pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'))

            buf2 = io.BytesIO()
            pdfrw.PdfWriter().write(buf2, reopen)
            buf2.seek(0)
            print("sending file.......................")



            return send_file(buf2, as_attachment=True, download_name= str(filename) + ".pdf", mimetype='application/pdf')
        if request.form['action'] == "check":
            # FileStorage object wrapper
            f = request.files['file']
            data = f.read()
            filename = f.filename
            file_object = io.BytesIO(data)
            values = []
            vid = 0
            df = pd.read_excel(file_object, header=None)

            df.columns = df.columns.astype(str)
            df = df.rename(columns={"0": "id", "1": "function", "2": "name", "3":"title", "4":"company", "5": "desc", "6":"text" })
            #print(df)
            html_table = df.to_html(classes='table table-striped table-bordered table-hover', index=False, header=False, escape=False)


            html_table = html_table.replace('<th>', '<th style="border-bottom: 0;">')
            return render_template("table.html", table=html_table)





    else:
        return render_template("upload.html")


@app.route("/help")
def help():
    """Show help"""

    return render_template(
        "help.html"
    )




