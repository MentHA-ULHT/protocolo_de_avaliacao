# Funções

def percentage(total: int, partial:int):
    '''
    Gets percentage from a total and partial number
    Does (partial/total)*100
    '''

    return int((partial/total)*100)

def create_percentage_list(obj_list, nr_answered):
    '''Returns a list of percentages, given a list of objects'''

    percentage = []
    for n, obj in enumerate(obj_list):
        p = 0
        if (n <= len(nr_answered)):
            if nr_answered[n] > 0 and obj.number_of_questions > 0:
                p = percentage(partial=nr_answered[n],total=obj.number_of_questions)
        percentage.append(int(p))
    return percentage


def print_nested_dict(dict_obj, indent=0):
    ''' Pretty Print nested dictionary with given indent level'''

    # Iterate over all key-value pairs of dictionary
    for key, value in dict_obj.items():
        # If value is dict type, then print nested dict
        if isinstance(value, dict):
            print(' ' * indent, key, ':', '{')
            print_nested_dict(value, indent + 4)
            print(' ' * indent, '}')
        else:
            print(' ' * indent, key, ':', value)