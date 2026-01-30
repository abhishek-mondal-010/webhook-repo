from app import create_app

# Create a Flask app instance using the  function
app = create_app()

# Only run the app if this script is executed directly
if __name__ == "__main__":
    # Start the Flask development server
    # debug=True enables automatic reloads and better error messages
    # port=5000 makes the app accessible at http://127.0.0.1:5000
    app.run(debug=True, port=5000)
