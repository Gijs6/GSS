from flask import Flask, render_template, request, redirect
from main import mainGSS

app = Flask(__name__)


@app.route("/GSS/result", methods=["GET", "POST"])
@app.route("/gss/result", methods=["GET", "POST"])
def gss_result():
    if request.method == "POST":
        htmlinput = request.form.get("htmlinput", "")
        cssinput = request.form.get("cssinput", "")

        cssfunctoutput = mainGSS(htmlinput, cssinput)

        return render_template("gss.html", cssresult=cssfunctoutput)
    else:
        return redirect("/gss")


@app.route("/GSS")
@app.route("/gss")
def gss():
    return render_template("gss.html")




if __name__ == '__main__':
    app.run()
