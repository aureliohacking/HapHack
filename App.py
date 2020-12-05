import os
from flask import Flask, render_template, request, Response
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

ruta = os.getcwd() + "/output/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nmap')
def nmap():
    return render_template('nmap.html')


@app.route('/nmap_back', methods=['POST'])
def nmap_back():
    if request.method == 'POST':
        direccion = request.form['direccion']

        os.system("nmap -O -oX - "+ direccion + ">" + ruta + direccion + ".xml")
        os.system("xsltproc "+ ruta + direccion + ".xml -o " + ruta + direccion + ".html")
        os.system("rm "+ ruta + direccion + ".xml")

        with open( ruta + direccion + '.html', "r") as f:
            content = f.read()
        return Response(content, mimetype='text/html')

@app.route('/blackWidow')
def blackWidow():
    return render_template('blackWidow.html')

@app.route('/blackWidow_back', methods=['POST'])
def blackWidow_back():
    if request.method == 'POST':
        direccion = request.form['direccion']

        os.system("blackwidow -d " + direccion + " > " + ruta + direccion + "_blackwidow" + ".txt")

        with open( ruta + direccion + '_blackwidow.txt', "r") as f:
            content = f.read()
        return Response(content, mimetype='text/plain')

@app.route('/a2sv')
def a2sv():
    return render_template('a2sv.html')

@app.route('/a2sv_back', methods=['POST'])
def a2sv_back():
    if request.method == 'POST':
        direccion = request.form['direccion']

        os.system("a2sv -t " + direccion + " > " + ruta + direccion + "_a2sv" + ".txt")
        with open( ruta + direccion + '_a2sv.txt', "r") as f:
            content = f.read()
        return Response(content, mimetype='text/plain')

@app.route('/informacion')
def informacion():
    return render_template('informacion.html')

@app.route('/informacion_back', methods=['POST'])
def informacion_back():
    if request.method == 'POST':
        direccion = request.form['direccion']

        os.system("whatweb -v -a 3 " + direccion + " > " + ruta + direccion + "_whatweb" + ".txt")
        os.system("sslscan " + direccion + " > " + ruta + direccion + "_sslscan" + ".txt")

        palabra = "WordPress"
        f = open(ruta + direccion + "_whatweb.txt")
        libro = f.read()
        n = libro.count(palabra)
        f.close()

        if n >= 1:
            os.system("wpscan --url " + direccion + " -o " + ruta + direccion + "_wordpress" + ".txt")

        palabra = "Joomla"
        f = open(ruta + direccion + "_whatweb.txt")
        libro = f.read()
        n = libro.count(palabra)
        f.close()

        if n >= 1:
            os.system("joomscan -u " + direccion + " > " + ruta + direccion + "_joomla" + ".txt")

        return 'entrar a la carpeta output para ver los 2 o 3 resultados'

@app.route('/freak')
def freak():
    return render_template('freak.html')

@app.route('/freak_back', methods=['POST'])
def freak_back():
    if request.method == 'POST':

        direccion = request.form['direccion']
        puerto = request.form['puerto']

        os.system("./check_freak.sh " + direccion + " " + puerto + " > " + ruta + direccion + "_freak" + ".txt")
        with open( ruta + direccion + '_freak.txt', "r") as f:
            content = f.read()
        return Response(content, mimetype = 'text/plain')

if __name__ == "__main__":
    app.run()