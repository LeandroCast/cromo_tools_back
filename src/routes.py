from.calculadora.views.calculadora_controller import calculadora_view

from src import app

calculadora_view.register(app,route_base='/calculadora/')
