#%%
import json
#%%
# =============================================================================
# scene_graph = {
#     'Objects':{
#         'Man': {'Attributes': {'Bald': 10, 'Tall': 25, 'Young': 3}},
#         'Woman': {'Attributes': {'Young': 10, 'Short': 1, 'LongHair':1}},
#         'Vehicle': {'Attributes': {'Old': 10, 'High': 1, 'Damaged':1}},
#     },
#     'Relations': {
#         'InFrontOf': [{'Man':55, 'Woman': 45}, {'Vehicle':23, 'Man': 6}],
#         'NextTo': [{'Man':50, 'Woman': 50}],
#         'Above':[{'Man':13, 'Woman': 87}, {'Vehicle':3, 'Man': 16}]
#     }
# }
# 
# =============================================================================
filename = 'FINAL_val_sceneGraphs.json'
with open(filename, 'r') as f:
    data = json.load(f)


# Initialize dictionaries to hold the statistics
object_relation_counts = {}
object_pair_counts = {}
object_specific_relation_counts = {}

for relation, pairs in  data['Relations'].items():
    for pair in pairs:
        for object, value in pair.items():
            # Update the total number of relations for the object
            if object not in object_relation_counts:
                object_relation_counts[object] = 0
            object_relation_counts[object] += value

            # Update the total number of pairs for the object
            if object not in object_pair_counts:
                object_pair_counts[object] = 0
            object_pair_counts[object] += 1

            # Update the number of times the object occurs in each relation
            if object not in object_specific_relation_counts:
                object_specific_relation_counts[object] = {}
            if relation not in object_specific_relation_counts[object]:
                object_specific_relation_counts[object][relation] = 0
            object_specific_relation_counts[object][relation] += value

object_relation_counts, object_pair_counts, object_specific_relation_counts


#%%
# Initialize dictionaries to hold the statistics
relation_pair_counts = {}
relation_occurrence_counts = {}
object_relation_counts = {}

for relation, pairs in data['Relations'].items():
    if relation not in relation_pair_counts:
        relation_pair_counts[relation] = 0
    if relation not in relation_occurrence_counts:
        relation_occurrence_counts[relation] = 0

    for pair in pairs:
        relation_pair_counts[relation] += 1
        for object, value in pair.items():
            relation_occurrence_counts[relation] += value

            if object not in object_relation_counts:
                object_relation_counts[object] = {}
            if relation not in object_relation_counts[object]:
                object_relation_counts[object][relation] = 0
            object_relation_counts[object][relation] += value

relation_pair_counts, relation_occurrence_counts, object_relation_counts

#%%

#               above pairs with diffrernt order were treated like different ones

# Initialize a dictionary to store the counts of each pair and the relations that have them
pair_details = {}

# Iterate over each relation and its pairs
for relation, pairs in data['Relations'].items():
    for pair in pairs:
        # Use a frozenset to treat pairs with the same objects as the same, regardless of order
        unordered_pair = frozenset(pair.keys())
        if unordered_pair not in pair_details:
            pair_details[unordered_pair] = {}
        if relation not in pair_details[unordered_pair]:
            pair_details[unordered_pair][relation] = 0
        pair_details[unordered_pair][relation] += sum(pair.values())

pair_details
#%%




