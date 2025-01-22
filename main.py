from flask import Flask, render_template, url_for, request
import requests
import smtplib

my_email = "pranaymaheshwaram.cbit@gmail.com"
password = "qasstmbfzxntmspj"


posts = requests.get("https://api.npoint.io/5c286a5758868f55d059").json()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', all_posts = posts)

@app.route('/contact',  methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=my_email, password= password)
        message = f"Subject:New Contact Request!\n\nName: {name}\nmail:{email}\nphone:{phone}\nmessage: {message}"
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=message)
        return render_template("contact.html", msg_sent= True)
    return render_template('contact.html', msg_sent = False)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route('/form-entry', methods=["POST"])
def receive_data():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    print(name, email, phone, message)
    return f"<h1>MEssage SENT !!</h1>"


if __name__ == '__main__':
    app.run(debug=True)