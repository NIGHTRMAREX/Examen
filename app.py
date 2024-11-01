from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Patrón para cada parte de la CURP
patrones = {
    "primer_apellido": r"^[A-Z]$",
    "vocal_interna": r"^[AEIOU]$",
    "segundo_apellido": r"^[A-Z]$",
    "primer_nombre": r"^[A-Z]$",
    "anio_nacimiento": r"^\d{2}$",
    "mes_nacimiento": r"^(0[1-9]|1[0-2])$",
    "dia_nacimiento": r"^(0[1-9]|[12]\d|3[01])$",
    "sexo": r"^[HM]$",
    "estado": r"^[A-Z]{2}$",
    "consonante1": r"^[A-Z]$",
    "consonante2": r"^[A-Z]$",
    "consonante3": r"^[A-Z]$",
    "renapo": r"^[A-Z\d]{2}$"
}

# Función para realizar el análisis de tokens y detectar errores
def analizar_curp(curp):
    tokens = [
        {"Token": curp[0], "Tipo": "Primera letra del primer apellido", "Patrón": patrones["primer_apellido"]},
        {"Token": curp[1], "Tipo": "Primera vocal interna del primer apellido", "Patrón": patrones["vocal_interna"]},
        {"Token": curp[2], "Tipo": "Primera letra del segundo apellido", "Patrón": patrones["segundo_apellido"]},
        {"Token": curp[3], "Tipo": "Primera letra del primer nombre", "Patrón": patrones["primer_nombre"]},
        {"Token": curp[4:6], "Tipo": "Últimos dos dígitos del año de nacimiento", "Patrón": patrones["anio_nacimiento"]},
        {"Token": curp[6:8], "Tipo": "Mes de nacimiento", "Patrón": patrones["mes_nacimiento"]},
        {"Token": curp[8:10], "Tipo": "Día de nacimiento", "Patrón": patrones["dia_nacimiento"]},
        {"Token": curp[10], "Tipo": "Sexo", "Patrón": patrones["sexo"]},
        {"Token": curp[11:13], "Tipo": "Estado de nacimiento", "Patrón": patrones["estado"]},
        {"Token": curp[13], "Tipo": "Primera consonante interna del primer apellido", "Patrón": patrones["consonante1"]},
        {"Token": curp[14], "Tipo": "Primera consonante interna del segundo apellido", "Patrón": patrones["consonante2"]},
        {"Token": curp[15], "Tipo": "Primera consonante interna del primer nombre", "Patrón": patrones["consonante3"]},
        {"Token": curp[16:18], "Tipo": "RENAPO", "Patrón": patrones["renapo"]},
    ]

    errores = []
    for token in tokens:
        if not re.match(token["Patrón"], token["Token"]):
            errores.append(f"Error en {token['Tipo']}: '{token['Token']}' no es válido.")

    return tokens, errores

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        curp = request.form['curp'].upper()
        if len(curp) != 18:
            return render_template('index.html', error="La CURP debe tener exactamente 18 caracteres.")

        tokens, errores = analizar_curp(curp)
        if errores:
            return render_template('index.html', tokens=tokens, errores=errores)
        else:
            return render_template('index.html', tokens=tokens)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
