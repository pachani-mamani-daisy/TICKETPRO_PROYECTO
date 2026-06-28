import os

class Config:
    SECRET_KEY = 'ticketpro_secret_key_2026'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ticketpro.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False