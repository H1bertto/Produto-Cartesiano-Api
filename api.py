import flask
from flask import request, jsonify
from flask.views import MethodView

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    return "<h1>Trabalho de Matemática Discreta</h1><p>Assunto: Produto Cartesiano</p>"


class CalculateView(MethodView):

    def post(self):
        conjunto_a = request.get_json().get('conjunto_a', False)
        conjunto_b = request.get_json().get('conjunto_b', False)
        operacao = request.get_json().get('operacao', False)
        logica = request.get_json().get('logica', False)

        if operacao:
            pass

        elif logica:
            pass

        return jsonify({
            'resposta': "",
            'modulo': ""
        })


calculate_view = CalculateView.as_view('calculate_view')
app.add_url_rule(
        '/calculate/', view_func=calculate_view, methods=['GET', 'POST']
)

app.run()
