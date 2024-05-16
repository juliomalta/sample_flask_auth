from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from database import db
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma_senha_propria'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({'message': 'User logged in'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401

# rotas antes de GET geralmente são POST

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'User logged out'}), 200

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)


#######
# Verifica se o servidor está rodando 


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     # Validação de dados
#     if not username or not password:
#         return jsonify({'message': 'Username and password are required'}), 400
#     if len(username) < 3 or len(password) < 8:
#         return jsonify({'message': 'Username must be at least 3 characters and password at least 8 characters long'}), 400

#     try:
#         user = User.query.filter_by(username=username).first()
#     except Exception as e:
#         return jsonify({'message': 'An error occurred while processing your request'}), 500

#     if user and user.check_password(password):
#         return jsonify({'message': 'User logged in'}), 200
#     else:
#         return jsonify({'message': 'Invalid username or password'}), 401