from flask import Flask,render_template,request

app=Flask(__name__)

@app.route("/")
def index():
    titulo="IDGS80111111"
    lista=["Pedro","Luis","Maico"]
    return render_template("index.html", titulo=titulo, lista=lista)

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

# @app.route("/operas")
# def operas():
#     return '''
#  <form action="">
#         <label for="">Name</label>
#         <input type="text" id="name" name="name" required>

#         <label for="">APaterno</label>
#         <input type="text" id="APaterno" name="APaterno" required>
#     </form>
        #    '''
# @app.route("/OperasBas")
# def operas():
#     return render_template("OperasBas.html")7

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


if __name__ == "__main__":
    app.run(debug=True, port=3000)