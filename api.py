import flask
from flask import request, jsonify
from flask.views import MethodView
from ast import literal_eval
from markdown import markdown
from pygments.formatters.html import HtmlFormatter
from flask_cors import CORS
import os

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
        operacao = request.get_json().get('operacao', False)
        logica = request.get_json().get('logica', False)

        cartesian = [(x, y) for x in conjunto_a for y in conjunto_b]
        result = []

        def check_if_prime(num):
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        return False
                else:
                    return True
            else:
                return False

        # Impar
        def list_odds(new_list, opc):
            odd_list = []
            for prod in new_list:
                if prod[opc] % 2 != 0:
                    odd_list.append(prod)
            return odd_list

        # Par
        def list_evens(new_list, opc):
            even_list = []
            for prod in new_list:
                if prod[opc] % 2 == 0:
                    even_list.append(prod)
            return even_list

        # Primos
        def list_primes(new_list, opc):
            prime_list = []
            for prod in new_list:
                if check_if_prime(prod[opc]):
                    prime_list.append(prod)
            return prime_list

        def check_if_number(prod):
            return isinstance(prod[0], int) and isinstance(prod[1], int)

        if logica:
            if 'a+b=' in logica:
                num = int(logica.replace('a+b=', ''))
                for prod in cartesian:
                    if check_if_number(prod) and prod[0] + prod[1] == num:
                        result.append(prod)
            elif 'a-b=' in logica:
                num = int(logica.replace('a-b=', ''))
                for prod in cartesian:
                    if check_if_number(prod) and prod[0] - prod[1] == num:
                        result.append(prod)
            elif 'a*b=' in logica:
                num = int(logica.replace('a*b=', ''))
                for prod in cartesian:
                    if check_if_number(prod) and prod[0] * prod[1] == num:
                        result.append(prod)
            elif 'a/b=' in logica:
                num = int(logica.replace('a/b=', ''))
                for prod in cartesian:
                    if check_if_number(prod) and prod[1] != 0 and prod[0] / prod[1] == num:
                        result.append(prod)
            elif isinstance(logica, dict):
                if 'a' in logica:
                    if logica['a'] == 'par':
                        result += list_evens(cartesian if not result else result, 0)
                    elif logica['a'] == 'impar':
                        result += list_odds(cartesian if not result else result, 0)
                    elif logica['a'] == 'primo':
                        result += list_primes(cartesian if not result else result, 0)
                if 'b' in logica:
                    if logica['b'] == 'par':
                        result += list_evens(cartesian if not result else result, 0)
                    elif logica['b'] == 'impar':
                        result += list_odds(cartesian if not result else result, 0)
                    elif logica['b'] == 'primo':
                        result += list_primes(cartesian if not result else result, 0)
                result = list(set(result))

        elif operacao:
            if operacao == '+':
                pass
            elif operacao == '-':
                pass
            elif operacao == '*':
                pass
            elif operacao == '/':
                for prod in cartesian:
                    if check_if_number(prod) and prod[1] % prod[0] == 0:
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