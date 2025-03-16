import pandas as pd 




def load_data(data_path):
    df = pd.read_csv(data_path)
    i=0
    unique_values = [None]*len(df.columns)
    for column in df.columns:
        unique_values[i] = df[column].unique()
        i+=1
    S = []
    G = []
    S0=[None]*len(unique_values)
    G0=['?']*len(unique_values)
    S.append(S0)
    G.append(G0)
    all_unique_values = []
    for value in unique_values:
        for item in value:
            all_unique_values.append(item)
    CONSISTENCY_RULE = {
        '?': set(item for item in all_unique_values),
        None: set(),
        **{item: {item} for item in all_unique_values}  # This adds each item as both key and value
    }


    return df, unique_values, S, G, CONSISTENCY_RULE



def is_consistent(h, x):
    if len(h) != len(x):
        return False
    return all(h[i] == x[i] or h[i] == '?' or x[i] == '?' for i in range(len(h)))


def is_more_general(h1, h2):
    if len(h1) != len(h2):
        return False
    return all(h1[i] == h2[i] or h1[i] == '?' or (h2[i] is None and h1[i] is not None) for i in range(len(h1)))


def get_minimal_generalizations(h, x, unique_values):
    if len(h) != len(x):
        return []
    if h==[None]*len(h):
        return [x]
    list_of_generalizations = []
    for i in range(len(h)):
        if h[i] == '?':
            pass
        elif h[i] == None:
            for item in unique_values[i]:
                if x[i] != item:
                    list_of_generalizations.append(h[:i] + [item] + h[i+1:])
        elif h[i] != x[i] :
            list_of_generalizations.append(h[:i] + ['?'] + h[i+1:])
    return list_of_generalizations



def get_minimal_specializations(h, x):
    if len(h) != len(x):
        return []
    list_of_specializations = []
    for i in range(len(h)):
        if h[i] == None:
            pass
        elif h[i] != x[i] and x[i] == '?':
            list_of_specializations.append(h[:i] + x[i] + h[i+1:])
        elif h[i] == x[i] and h[i] != '?':
            list_of_specializations.append(h[:i] + [None] + h[i+1:])
    return list_of_specializations


def remove_less_general(G):
    to_remove = []
    for g in G:
        for g1 in G:
            if is_more_general(g1, g) and g1 != g:
                to_remove.append(g)
                break
    for item in to_remove:
        if item in G:
            G.remove(item)

def remove_more_general(S):
    to_remove = []
    for s in S:
        for s1 in S:
            if is_more_general(s, s1) and s1 != s:
                to_remove.append(s)
                break
    for item in to_remove:
        if item in S:
            S.remove(item)


def test_data(S0, G0, df, unique_values):
    print(S0)
    print(G0)
    for value in unique_values:        
        print(value)
    for index, row in df.iterrows():
        print(index, row.values)




def trait_positive_hypothesis(row, S, G):
    print('Positive Hypothesis')



def trait_negative_hypothesis(row, S, G):
    print('Negative Hypothesis')



def trait_row(row, S, G):
    if row[-1] == 'Yes':
        trait_positive_hypothesis(row, S, G)
    else:
        trait_negative_hypothesis(row, S, G)




def main():
    #set the path of the data file
    data_path = 'data.csv'
    df, unique_values, S, G, CONSISTENCY_RULE = load_data(data_path)
    for value in unique_values:
        print(value)

    
        




if __name__ == '__main__':
    main()