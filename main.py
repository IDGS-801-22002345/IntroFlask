from datetime import datetime 
from flask import Flask,render_template,request
from flask import g
from flask_wtf.csrf import CSRFProtect
from flask import flash
import forms 

app=Flask(__name__)
app.secret_key="esta es una clave secreta"
csr=CSRFProtect()

@app.errorhandler(404)
def page_notfound(e):
    return render_template("404.html"), 404

@app.before_request
def before_request():
    g.user= "Mario"
    print("beforer1")

@app.after_request
def after_request(response):
    print("afterr1")
    return response

@app.route("/")
def index():
    nom= 'None'
    titulo="IDGS80111111"
    lista=["Pedro","Luis","Maico"]
    nom=g.user
    print('Entro index {}'.format(g.user))
    return render_template("index.html", titulo=titulo, lista=lista, nom=nom)

@app.route("/ejemplo1")
def ejemplo1():
    return render_template("ejemplo1.html")

@app.route("/ejemplo2")
def ejemplo2():
    return render_template("ejemplo2.html")

@app.route("/hola")
def hola():
    return "<h1>Hola, Mundo!</h1>"

@app.route("/user/<string:user>")
def user(user):
    return f"<h1>Hola, {user}!</h1>"

@app.route("/numero/<int:numero>")
def number(numero):
    return f"<h1>El numero es {numero}!</h1>"

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return f"<h1>Hola, {username}! Tu ID es: {id}</h1>"

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1,n2):
    return f"<h1>La suma es: {n1+n2}</h1>"

@app.route("/default/")
@app.route("/default/<string:param>")
def func(param="juan"):
    return f"<h1>Hola, {param}</h1>"


@app.route("/Cinepolis", methods=["GET", "POST"])
def menu():
    if request.method == "POST":
        name = request.form.get("name")
        num_personas = int(request.form.get("numPersonas"))
        tarjeta_cineco = request.form.get("pago")
        num_boletos = int(request.form.get("numBoletos"))

        max_boletos = num_personas * 7
        if num_boletos > max_boletos:
            error = f"No puedes comprar más de {max_boletos} boletos."
            return render_template(
                "Cinepolis.html",
                error=error,
                name=name,
                numPersonas=num_personas,
                pago=tarjeta_cineco,
                numBoletos=num_boletos,
            )

        precio_boleto = 12 

        total_pagar = num_boletos * precio_boleto

        if num_boletos > 5:
            descuento = total_pagar * 0.15  
        elif num_boletos >= 3 and num_boletos <= 5:
            descuento = total_pagar * 0.10 
        else:
            descuento = 0  

        total_pagar -= descuento

        if tarjeta_cineco == "1": 
            total_pagar *= 0.9 

        return render_template("Cinepolis.html", total_pagar=total_pagar)

    return render_template("Cinepolis.html")


@app.route("/OperasBas", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        n1 = float(request.form.get("n1"))
        n2 = float(request.form.get("n2"))
        operacion = int(request.form.get("operacion"))

        if operacion == 1:
            resultado = n1 + n2
            operacion_texto = "suma"
        elif operacion == 2:
            resultado = n1 - n2
            operacion_texto = "resta"
        elif operacion == 3:
            resultado = n1 * n2
            operacion_texto = "multiplicación"
        elif operacion == 4:
            if n2 == 0:
                return "Error: No se puede dividir entre cero."
            resultado = n1 / n2
            operacion_texto = "división"
        else:
            return "Error: Operación no válida."

        return render_template("OperasBas.html", n1=n1, n2=n2, resultado=resultado, operacion_texto=operacion_texto)

    return render_template("OperasBas.html")


@app.route("/Zodiaco", methods=["GET", "POST"])
def zodiaco():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido_paterno = request.form.get("apellido_paterno")
        apellido_materno = request.form.get("apellido_materno")
        dia = int(request.form.get("dia"))
        mes = int(request.form.get("mes"))
        anio = int(request.form.get("anio"))
        sexo = request.form.get("sexo")

        edad = datetime.now().year - anio
        signo = obtener_signo_zodiaco_chino(anio)

        return render_template("zodiacoChino.html", nombre=nombre, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno, edad=edad, signo=signo, sexo=sexo)
    return render_template("zodiacoChino.html")

def obtener_signo_zodiaco_chino(anio):
    signos = ["Mono", "Gallo", "Perro", "Cerdo", "Rata", "Buey", "Tigre", "Conejo", "Dragon", "Serpiente", "Caballo", "Cabra"]
    indice = (anio % 12)
    return signos[indice]


@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    mat=0
    nom=''
    ape=''
    email=''
    alummo_clas=forms.UserForm(request.form)
    if request.method == 'POST' and alummo_clas.validate():
        mat=alummo_clas.matricula.data
        nom=alummo_clas.nombre.data
        ape=alummo_clas.apellido.data
        email=alummo_clas.correo.data
        mensaje='Bienvendio {}'.format(nom)
        flash(mensaje)
    return render_template("alumnos.html", form=alummo_clas,mat=mat,nom=nom,ape=ape,email=email)


if __name__ == "__main__":
    csr.init_app(app)
    app.run(debug=True, port=3000)