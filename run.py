from app import create_app, db
from waitress import serve

app = create_app()

# Create database context
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("Server is starting using Waitress on http://127.0.0.1:5001")
    serve(app, host='0.0.0.0', port=5001)
