import os
import requests
import jinja2
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
templateLoader =jinja2.FileSystemLoader("templates")
templateEnv = jinja2.Environment(loader=templateLoader)

def render_template(templateFilename, **context):
    return templateEnv.get_template(templateFilename).render(**context)

def send_simple_message(to, subject, body, html):
    return requests.post(f"https://api.mailgun.net/v3/{DOMAIN}/messages",
		auth=("api", os.getenv("MAILGUN_API_KEY")),
		data={"from": f"Wroclaw Galleries REST API <apiWG@{DOMAIN}>",
			"to": [to],
			"subject": subject,
			"text": body,
   			"html": html})
    
def send_user_registration_email(email, username):
    return send_simple_message(email, "Everything went according to plan!",
                               f"Hiya {username}! All right! You can now use our Stores REST API",
                               render_template("email/action.html", username=username))
    
