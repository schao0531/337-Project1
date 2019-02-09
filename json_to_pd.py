import pandas as pd

def json_to_pd(data):
    with open('gg2013.json') as f:
        data = json.load(f)

    Id = []
    text = []
    timestamp = []
    user_id = []
    screen_name = []

    for row in data:
        Id.append(row['id'])
        text.append(row['text'])
        timestamp.append(row['timestamp_ms'])
        user_id.append(row['user']['id'])
        screen_name.append(row['user']['screen_name'])

    table = pd.DataFrame({'text':text,'timestamp':timestamp,'user_id':user_id,'user_screen_name':screen_name},index=Id)
    table.index.rename('id',inplace=True)
    return table
