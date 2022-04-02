from bookwell_system import app as application
from dotenv import load_dotenv
load_dotenv()
app=application
if __name__ == '__main__':
	app.run(debug=True)
