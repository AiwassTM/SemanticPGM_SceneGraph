#%%
import json
from collections import defaultdict
from tqdm import tqdm
import Project1 as p1
import Project2 as p2
import numpy as np
from networkx import is_connected

from pgmpy.models import MarkovNetwork
from pgmpy.factors import FactorSet
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import VariableElimination, BeliefPropagation

#%%
#filename = 'Filtered_Data_O10_A70_R18.json'
filename = 'PoperlyFiltered2.json'
with open(filename, 'r') as f:
    data = json.load(f)

#%%
def CreateChunksOfPairs(data):
    relations = sorted(data['Relations'].keys())
    pairs = {}

    for relation in relations:
        for pair in data['Relations'][relation]:
            pair_key = tuple(sorted(pair.keys()))  # Create a sorted tuple to represent the pair
            if pair_key not in pairs:
                pairs[pair_key] = {obj: [0.001]*len(relations) for obj in pair_key}
            for obj, value in pair.items():
                pairs[pair_key][obj][relations.index(relation)] = value

    return {'Relations': relations, 'Pairs': list(pairs.values())}


chunks = CreateChunksOfPairs(data)

#%%
def CreateRelationalFactors(model, data):
    for pair in data['Pairs']:
        objects = list(pair.keys())
        #values = [[[1, pair[objects[0]][i]], [pair[objects[1]][i], 1]] for i in range(len(data['Relations']))]
        
        values = np.random.randint(1, 35, (len(data['Relations']), 2, 2))
        values[:, 0, 0], values[:, 1, 1] = 1, 1
        
        factor = DiscreteFactor(['Relations', objects[0], objects[1]], [len(data['Relations']), 2, 2], values, state_names={'Relations': data['Relations'], objects[0]: ['tar','ref'], objects[1]: ['tar','ref']})
        
        # Add nodes and edges to the model
        model.add_nodes_from(['Relations', objects[0], objects[1]])
        model.add_edges_from([('Relations', objects[0]), ('Relations', objects[1]), (objects[0], objects[1])])
        
        # Add factor to the model
        model.add_factors(factor)
        
#%%      
def CreateAttributeFactors(model, data):
    for obj, attributes in data['Objects'].items():
        atts, values = attributes['Attributes'].keys(), attributes['Attributes'].values()
        #print(obj)
        #print(atts)
        #print(values)
        
        false_atts = ['white', 'black', 'big', 'small']
        false_vals = np.random.randint(1, 30, (2, len(false_atts)))
        false_vals[0,:] = 1     
        factor = DiscreteFactor([obj, obj+'Attributes'], [2, len(false_atts)], false_vals, state_names={obj+'Attributes': false_atts, obj: ['N','Y']})
        model.add_edge(obj, obj+'Attributes')
        model.add_factors(factor) 


# =============================================================================
#       NOPEEEE
#         false_atts = ['white', 'black', 'gray', 'big', 'small']
#         model.add_node(obj)
#         for f in false_atts:
#             v = np.random.randint(1, 30, (2))
#             factor = DiscreteFactor([obj], [2], v, state_names={obj: [f,'not_'+f]})          
#             model.add_factors(factor) 
# =============================================================================

# =============================================================================
#         false_atts = ['white', 'black', 'gray', 'big', 'small']
#         false_vals = np.random.randint(1, 30, (len(false_atts)))
#         model.add_node(obj)
#         factor = DiscreteFactor([obj], [len(false_atts)], false_vals, state_names={obj: false_atts})
#         model.add_factors(factor)
# =============================================================================
# =============================================================================
#         model.add_node(obj+'Attributes')
#         model.add_node(obj)
#         model.add_edge(obj, obj+'Attributes')
#         factor = DiscreteFactor([obj, obj+'Attributes'], [2, len(false_atts)], false_vals, state_names={obj+'Attributes': false_atts, obj: ['N','Y']})
#         model.add_factors(factor) 
# =============================================================================
        
        #factor = DiscreteFactor([obj], [len(atts)], list(values), state_names={obj: list(atts)})
        #print(factor)
         
        #break
        #for att, values in attributes['Attributes'].items():
            
            #a, v = att.keys(), att.values()
            
            #model.add_edge(obj, att)
            #values = [[0.01, 1], [0.01, value]]
            #print(obj, att,value)#, values)
            #print(values, '\n\n')
            #factor = DiscreteFactor([obj, att], [2, len(a)], att.values(), state_names={obj: ['N','Y'], att: ['N', 'Y']})
            # xd
            
            #factor = DiscreteFactor([obj], [len(att)], list(value), state_names={obj: list(att)})
            #print(obj, att, values)
            #model.add_factors(factor)    


# =============================================================================
# i = iter(data['Objects'].items())
# obj_Att = next(i)[1]['Attributes']
# att, vals = obj_Att.keys(), obj_Att.values()
# factor = DiscreteFactor(['obj'], [len(att)], list(vals), state_names={'obj': list(att)})
# =============================================================================

# =============================================================================
# data = {'Relations': ['relation1', 'relation2', 'relation3'],
#  'Pairs': [{'obj1': [55, 50, 2], 'obj2': [45, 50, 0]},
#            {'obj2': [6, 0.001, 0.001], 'obj200': [23, 0.001, 0.001]},
#            {'obj16': [0.001, 0.001, 64], 'obj22': [0.001, 0.001, 11]}]
# }
# 
# =============================================================================
#%%
model = MarkovNetwork()
CreateRelationalFactors(model, chunks)
model.check_model()
CreateAttributeFactors(model, data)
model.check_model()
print(is_connected(model))

#%%
for f in model.factors:
    print(f)

#%%
inference = BeliefPropagation(model)
q= inference.query(['building', 'boy'], evidence={'Relations': 'in_front_of'})
q= inference.query(['building', 'boy'], evidence={'Relations': 'behind', 'Attributes':'black'})
q= inference.query(['building', 'boy'], evidence={'Relations': 'behind', 'Attributes':'black'})
print(q)

q= inference.query(['building'], evidence={'Relations': 'behind', 'boy': 'small'})
print(q)
q= inference.query(['building'], evidence={'Relations': 'in_front_of', 'boy': 'small'})
print(q)
#%%
# MAP Query
map_q = inference.map_query(['building', 'tree'], evidence={'Relations': 'behind', 'Attributes':'black'})
map_q= inference.query(['Relations'], evidence={'tree':'Y'})
# Print the result
print(map_q)



#%%







