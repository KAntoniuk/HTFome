from app_data import create_app
import os

application = app = create_app()

if __name__ == '__main__':
    app.run()