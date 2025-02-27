from flask import Flask, render_template, request
from flask_migrate import Migrate, upgrade
from models import db, Customer, Account, seedData


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/Bank'
db.app = app
db.init_app(app)
migrate = Migrate(app,db)



@app.route("/")

def home():
    customers_count = Customer.query.count()
    accounts_count = Account.query.count()
    total_balance = db.session.query(db.func.sum(Account.balance)).scalar() or 0
    return render_template('home.html', customers = customers_count, accounts=accounts_count, total_balance=total_balance)

def startpage():
    return render_template("index.html")



@app.route('/customer/<int:id>')
def customer(id):
    customer = Customer.query.get_or_404(id)
    accounts = Account.query.filter_by(customer_id=id).all()
    total_balance = sum(account.balance for account in accounts)
    return render_template('customer.html', customer=customer, accounts=accounts, total_balance=total_balance)


@app.route('/search', methods=['GET'])
def search():
    lastname = request.args.get('lastname')
    surname = request.args.get('surname')
    city = request.args.get('city')
    query = Customer.query

    if lastname:
        query = query.filter(Customer.lastname.ilike(f'%{lastname}%'))
    if surname:
        query = query.filter(Customer.surname.ilike(f'%{surname}%'))
    if city:
        query = query.filter(Customer.city.ilike(f'%{city}%'))

    customers = query.all()
    return render_template('search.html', customers=customers)

if __name__ == '__main__':
    app.run(debug=True)


if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData(db)
    app.run(debug=True)