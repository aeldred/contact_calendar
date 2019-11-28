from flask import Flask

app = Flask(__name__)

# avoid circular dependencies
from contact_calendar import routes
