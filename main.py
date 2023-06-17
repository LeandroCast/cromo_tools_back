# from src import app, db
from src import app
from src import routes

# Inicialização do banco de dados
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
    print('buildando app')
