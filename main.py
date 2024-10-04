from flask import Flask, render_template, url_for, redirect, request, flash
from werkzeug.utils import secure_filename
from forms import *
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from clusters import *
import smtplib

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["UPLOAD_FOLDER"] = "static/uploads"


@app.route("/", methods=["GET", "POST"])
def home():
    colors = [('#4b7cca', 24.96), ('#0350ae', 23.21), ('#2564ba', 14.12), ('#914c0a', 8.01), ('#c36a0b', 6.84), ('#5f6014', 6.16), ('#e4950c', 5.04), ('#f8be1f', 4.82), ('#2d3b13', 4.32), ('#828961', 2.52)]
    img_form = TemplateForm()
    contact_form = ContactForm()
    if img_form.validate_on_submit():
        num = img_form.num_colors.data
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path = url_for("static", filename=f"uploads/{filename}")
        return redirect(url_for("edit", path=path, number=num))
    if contact_form.validate_on_submit():
        connect = smtplib.SMTP(host="smtp.gmail.com", port=587)
        connect.starttls()
        connect.login(user=os.environ.get("USER_EMAIL"), password=os.environ.get("USER_PASS"))
        connect.sendmail(from_addr=os.environ.get("USER_EMAIL"),
                         to_addrs=os.environ.get("USER_EMAIL"),
                         msg=f"Subject:Contact from {contact_form.name.data}\n\n"
                             f"Name: {contact_form.name.data}\n"
                             f"Email: {contact_form.email.data}"
                             f"Phone: {contact_form.phone.data}"
                             f"Message: {contact_form.message.data}")
        flash("Message has been successfully sent")
        return redirect(url_for("home") + "#contact")
    return render_template("index.html", img_form=img_form, contact_form=contact_form, colors=colors)


@app.route("/result/<path:path>/<int:number>", methods=["GET", "POST"])
def edit(path, number):
    colors = get_clusters(path, number)
    img_form = TemplateForm()
    contact_form = ContactForm()
    if img_form.validate_on_submit():
        num = img_form.num_colors.data
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path = url_for("static", filename=f"uploads/{filename}")
        return redirect(url_for("edit", path=path, number=num))
    if contact_form.validate_on_submit():
        connect = smtplib.SMTP(host="smtp.gmail.com", port=587)
        connect.starttls()
        connect.login(user=os.environ.get("USER_EMAIL"), password=os.environ.get("USER_PASS"))
        connect.sendmail(from_addr=os.environ.get("USER_EMAIL"),
                         to_addrs=os.environ.get("USER_EMAIL"),
                         msg=f"Subject:Contact from {contact_form.name.data}\n\n"
                             f"Name: {contact_form.name.data}\n"
                             f"Email: {contact_form.email.data}"
                             f"Phone: {contact_form.phone.data}"
                             f"Message: {contact_form.message.data}")
        flash("Message has been successfully sent")
        return redirect(url_for("edit", path=path, number=number) + "#contact")
    return render_template("page.html", img_form=img_form, contact_form=contact_form, colors=colors, path=path)


if __name__ == "__main__":
    app.run(debug=True)
