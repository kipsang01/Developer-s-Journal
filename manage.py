from app import create_app,db
from app.models import User

app = create_app('development')

with app.app_context():
    db.drop_all()


if __name__ == '__main__':
    app.run()

