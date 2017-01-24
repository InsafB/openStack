import requests

def send_simple_message(user_id):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc12348685aa64630bc8157aa469c7a2e.mailgun.org/messages",
        auth=("api", "key-bc9ebbf529e8e7b9b96f729e91cbe39d"),
        data={"from": "Mailgun Sandbox <postmaster@sandboxc12348685aa64630bc8157aa469c7a2e.mailgun.org>",
              "to": "boukrouh.insaf@gmail.com",
              "subject": "Notification: OpenStack lottery game",
              "text": "Hello,\nUser "+user_id+" has played.\nOpenStack Team 9."})
