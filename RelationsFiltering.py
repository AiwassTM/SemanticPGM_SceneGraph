#%%
import json
import matplotlib.pyplot as plt

    
#%%
filename = 'FINAL_val_sceneGraphs.json' # or filename = 'filtered_file.json'

#filename = 'filtered_file_attributesANDobjects_andAdjustedRelations.json'
#filename = 'Filtered_Data_O10_A70_R18.json'
with open(filename, 'r') as f:
    data = json.load(f)
#%%
unique_pairs = set()
relation_counts = {}
pair_relation_counts = {}

for relation, pairs in data['Relations'].items():
    relation_counts[relation] = len(pairs)
    for pair in pairs:
        pair_key = frozenset(pair.keys())
        unique_pairs.add(pair_key)
        if pair_key not in pair_relation_counts:
            pair_relation_counts[pair_key] = {}
        if relation not in pair_relation_counts[pair_key]:
            pair_relation_counts[pair_key][relation] = sum(pair.values())
        pair_relation_counts[pair_key][relation] += sum(pair.values())
# =============================================================================
#             pair_relation_counts[pair_key][relation] = 0
#         pair_relation_counts[pair_key][relation] += 1
# =============================================================================

print(f'Total unique pairs across all relations: {len(unique_pairs)}')

relation_counts = dict(sorted(relation_counts.items(), key=lambda item: item[1], reverse=True))
for relation, count in relation_counts.items():
    print(f'Unique pairs for relation "{relation}": {count}')

pair_relation_counts = dict(sorted(pair_relation_counts.items(), key=lambda item: sum(item[1].values()), reverse=True))
for pair, relations in pair_relation_counts.items():
    print(f'{set(pair)}:')
    relations = dict(sorted(relations.items(), key=lambda item: item[1], reverse=True))
    for relation, count in relations.items():
        print(f'  {relation}": {count} times')
    print('')
    
#%%
hist_data = [len(relations) for pair, relations in pair_relation_counts.items()]
hist_data2 = [sum(relations.values()) for pair, relations in pair_relation_counts.items()]

# Create histogram
plt.hist(hist_data2, bins=range(1, max(hist_data)+2), align='left', rwidth=0.8)
plt.xlabel('Number of relations')
plt.ylabel('Number of pairs')
plt.title('Histogram of number of relations for each pair')
#plt.yscale('log')
plt.show()

#%%
# Filter out relations with less than 50 pairs
filtered_data2 = {relation: pairs for relation, pairs in data['Relations'].items() if 50 < sum(sum(pair.values()) for pair in pairs) and (len(relation)<10 and len(relation)>4) }
filtered_data = {relation: pairs for relation, pairs in data['Relations'].items() if relation_counts[relation] >17}
total = sum(sum(pair[1]) for pair in pairs)


new_data2 = {'Objects': data['Objects'], 'Relations': filtered_data2}
#
#
data["Relations"] = filtered_data2
#
#%%
# Save the filtered data back to the JSON file
with open('filtered_file.json', 'w') as f:
    json.dump(data, f, indent=4)
    
#%%    