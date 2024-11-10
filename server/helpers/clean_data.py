import json

def clean_top_characteristics(dp, top_n=15):
    # Iterate over each person in the dataset
    file = open(dp, 'r', encoding='utf-8')
    data = json.load(file)

    for person, characteristics in data.items():
        # Sort characteristics by score in descending order and select the top_n
        top_characteristics = dict(sorted(characteristics.items(), key=lambda x: x[1], reverse=True)[:top_n])
        # Update the dictionary to only include the top_n characteristics
        data[person] = top_characteristics
    ofile = json.dump(data, "data/extended_properties_processed.json")
    if not ofile:
        return False
    return True