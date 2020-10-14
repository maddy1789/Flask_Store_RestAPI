from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_db():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5001, debug=True)