def nearest_neighbor(graph_dict, rest_id, num):
    ''' Find the nearest neighbors of the given restaurant id

    Parameters
    ----------
    graph_dict: Dict
        A Python dictionary that stores the graph structure

    rest_id: String
        The id of restaurant

    num: Int
        The amount of results to return

    Returns
    -------
    result_list: List
        A list of tuples. Each tuple represents a retrieved restaurant.
        Tuple[0] means the restaurant id, and Tuple[1] is the distance.
        For example: [('175', 1), ('931', 2)] means the distance between rest_id and 931 is 2

    '''
    result_list = []
    visited = [rest_id]
    next_level = [rest_id]
    distance_counter = 1
    while(len(result_list) < num) and next_level != []:
        new_next_level = []
        this_level = []
        for node1 in next_level:
            for node2 in graph_dict[node1]:
                if node2 not in visited:
                    this_level.append((len(graph_dict[node1][node2]), node2))
                    new_next_level.append(node2)
                    visited.append(node2)
        this_level.sort(reverse = True)
        next_level = new_next_level
        for node in this_level:
            result_list.append((node[1], distance_counter))
        distance_counter+=1
    
    return result_list[0:num]

def node_to_node(graph_dict, node1, node2):
    ''' Find the shortest path between two restaurants

    Parameters
    ----------
    graph_dict: Dict
        A Python dictionary that stores the graph structure

    node1: String
        The id of first restaurant

    node2: String
        The id of second restaurant

    Returns
    -------
    result_list: List
        A list of tuples. Each tuple represents a step in the path.
        Tuple[0] means the restaurant id, and Tuple[1] is the list of shared tags
        For example: [('231', ['chicken','fries']),('108', ['fries'])] means in the first step of the shortest path
            , it goes to restaurant 231, and the connection between is "chicken" and "fries"

    '''
    visited = {node1:[]}
    next_level = [node1]
    while(node2 not in visited) and next_level != []:
        new_next_level = []
        this_level = {}
        for idx1 in next_level:
            for idx2 in graph_dict[idx1]:
                if idx2 not in visited:
                    visited[idx2] = visited[idx1]+[(idx2, graph_dict[idx1][idx2])]
                    this_level[idx2] = len(graph_dict[idx1][idx2])
                    new_next_level.append(idx2)
                elif idx2 in this_level and len(graph_dict[idx1][idx2]) > this_level[idx2]:
                    visited[idx2] = visited[idx1]+[(idx2, graph_dict[idx1][idx2])]
                    this_level[idx2] = len(graph_dict[idx1][idx2])
        
        next_level = new_next_level
    
    if node2 in visited:
        return visited[node2]
    else:
        return [(node2, ['They are NOT connected!'])]

def similar_list(graph_dict, node_list):
    ''' Find a list of most similar restaurants to the input restaurant list

    Parameters
    ----------
    graph_dict: Dict
         A Python dictionary that stores the graph structure

    node_list: Dict
         A list of restaurants that represents the users' preference

    Returns
    -------
    result_list: List
        A list of tuples. Each tuple represents a similar restaurant.
        Tuple[0] means the average distance to node_list, and Tuple[0] is the restaurant id
        For example: [(2.0, '833'),(2.2, '398')] means restaurant 833 has the shortest average distance 2.0 to node_list

    '''
    total_list = []
    time_counter = {}
    result_list = []
    for node in node_list:
        total_list = total_list + nearest_neighbor(graph_dict, node, 500)
    
    for node in total_list:
        if node[0] in time_counter:
            time_counter[node[0]] = (time_counter[node[0]][0]+1, time_counter[node[0]][1]+node[1])
        else:
            time_counter[node[0]] = (1, node[1])
        if time_counter[node[0]][0] == len(node_list):
            result_list.append((time_counter[node[0]][1]/len(node_list), node[0]))
    
    result_list.sort()
    
    return result_list[0:100]

def rest_stat_dist(rest_dict, graph_dict, node_list, name="cuisine"):
    ''' Turn the nodes into x-axis list and y-axis list for plotting

    Parameters
    ----------
    rest_dict: Dict
         A Python dictionary that stores the restaurant information

    graph_dict: Dict
         A Python dictionary that stores the graph structure

    node_list: List
         A list of restaurants that are going to plot

    name: String
        The data field to plot

    Returns
    -------
    x-axis: List
        The x-axis list for distribution plot of node_list in "name" field

    y-axis: List
        The y-axis list for distribution plot of node_list in "name" field

    '''
    tag_list = []
    for node in node_list:
        if isinstance(rest_dict[node][name], list):
            tag_list = tag_list + rest_dict[node][name]
        else:
            tag_list.append(rest_dict[node][name])
    
    tag_counter = {}
    for tag in tag_list:
        if tag in tag_counter:
            tag_counter[tag] += 1
        else:
            tag_counter[tag] = 1
    
    occurence = []
    
    for tag in tag_counter:
        occurence.append((tag_counter[tag], tag))
    occurence.sort(reverse = True)
    
    x_axis = []
    y_axis = []
    
    for item in occurence[0:8]:
        x_axis.append(item[1])
        y_axis.append(item[0])
    
    return x_axis, y_axis
    


def valid_rest_id(node, rest):
    ''' Determine whether the input node number is valid

    Parameters
    ----------
    node: String
        The user input string

    rest_dict: Dict
        A Python dictionary that stores the restaurant information

    Returns
    -------
    Bool: Whether or not the input number is valid

    '''

    if node.isdigit() and int(node) >= 0 and int(node) <= len(rest):
        return True
    else:
        return False