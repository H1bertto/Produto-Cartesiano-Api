import flask
from flask import request, jsonify
from flask.views import MethodView
from ast import literal_eval
from markdown import markdown
from pygments.formatters.html import HtmlFormatter
from flask_cors import CORS
import operator
import os
import re

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    readme = open("README.md", 'r', encoding="utf-8")
    md_template = markdown(readme.read(), extensions=["fenced_code"])
    formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = "<style>" + css_string + "</style>"
    md_template = md_css_string + md_template
    return md_template
    # return "<h1>Trabalho de Matemática Discreta</h1><p>Assunto: Produto Cartesiano</p>"


class CalculateView(MethodView):

    def post(self):
        conjunto_a = request.get_json().get('conjunto_a', False)
        if not isinstance(conjunto_a, list):
            conjunto_a = literal_eval(conjunto_a)
        conjunto_b = request.get_json().get('conjunto_b', False)
        if not isinstance(conjunto_b, list):
            conjunto_b = literal_eval(conjunto_b)
        logica = request.get_json().get('logica', False)

        cartesian = [(x, y) for x in conjunto_a for y in conjunto_b]
        result = []

        # Primo
        def prime(num, extra):
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        return False
                else:
                    return True
            else:
                return False

        # Impar
        def odd(num, extra):
            if num % 2 != 0:
                return True
            return False

        # Par
        def even(num, extra):
            if num % 2 == 0:
                return True
            return False
                
        def check_if_only_numbers():
            for prod in cartesian:
                if not check_if_number(prod):
                    return False
            return True

        def check_if_number(prod):
            return isinstance(prod[0], int) and isinstance(prod[1], int)

        if logica and check_if_only_numbers():
            a = None
            b = None
            x = None
            num_a = None
            num_b = None
            num_x = None

            # Aritimetica
            if 'a+b=' in logica:
                x = operator.add
                num_x = int(re.findall("a\+b=([\d]+)", logica, re.IGNORECASE)[0])
            elif 'a-b=' in logica:
                x = operator.sub
                num_x = int(re.findall("a-b=([\d]+)", logica, re.IGNORECASE)[0])
            elif 'a*b=' in logica:
                x = operator.mul
                num_x = int(re.findall("a\*b=([\d]+)", logica, re.IGNORECASE)[0])
            elif 'a/b=' in logica:
                x = operator.truediv
                num_x = int(re.findall("a/b=([\d]+)", logica, re.IGNORECASE)[0])
            elif 'a#b' in logica:
                x = operator.mod
                num_a = x

            # Logica
            if 'a!=' in logica:
                a = operator.is_not
                num_a = re.findall("a!=([\d]+|b)", logica, re.IGNORECASE)[0]
            elif 'a<=' in logica:
                a = operator.le
                num_a = re.findall("a<=([\d]+|b)", logica, re.IGNORECASE)[0]
            elif 'a<' in logica:
                a = operator.lt
                num_a = re.findall("a<([\d]+|b)", logica, re.IGNORECASE)[0]
            elif 'a>=' in logica:
                a = operator.ge
                num_a = re.findall("a>=([\d]+|b)", logica, re.IGNORECASE)[0]
            elif 'a>' in logica:
                a = operator.gt
                num_a = re.findall("a>([\d]+|b)", logica, re.IGNORECASE)[0]
            elif 'a==' in logica:
                a = operator.eq
                num_a = re.findall("a==([\d]+|b)", logica, re.IGNORECASE)[0]
            elif 'a=par' in logica:
                a = even
                num_a = "0"
            elif 'a=impar' in logica:
                a = odd
                num_a = "0"
            elif 'a=primo' in logica:
                a = prime
                num_a = "0"

            if 'b!=' in logica:
                b = operator.is_not
                num_b = re.findall("b!=([\d]+|a)", logica, re.IGNORECASE)[0]
            elif 'b<=' in logica:
                b = operator.le
                num_b = re.findall("b<=([\d]+|a)", logica, re.IGNORECASE)[0]
            elif 'b<' in logica:
                b = operator.lt
                num_b = re.findall("b<([\d]+|a)", logica, re.IGNORECASE)[0]
            elif 'b>=' in logica:
                b = operator.ge
                num_b = re.findall("b>=([\d]+|a)", logica, re.IGNORECASE)[0]
            elif 'b>' in logica:
                b = operator.gt
                num_b = re.findall("b>([\d]+|a)", logica, re.IGNORECASE)[0]
            elif 'b==' in logica:
                b = operator.eq
                num_b = re.findall("b==([\d]+|a)", logica, re.IGNORECASE)[0]
            elif 'b=par' in logica:
                b = even
                num_b = "0"
            elif 'b=impar' in logica:
                b = odd
                num_b = "0"
            elif 'b=primo' in logica:
                b = prime
                num_b = "0"
            
            if '||' in logica:
                for prod in cartesian:
                    if num_a == 'b':
                        num_a = prod[1]
                    if num_b == 'a':
                        num_b = prod[0]
                    if a(prod[0], int(num_a)) or b(prod[1], int(num_b)) or x(prod[0], prod[1]) == num_x:
                        result.append(prod)
            elif '&&' in logica:
                for prod in cartesian:
                    if num_a == 'b':
                        num_a = prod[1]
                    if num_b == 'a':
                        num_b = prod[0]
                    if a and b:
                        if a(prod[0], int(num_a)) and b(prod[1], int(num_b)):
                            result.append(prod)
                    elif a and x:
                        if a(prod[0], int(num_a)) and x(prod[0], prod[1]) == num_x:
                            result.append(prod)
                    elif b and x:
                        if b(prod[1], int(num_b)) and x(prod[0], prod[1]) == num_x:
                            result.append(prod)
            else:
                if a:
                    for prod in cartesian:
                        if num_a == 'b':
                            num_a = prod[1]
                        if a(prod[0], int(num_a)):
                            result.append(prod)
                elif b:
                    for prod in cartesian:
                        if num_b == 'a':
                            num_b = prod[0]
                        if b(prod[1], int(num_b)):
                            result.append(prod)
                elif x:
                    for prod in cartesian:
                        if x(prod[0], prod[1]) == num_x:
                            result.append(prod)

        return jsonify({
            'conjunto_universo': cartesian,
            'modulo_conjunto_universo': len(cartesian),
            'resposta': result,
            'modulo_resposta': len(result)
        })


calculate_view = CalculateView.as_view('calculate_view')
app.add_url_rule(
        '/calculate/', view_func=calculate_view, methods=['GET', 'POST']
)

if __name__ == "__main__":
    if "HEROKU_ENV" in os.environ:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()