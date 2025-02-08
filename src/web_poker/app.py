from flask import Flask, render_template
from web_poker.config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    @app.route('/')
    def home():
        return render_template('base.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run() 