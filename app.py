from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == 'True'
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def portfolio():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]

        msg = Message("Nuevo mensaje de portafolio",
                      recipients=[os.getenv("MAIL_USERNAME")])
        msg.body = f"Nombre: {nombre}\nEmail: {email}\nMensaje:\n{mensaje}"

        try:
            mail.send(msg)
            flash("Mensaje enviado correctamente.")
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")
            flash("Ocurrió un error. Intenta más tarde.")
        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

