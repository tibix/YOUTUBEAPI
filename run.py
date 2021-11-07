from app import create_app

app = create_app(env='dev')

if __name__ == "__main__":
    app.run()