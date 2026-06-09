print('alive'); app = __import__('flask').Flask(__name__); print('flask ok'); app.run(debug=False, port=5000)
