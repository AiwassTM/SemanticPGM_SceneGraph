#%%
import json
#filename = 'Filtered_Data_O10_A70_R18.json' # 'FINAL_val_sceneGraphs.json'
filename = 'FINAL_val_sceneGraphs.json'
with open(filename, 'r') as f:
    data = json.load(f)
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
#         'Above':[{'Man':13, 'Woman': 87}, {'Vehicle':3, 'Man': 16}, {'Woman':13, 'Man': 87}]
#     }
# }
# data = scene_graph
# =============================================================================
#%%

Relations = {}
for relation, list_of_pairs in data['Relations'].items():
    Relations[relation] = {}
    for pair in list_of_pairs:
        pair_of_relation = frozenset(pair.keys())
        if pair_of_relation not in Relations[relation]:
            Relations[relation][pair_of_relation] = sum(pair.values())
        else:
            Relations[relation][pair_of_relation] += sum(pair.values())
#%%            
RelationsSums = {}
for relation, pairs in Relations.items():
    RelationsSums[relation] = sum(pairs.values())
    
RelationsSums = dict(sorted(RelationsSums.items(),key=lambda item: item[1], reverse=True))
SelectedRelations = dict(list(RelationsSums.items())[0:10])
FilteredRelations = {relation: pairs for relation, pairs in data['Relations'].items() if relation in SelectedRelations}
data['Relations'] = FilteredRelations

#%%           
# =============================================================================
# Relations_ratios = {}          
# for relation, pairs in Relations.items():
#     Relations_ratios[relation] = len(pairs)/sum(pairs.values())
#     print(relation, len(pairs), sum(pairs.values()))
# =============================================================================
    
#%%
Objects = {}
Pairs = {}
for relation, list_of_pairs in data['Relations'].items():
    for pair in list_of_pairs:
        unique_pair = frozenset(pair.keys())
        if unique_pair not in Pairs:
            Pairs[unique_pair] = {}     
            Pairs[unique_pair][relation] = sum(pair.values())
        else:
            if relation in Pairs[unique_pair]:
                Pairs[unique_pair][relation] += sum(pair.values())
            else:
                Pairs[unique_pair][relation] = sum(pair.values())
#%%
Pairs_rations = {}  
Pairs_properties = {}              
for pair, relations in Pairs.items():
    Pairs_rations[pair] = {'Count': len(relations), 'Sum': sum(relations.values())}
    Pairs_properties[pair] = [len(relations), sum(relations.values())]
#    Pairs_rations[pair] =  len(relations)/sum(relations.values())
#    Pairs_properties[pair] = [len(relations), sum(relations.values())]
    
#%%

#%%
object_relation_counts = {}
object_pair_counts = {}                 # IMPORTANT - good results
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

#%%
MostPrevalentObjectsInPairs = dict(sorted(object_pair_counts.items(),key=lambda item: item[1], reverse=True)[5:25])
FilteredObjects = {obj: att for obj, att in data['Objects'].items() if obj in MostPrevalentObjectsInPairs}
data['Objects'] = FilteredObjects

#%%

# =============================================================================
# Attributes = {}
# for obj in data['Objects'].values():
#     for attributes in obj.values():
#         for att, val in attributes.items():
#             if att in Attributes:
#                 Attributes[att] += val
#             else:
#                 Attributes[att] = val
#             print(att, val)
#         #Attributes[attributes.keys()] = attributes.values
# 
# 
# 
# =============================================================================
            #   Attributes filtering
#
# Initialize a dictionary to store the counts of each attribute and the objects that have them
attribute_details = {}
#attribute_details_old = attribute_details
# Iterate over each object and its attributes
for obj, details in data["Objects"].items():
    for attribute in details["Attributes"].keys():
        if attribute not in attribute_details:
            attribute_details[attribute] = set()
        attribute_details[attribute].add(obj)

MostPrevalentAttributesOfObjects = dict(sorted(attribute_details.items(),key=lambda item: len(item[1]), reverse=True)[0:10])        
# Filter out attributes that are shared by less than 50 objects
#filtered_attributes = {attribute: objects for attribute, objects in attribute_details.items() if len(objects) >= 200}

# Update the "Objects" field in the data dictionary
for obj, details in data["Objects"].items():
    data["Objects"][obj]["Attributes"] = {attribute: count for attribute, count in details["Attributes"].items() if attribute in MostPrevalentAttributesOfObjects}

#%%
# Get the set of remaining objects
remaining_objects = set(data["Objects"].keys())

# Update the "Relations" field in the data dictionary
for relation, pairs in data["Relations"].items():
    # Filter out pairs whose members got deleted from the "Objects" field
    data["Relations"][relation] = [pair for pair in pairs if all(member in remaining_objects for member in pair)]

#%%
filename = 'PoperlyFiltered.json' #'Filtered_Data_O10_A70_R18.json'
with open(filename, 'w') as f:
    json.dump(data, f, indent=4)
#%%
# =============================================================================
# #%%
# 
# xd =  {'One': [10, 12], 'Two': [4, 15], 'Three': [13, 2], 'Four': [11, 7], 'Five': [5, 17], 'Six': [8,8]}
# import math
# 
# sorted_items = sorted(Pairs_properties.items(), key=lambda item: -math.sqrt(item[1][0] * item[1][1]))
sorted_items_int = sorted(Pairs_properties.items(), key=lambda item: -(item[1][0] * item[1][1]))
# 
# 
# #%%
# 
# def sorter(item):
#     x = -math.sqrt(item[1][0] * item[1][1])
#     y = -(item[1][0] * item[1][1])
#     print(x, y)
#     return x
# 
# 
# sorter(list(Pairs_properties.items())[2])
# sorter(sorted_items_int[0])
# 
# 
#%%
sorter_l = lambda item: -(item[0] * item[1])
xd2 = {item[0]:sorter_l(item[1]) for item in sorted_items_int}
# 
# 
# #%%
# # Plot histogram for attributes
# # Get the number of items that constitute 70% of the total.
num_items = len(sorted_items_int)
top_70_percent_count = int(num_items * 1)
# 
# # Select the top 70% of items.
top_70_percent_items = sorted_items_int[:top_70_percent_count]
# 
sorter_l = lambda item: -(item[0] * item[1])
xd70 = {item[0]:sorter_l(item[1]) for item in top_70_percent_items}
# 
selected_pairs = list(xd70)[0:20]


# 
# keys_xd = ['']*len(xd70.keys())
# for i, key in enumerate(xd70.keys()):
#     keys_xd[i] = ' '.join(key).replace(' ', '_')
# 
# 
# 
# 
# =============================================================================
