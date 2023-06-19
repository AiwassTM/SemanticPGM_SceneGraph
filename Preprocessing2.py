#%%
import json
from collections import defaultdict
from tqdm import tqdm
import Project1 as p1

from pgmpy.models import MarkovNetwork
from pgmpy.factors import FactorSet
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import VariableElimination, BeliefPropagation

#%%
# Initialize an empty list to store the relations
def CreateRelationalChunksForModel(ready_data: dict) -> list:
    data = ready_data
    relations_list = []
    
    # Iterate over the relations
    for relation, objs in data['Relations'].items():
        for obj in objs:
            # Get all unique objects involved in the relation
            involved_objects = list(obj.keys())
    
            # For every pair of involved objects, create a new dictionary
            for i in range(len(involved_objects)):
                for j in range(i+1, len(involved_objects)):
                    obj1 = involved_objects[i]
                    obj2 = involved_objects[j]
    
                    # Check if a dictionary for this pair of objects already exists
                    existing_dict = None
                    for existing_relation in relations_list:
                        if obj1 in existing_relation and obj2 in existing_relation:
                            existing_dict = existing_relation
                            break
    
                    # If a dictionary for this pair of objects doesn't exist, create a new one
                    if existing_dict is None:
                        existing_dict = {'Relations':[], obj1: [], obj2: []}
                        relations_list.append(existing_dict)
    
                    # Add the relation and the corresponding values to the appropriate lists
                    existing_dict['Relations'].append(relation)
                    existing_dict[obj1].append(obj[obj1])
                    existing_dict[obj2].append(obj[obj2])
    return relations_list

def CreateFactorFromRelation(model: MarkovNetwork, data: dict, directional_index: int = 0) -> DiscreteFactor:
    
# =============================================================================
#     for key, value in unique_items.items():
#         unique_items[key] = [item.replace(" ", "_") for item in value]
# =============================================================================
    
    nodes = list(data.keys())
    #
    edges = [(nodes[i], nodes[j]) for i in range(len(nodes)) for j in range(i+1, len(nodes))]
    model.add_edges_from(edges)
    #
    values = list(data.values())
    
    objects_key = [key for key in data.keys() if key != 'Relations']
    
    values = [[[0.001, data[objects_key[0]][i]], [data[objects_key[1]][i], 0.001]] for i in range(len(data['Relations']))]
    #print(values)
    names = {node: ['ref', 'tar'] if node != 'Relations' else data['Relations'] for node in nodes}

    cardinality = [2,2,2]
    cardinality[directional_index] = len(data['Relations'])

    f = DiscreteFactor(nodes, cardinality, values, state_names=names)
    #model.add_factors(f)
    return f