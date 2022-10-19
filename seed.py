from models import db, User
from app import app

db.drop_all()
db.create_all()

# Add Users
joel = User(
    first_name='Joel',
    last_name='Burton',
    img_url='http://joelburton.com/joel-burton.jpg'
)

trevez = User(
    first_name='Trevor',
    last_name='Ezra',
    img_url='http://joelburton.com/joel-burton.jpg'
)

db.session.add(joel)
db.session.add(trevez)

db.session.commit()
