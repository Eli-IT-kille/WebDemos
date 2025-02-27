class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bank.db'
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False