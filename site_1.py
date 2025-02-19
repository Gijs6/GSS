from flask import Flask, render_template, request
from main import mainGSS

app = Flask(__name__)

@app.route("/GSS", methods=["GET", "POST"])
@app.route("/gss", methods=["GET", "POST"])
def gss():
    if request.method == "POST":
        htmlinput = request.form.get("htmlinput", "")
        cssinput = request.form.get("cssinput", "")

        cssfunctoutput = mainGSS(htmlinput, cssinput)

        return render_template("gss.html", cssresult=cssfunctoutput)
    else:
        return render_template("gss.html")




if __name__ == '__main__':
    app.run()
