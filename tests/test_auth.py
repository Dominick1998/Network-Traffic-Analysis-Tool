import unittest
import jwt
from backend.auth import generate_token, token_required, role_required, JWT_SECRET_KEY
from flask import Flask, jsonify, request

# Create a dummy Flask app for testing decorators
app = Flask(__name__)

@app.route('/protected', methods=['GET'])
@token_required
def protected_route():
    """
    A protected route requiring authentication.
    """
    return jsonify({'message': 'Access granted'})

@app.route('/admin_only', methods=['GET'])
@token_required
@role_required("Admin")
def admin_only_route():
    """
    A route restricted to admin users.
    """
    return jsonify({'message': 'Admin access granted'})

class AuthTests(unittest.TestCase):
    """
    A set of tests for the authentication and authorization functions.
    """

    def setUp(self):
        """
        Set up a test client and mock tokens.
        """
        self.app = app.test_client()
        self.admin_token = generate_token(user_id=1, role="Admin")
        self.user_token = generate_token(user_id=2, role="User")

    def test_generate_token(self):
        """
        Test JWT token generation.
        """
        token = generate_token(user_id=1, role="Admin")
        decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(decoded['user_id'], 1)
        self.assertEqual(decoded['role'], "Admin")

    def test_protected_route_with_valid_token(self):
        """
        Test accessing a protected route with a valid token.
        """
        response = self.app.get('/protected', headers={'Authorization': self.admin_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Access granted'})

    def test_protected_route_with_invalid_token(self):
        """
        Test accessing a protected route with an invalid token.
        """
        response = self.app.get('/protected', headers={'Authorization': 'invalid_token'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Invalid token!'})

    def test_admin_only_route_with_admin_token(self):
        """
        Test accessing an admin-only route with an admin token.
        """
        response = self.app.get('/admin_only', headers={'Authorization': self.admin_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Admin access granted'})

    def test_admin_only_route_with_user_token(self):
        """
        Test accessing an admin-only route with a non-admin token.
        """
        response = self.app.get('/admin_only', headers={'Authorization': self.user_token})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Access denied: Insufficient privileges!'})

    def test_token_expiration(self):
        """
        Test that an expired token is rejected.
        """
        expired_token = jwt.encode(
            {'user_id': 1, 'role': 'Admin', 'exp': 0},  # Expired token
            JWT_SECRET_KEY,
            algorithm="HS256"
        )
        response = self.app.get('/protected', headers={'Authorization': expired_token})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {'message': 'Token has expired!'})

if __name__ == "__main__":
    unittest.main()
