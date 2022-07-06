from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

#przydatne funkcje
def suma_aryt(n,a1,r):
    suma = ((2*a1 +(n-1)*r)/2)*n
    return suma

def suma_geo(n, a1, q):
    if q == 1:
        suma = a1*n
    else:
        suma = a1 * (1- q**n) / (1- q)
    return suma

def suma_dow(wzor, n):
    suma = 0
    while n >= 1:
        suma = nty_dow(wzor, n) + suma
        n -= 1
    return suma

def nty_aryt(n, a1, r):
    return a1 + (n-1) *r

def nty_geo(n, a1, q):
    return a1 * q**(n-1)

def nty_dow(wzor, n):
    return eval(wzor)

def wykres_aryt(n, a1, r):
    wyrazy = []
    x = list(range(1, n+1))
    while n >= 1:
        wyrazy.append(nty_aryt(n,a1,r))
        n -= 1
    wyrazy.reverse()
    plt.scatter(x, wyrazy, c = "blue")
    plt.xlabel("n-ty wyraz")
    plt.ylabel("wartosc n-tego wyrazu ciągu")
    plt.title("Wykres dla n wyrazow ciągu arytmetycznego")
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    url=base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(url)

def wykres_geo(n, a1, q):
    wyrazy = []
    x = list(range(1, n+1))
    while n >= 1:
        wyrazy.append(nty_geo(n,a1,q))
        n -= 1
    wyrazy.reverse()
    plt.scatter(x, wyrazy, c = "blue")
    plt.xlabel("n-ty wyraz")
    plt.ylabel("wartosc n-tego wyrazu ciągu")
    plt.title("Wykres dla n wyrazow ciągu geometrycznego")
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    url=base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(url)

def wykres_dow(wzor, n):
    x = list(range(1, n+1))
    wyrazy = []
    while n >= 1:
        wyrazy.append(nty_dow(wzor, n))
        n -= 1
    wyrazy.reverse()
    plt.scatter(x, wyrazy, c = "blue")
    plt.xlabel("n-ty wyraz")
    plt.ylabel("wartosc n-tego wyrazu ciągu")
    plt.title("Wykres dla n wyrazow ciągu geometycznego")
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    url=base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(url)


app = Flask(__name__)

#strona główna
@app.route("/")
def index():
    return render_template("index.html")

#kontakt
@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")

#arytmetyczny
@app.route("/arytmetyczny", methods=['POST','GET'])
def arytmetyczny():
    n=None
    a1=None
    r=None
    wykres=None
    wyraz=None
    suma=None
    if request.method=='POST':
        try:
            n=int(request.form["n"])
            a1=float(request.form["a1"])
            r=float(request.form["r"])
        except:
            pass
        wykres=wykres_aryt(n,a1,r)
        wyraz=nty_aryt(n, a1, r)
        suma=suma_aryt(n, a1, r)
    return render_template("arytmetyczny.html", n=n, a1=a1, r=r, wykres=wykres, suma=suma, wyraz=wyraz)

#geometryczny
@app.route("/geometryczny", methods=['POST','GET'])
def geometryczny():
    n=None
    a1=None
    q=None
    wykres=None
    wyraz=None
    suma=None
    if request.method=='POST':
        try:
            n=int(request.form["n"])
            a1=float(request.form["a1"])
            q=float(request.form["q"])
        except:
            pass
        wykres=wykres_geo(n,a1,q)
        wyraz=nty_geo(n, a1, q)
        suma=suma_geo(n, a1, q)
    return render_template("geometryczny.html", n=n, a1=a1, q=q, wykres=wykres, wyraz=wyraz, suma=suma)

#dowolny
@app.route("/dowolny", methods=['POST','GET'])
def dowolny():
    n=None
    wzor=None
    wykres=None
    wyraz=None
    suma=None
    if request.method=='POST':
        try:
            n=int(request.form["n"])
            wzor=request.form["wzor"]
        except:
            pass
        wykres=wykres_dow(wzor,n)
        wyraz=nty_dow(wzor,n)
        suma=suma_dow(wzor,n)
    return render_template("dowolny.html", n=n, wzor=wzor, wykres=wykres, suma=suma, wyraz=wyraz)