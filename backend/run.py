import os
from dotenv import load_dotenv
from app import create_app

env_file = '.env.production' if os.path.exists(
    '.env.production') else '.env.development'
load_dotenv(env_file)

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
