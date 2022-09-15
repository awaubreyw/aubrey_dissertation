
import os
import json

def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj

video_info_filenames = [
    "3blue1brown.json",
    "asapscience.json",
    "crashcourse.json",
    "deep_look.json",
    "everyday_astronaut.json",
    "khan_academy.json",
    "kurzgesagt_–_in_a_nutshell.json",
    "minutephysics.json",
    "nilered.json",
    "physics_girl.json",
    "primer.json",
    "science_channel.json",
    "scishow.json",
    "smartereveryday.json",
    "tkor.json",
    "veritasium.json",
    "vsauce.json"
]

descriptions_index = {}
title_index = {}

# keys: title, description
for filename in video_info_filenames:
    with open(os.path.join("src/results", filename), "r") as f:
        data = json.load(f)

    # get the video data from the file
    video_datas = data[list(data.keys())[0]]['video_data']


    # Inverted Index Code
    # Its important to lowercase so that we can match things like "Visual" and "visual"
    for vid_id, vid_metadata in video_datas.items():
        title = vid_metadata['title'].lower().split() # Split on spaces e.g. ['How', 'to', 'lie', 'using', 'visual', 'proofs']
        
        for word in title:
            if word not in title_index:
                title_index[word] = {vid_id} # We use a set instead of a list because we don't want duplicate video ids
            title_index[word].add(vid_id)
            
        description = vid_metadata['description'].lower().split()
        
        # We can reuse the same code for the description
        for word in description:
            if word not in descriptions_index:
                descriptions_index[word] = {vid_id}
            descriptions_index[word].add(vid_id)

with open("title_inverted_index.json", "w") as f:
    json.dump(title_index, f, default=serialize_sets)

with open("description_inverted_index.json", "w") as f:
    json.dump(descriptions_index, f, default=serialize_sets)