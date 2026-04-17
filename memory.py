import json

FILE = "post_history.json"

def save_post(topic):

    try:
        with open(FILE,"r") as f:
            data=json.load(f)
    except:
        data=[]

    data.append(topic)

    with open(FILE,"w") as f:
        json.dump(data,f)