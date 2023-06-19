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
        values = np.random.randint(100, 3500, (2, 1, 1))
        
        for rel in data['Relations']:
            factor = DiscreteFactor([rel, objects[0], objects[1]],
                                    [2, 1, 1], values,
                                    state_names={rel: ['N', 'Y'], objects[0]: [''], objects[1]: ['']})
            print(factor)
            model.add_nodes_from([rel, objects[0], objects[1]])
            model.add_edges_from([(rel, objects[0]), (rel, objects[1]), (objects[0], objects[1])])
            model.add_factors(factor)
        
#%%      
def CreateAttributeFactors(model, data):
    for obj, attributes in data['Objects'].items():
        #atts, values = attributes['Attributes'].keys(), attributes['Attributes'].values()
        
        false_atts = ['white', 'black', 'big', 'small']
        false_vals = np.random.randint(100, 3000, (1, len(false_atts)))
        factor = DiscreteFactor([obj, obj+'Attributes'], [1, len(false_atts)], false_vals, state_names={obj+'Attributes': false_atts, obj: ['']})
        model.add_edge(obj, obj+'Attributes')
        model.add_factors(factor) 

#%%
model = MarkovNetwork()
CreateRelationalFactors(model, chunks)
model.check_model()
CreateAttributeFactors(model, data)
model.check_model()
print(is_connected(model))

#%%
# well, i dont know what nodes and relations are inside the model therefore can not predetermine working queryies.
# also dataset is too bad to return good numbers therefore are randomized, train_sceneGraph.json can be used to solve this, but is huuuge.
#
# =============================================================================
# print('Nodes:\n',len(model.nodes()), '\n', model.nodes())
# print('\nEdges:\n', len(model.edges()), '\n', model.edges())
# print('\nFactors:\n', len(model.factors))
# 
# #%%
# inference = BeliefPropagation(model)
# q = inference.query(['Man', 'Woman', 'InFrontOf'])#, evidence={'InFrontOf': 'Y'}) #Strange & Stupid
# q = inference.query(['Man', 'Woman'], evidence={'ManAttributes': 'white', 'WomanAttributes': 'white'}) 
# q = inference.query(['Tree', 'Woman'], evidence={'InFrontOf': 'Y'}) 
# q = inference.query(['Man', 'Woman', 'ToTheLeftOf']) 
# print(q)
# 
# 
# map_q= inference.map_query(['InFrontOf'], evidence={'Man':'', 'Woman':''})
# map_q= inference.query(['Man', 'Woman', 'InFrontOf'], evidence={'ManAttributes': 'white', 'WomanAttributes': 'black'}) 
# map_q= inference.query(['fenceAttributes', 'buildingAttributes'], evidence={'behind': 'Y'}) 
# print(map_q)
# 
# =============================================================================

#%%










