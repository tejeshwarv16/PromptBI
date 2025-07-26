# backend/run.py

from app import create_app

# Create an instance of the app using our factory function
app = create_app()

if __name__ == '__main__':
    # Runs the Flask development server
    # debug=True will reload the server automatically when you save changes
    app.run(debug=True)