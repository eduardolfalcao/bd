from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)

# Configure your JWT secret key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key

# Initialize the JWT manager
jwt = JWTManager(app)

# python3 api-maria.py
# curl -X POST -H "Content-Type: application/json" -d @test-admin.json http://127.0.0.1:8080/login
# curl -H "Authorization: Bearer <meu_token>" http://127.0.0.1:8080/protected

# Route to create a new token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    roles = ['prof']
    if username == 'edu' and password=='123':
        access_token = create_access_token(identity=username, additional_claims={"roles": roles})
        return jsonify(access_token=access_token) 
    else:
        return jsonify({"msg": "Bad username or password"}), 401
    

# A protected route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    claims = get_jwt()
    roles = claims.get('roles', [])

    # Check if the user has the required role
    if 'prof' not in roles:
        return jsonify(msg="You do not have access to this resource"), 403

    #chamada ao BD

    return jsonify(logged_in_as=current_user, roles=roles), 200

if __name__ == '__main__':
    app.run(port=8080)