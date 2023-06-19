#%%
import json
from collections import defaultdict
from tqdm import tqdm

  
#%%
def Function1():
    print("XD")


def FilterData_StageZero(input_file_name:str, output_file_name:str) -> None:
    '''
    Description:
    -----------
        Removes junk data.

    '''
    # Load the JSON file
    with open(input_file_name, 'r') as f:
        data = json.load(f)

    # Initialize a new dictionary to store the filtered data
    filtered_data = {}

    # Iterate over the data
    for i, (scene_id, scene_data) in enumerate(data.items()):
        # Create a new scene dictionary, excluding 'w', 'h', 'x', 'y'
        new_scene = {key: value for key, value in scene_data.items() if key not in ['w', 'h', 'x', 'y', 'height','width']}

        # Update the 'objects' dictionary
        new_objects = {}
        for obj_id, obj_data in scene_data['objects'].items():
            new_objects[obj_id] = {key: value for key, value in obj_data.items() if key not in ['w', 'h', 'x', 'y']}
        new_scene['objects'] = new_objects

        # Add the new scene to the filtered data, renumbering the scene ID
        filtered_data[i] = new_scene

    # Save the filtered data to a new JSON file
    with open(output_file_name, 'w') as f:
        json.dump(filtered_data, f, indent=4)

  

  
def Preprocessing_StageOne(input_file_name:str, output_file_name:str) -> None:
    '''
    Description:
    -----------
        Replaces ID of object with its Name and then removes "Name" field as it becomes redundant.

    '''
    with open(input_file_name, 'r') as f:
        data = json.load(f)
                
    # Initialize dictionaries to store the IDs for each name
    object_ids = {}
    relation_ids = {}
    attribute_ids = {}
    ### Placing it ABOVE seems working, althrough it demands some investigation later

    # Iterate over the data
    for scene_id, scene_data in data.items():
        for obj_id, obj_data in scene_data['objects'].items():
            # Store the object ID
            if obj_data['name'] not in object_ids:
                object_ids[obj_data['name']] = [obj_id]
            else:
                object_ids[obj_data['name']].append(obj_id)

            # Store the attribute IDs
            for attribute in obj_data['attributes']:
                if attribute not in attribute_ids:
                    attribute_ids[attribute] = [obj_id]
                else:
                    attribute_ids[attribute].append(obj_id)

            # Store the relation IDs
            for relation in obj_data['relations']:
                if relation['name'] not in relation_ids:
                    relation_ids[relation['name']] = [obj_id]
                else:
                    relation_ids[relation['name']].append(obj_id)
        #
        #
        #
        # Replace object IDs with their names in the 'objects' dictionary
        for obj_name, obj_ids in object_ids.items():
            for obj_id in obj_ids:
                if obj_id in scene_data['objects']:
                    scene_data['objects'][obj_name] = scene_data['objects'].pop(obj_id)

        # Replace object IDs with their names in the 'object' field of each relation
        for obj_name, obj_ids in object_ids.items():
            for obj_id in obj_ids:
                for obj_data in scene_data['objects'].values():
                    for relation in obj_data['relations']:
                        if relation['object'] == obj_id:
                            relation['object'] = obj_name
                            
#=============================================================================
    for scene_id, scene_data in data.items():
        for obj_id, obj_data in scene_data['objects'].items():
        # Delete the 'name' key
            del obj_data['name']
#=============================================================================

    # Save the updated data to a new JSON file
    with open(output_file_name, 'w') as f:
        json.dump(data, f, indent=4)
        



def MergeScenes_StageTwo(input_file_name:str, output_file_name:str):
    '''
    Description:
    -----------
        Cumulates all scenes' informations into one.

    '''

    with open(input_file_name) as f:
        scene_graphs = json.load(f)
        
    result = {
        "Objects": defaultdict(lambda: {"Attributes": defaultdict(int)}),
        "Relations": defaultdict(list)
    }

    for _, scene_graph in tqdm(scene_graphs.items(), desc="Processing scene graphs"):
        for obj_name, obj in scene_graph["objects"].items():
            # Process attributes
            for attr in obj["attributes"]:
                result["Objects"][obj_name]["Attributes"][attr] += 1

            # Process relations
            for rel in obj["relations"]:
                relation_name = rel["name"]
                target_object = rel["object"]

                # Find existing relation pair in the list
                for pair in result["Relations"][relation_name]:
                    if obj_name in pair and target_object in pair:
                        pair[obj_name] += 1
                        break
                else:  # If no existing pair is found, create a new one
                    result["Relations"][relation_name].append({obj_name: 1, target_object: 0})
                    
    # Write the result to a JSON file
    with open(output_file_name, 'w') as f:
        json.dump(result, f, indent=4)

    return result




def Load_and_Save(func):
    def wrapper(filename_in: str, filename_out: str):
        # read the input from the file
        with open(filename_in, 'r') as f:
            input_value = json.load(f)

        # call the original function with the read input
        output_value = func(input_value)

        # write the output to the output file
        with open(filename_out, 'w') as f:
            json.dump(output_value, f, indent=4)
        
        return output_value

    return wrapper

@Load_and_Save
def Transformation_FinalStage(data):
    '''
    Description:
    -----------
        Cumulates all scenes' informations into one.

    '''
    for relation_name, pairs in data["Relations"].items():
        new_pairs = []
        for pair in pairs:
            keys = list(pair.keys())
            if len(keys) >= 2:
                new_pair = {keys[0]: pair[keys[0]], keys[1]: pair[keys[1]]}
                new_pairs.append(new_pair)
        data["Relations"][relation_name] = new_pairs
    return data


def Underscoring_Uniques():
    with open('unique_items.json') as f:
        unique_items = json.load(f)
    
    for key, value in unique_items.items():
        unique_items[key] = [item.replace(" ", "_") for item in value]
    
    with open('unique_items_underscored.json', 'w') as f:
        json.dump(unique_items, f, indent=4)
        

def replace_space_with_underscore(input_file_name: str, output_file_name: str) -> None:
    with open(input_file_name, 'r') as f:
        data = json.load(f)

    def replace_in_dict(obj):
        if isinstance(obj, dict):
            return {k.replace(' ', '_'): replace_in_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_in_dict(item) for item in obj]
        elif isinstance(obj, str):
            return obj.replace(' ', '_')
        else:
            return obj

    data = replace_in_dict(data)

    with open(output_file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Usage example:
# replace_space_with_underscore('input.json', 'output.json')

# =============================================================================
# FilterData('val_sceneGraphs.json', 'filtered_val_sceneGraphs.json')
# PreprocessingOne('filtered_val_sceneGraphs.json', 'preprocessed_val_sceneGraphs.json')
# result = MergeScenesFromStageOne('preprocessed_val_sceneGraphs.json', 'merged_preprocessed_val_sceneGraphs.json')
# transformed_data = TransformMergedScenes(result)
# =============================================================================