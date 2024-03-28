import json

#获得的json数据
new_resp = '{"predicted_label": "grassfalse", "scores": [["grassfalse", "1.000"], ["grasstrue", "0.000"]]}'
data = json.loads(new_resp)
predicted_label = data['predicted_label']

print(predicted_label)

