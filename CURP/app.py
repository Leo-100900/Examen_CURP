from flask import Flask, render_template, request, flash
import random
import string

app = Flask(__name__)
app.secret_key = 'tu_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    curp = None
    nombre = None
    apellido_paterno = None
    apellido_materno = None

    if request.method == 'POST':
        nombre = request.form['nombre'].upper()
        apellido_paterno = request.form['apellido_paterno'].upper()
        apellido_materno = request.form['apellido_materno'].upper()
        año = request.form['año']
        mes = request.form['mes']
        dia = request.form['dia']
        genero = request.form['genero']
        estado = request.form['estado']

        if not nombre.isupper() or not apellido_paterno.isupper() or not apellido_materno.isupper():
            flash("Los campos deben estar en mayúsculas.")
            return render_template('index.html', nombre=nombre, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno, curp=curp)

        # Generar CURP
        primera_letra_apellido_paterno = apellido_paterno[0]
        primera_vocal_apellido_paterno = next((c for c in apellido_paterno[1:] if c in 'AEIOU'), '')
        primera_letra_apellido_materno = apellido_materno[0]
        primera_letra_nombre = nombre[0]

        año_curp = año[-2:]  # Tomar los últimos dos dígitos del año
        mes_curp = mes
        dia_curp = dia

        # Género
        genero_curp = genero

        # Estado
        estado_curp = obtener_abreviatura_estado(estado)

        # Segunda consonante
        segunda_consonante_apellido_paterno = segunda_consonante(apellido_paterno)
        segunda_consonante_apellido_materno = segunda_consonante(apellido_materno)
        segunda_consonante_nombre = segunda_consonante(nombre)

        # Generar homoclave
        homoclave = generar_homoclave()

        curp = f"{primera_letra_apellido_paterno}{primera_vocal_apellido_paterno}{primera_letra_apellido_materno}{primera_letra_nombre}{año_curp}{mes_curp}{dia_curp}{genero_curp}{estado_curp}{segunda_consonante_apellido_paterno}{segunda_consonante_apellido_materno}{segunda_consonante_nombre}{homoclave}"

    return render_template('index.html', nombre=nombre, apellido_paterno=apellido_paterno, apellido_materno=apellido_materno, curp=curp)

def obtener_abreviatura_estado(estado):
    estados = {
        "AGUASCALIENTES": "AS",
        "BAJA CALIFORNIA": "BC",
        "BAJA CALIFORNIA SUR": "BS",
        "CAMPECHE": "CC",
        "COLIMA": "CM",
        "COAHUILA": "CL",
        "CHIAPAS": "CS",
        "CHIHUAHUA": "CH",
        "DURANGO": "DG",
        "GUANAJUATO": "GT",
        "GUERRERO": "GR",
        "HIDALGO": "HG",
        "JALISCO": "JC",
        "MÉXICO": "MC",
        "MICHOACÁN": "MN",
        "MORELOS": "MS",
        "NAYARIT": "NT",
        "NUEVO LEÓN": "NL",
        "OAXACA": "OC",
        "PUEBLA": "PL",
        "QUERÉTARO": "QT",
        "QUINTANA ROO": "QR",
        "SAN LUIS POTOSÍ": "SP"
    }
    return estados.get(estado, '')

def segunda_consonante(cadena):
    consonantes = [c for c in cadena if c not in 'AEIOU' and c.isalpha()]
    return consonantes[1] if len(consonantes) > 1 else ''  # Obtener la segunda consonante

def generar_homoclave():
    letra = random.choice(string.ascii_uppercase)  # Elige una letra aleatoria
    numero = random.randint(0, 9)  # Elige un número aleatorio
    return f"{letra}{numero}"

if __name__ == '__main__':
    app.run(debug=True)
