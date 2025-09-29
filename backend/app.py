from app import create_app, db
from flask_jwt_extended import JWTManager

app = create_app()

# ✅ Configure a secret key for JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # replace with environment variable in production

# ✅ Initialize JWTManager
jwt = JWTManager(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ensure tables exist
    app.run(debug=True, port=5000)
