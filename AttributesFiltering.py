import json

with open('FINAL_val_sceneGraphs.json', 'r') as f:
    data = json.load(f)
#%%

#%%
#
#
#       BETTER-     VALUES
#
#
#
#
import matplotlib.pyplot as plt

# =============================================================================
# # Initialize a dictionary to store the counts of each attribute and the objects that have them
# attribute_details = {}
# object_details = {}
# 
# # Iterate over each object and its attributes
# for obj, details in data["Objects"].items():
#     if obj not in object_details:
#         object_details[obj] = set()
#     for attribute in details["Attributes"].keys():
#         if attribute not in attribute_details:
#             attribute_details[attribute] = set()
#         attribute_details[attribute].add(obj)
#         object_details[obj].add(attribute)
# =============================================================================
        


                        #   VALUES
#------------------------------------------------------------------------------
# Initialize a dictionary to store the counts of each attribute and the objects that have them
attribute_details = {}
object_details = {}

# Iterate over each object and its attributes
for obj, details in data['Objects'].items():
    if obj not in object_details:
        object_details[obj] = {}
    for attribute, count in details['Attributes'].items():
        if attribute not in attribute_details:
            attribute_details[attribute] = {}
        attribute_details[attribute][obj] = count
        object_details[obj][attribute] = count

#------------------------------------------------------------------------------
#%%
# =============================================================================
# # Create histograms
# attribute_histogram = {attribute: len(objects) for attribute, objects in attribute_details.items()}
# object_histogram = {obj: len(attributes) for obj, attributes in object_details.items()}
# 
# attribute_histogram = dict(sorted(attribute_histogram.items(),key=lambda item: item[1], reverse=True))
# object_histogram  = dict(sorted(object_histogram.items(),key=lambda item: item[1], reverse=True))
# =============================================================================


                        # VALUES

# Create histograms
attribute_histogram = {attribute: sum(objects.values()) for attribute, objects in attribute_details.items()}
object_histogram = {obj: sum(attributes.values()) for obj, attributes in object_details.items()}

attribute_histogram = dict(sorted(attribute_histogram.items(),key=lambda item: item[1], reverse=True))
object_histogram  = dict(sorted(object_histogram.items(),key=lambda item: item[1], reverse=True))

#%%
# Plot histogram for attributes
plt.figure(figsize=(10, 5))
plt.bar(attribute_histogram.keys(), attribute_histogram.values(), log=True)
plt.xlabel('Attributes')
plt.ylabel('Number of unique objects')
plt.title('Histogram showing for unique attributes how many objects have them')
plt.show()

# Plot histogram for objects
plt.figure(figsize=(10, 5))
plt.bar(object_histogram.keys(), object_histogram.values(), log=True)
plt.xlabel('Objects')
plt.ylabel('Number of unique attributes')
plt.title('Histogram showing for unique objects how many attributes they have')
plt.show()
