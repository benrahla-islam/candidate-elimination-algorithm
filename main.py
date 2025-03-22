import pandas as pd 




def load_data(data_path):
    df = pd.read_csv(data_path)
    unique_values = [df[column].unique().tolist() for column in df.columns]
    
    S0 = [None] * (len(unique_values)-1)
    G0 = ['?'] * (len(unique_values)-1)

    return df, unique_values, [S0], [G0]



def is_consistent(h, x):
    if len(h) != len(x):
        return False
    return all(h[i] == x[i] or h[i] == '?' or x[i] == '?' for i in range(len(h)))


def is_more_general(h1, h2):
    if len(h1) != len(h2):
        return False
    moreGeneral = False
    for i in range(len(h1)):
        if h1[i] == '?':
            if h2[i] == '?':
                pass
            else:
                moreGeneral = True
        else:
            if h1[i] != h2[i] :
                if h2[i] != None:
                    return False
                else:
                    moreGeneral = True
    if moreGeneral:
        return True
    else:
        return False
    

def get_minimal_generalizations(h, x):
    if len(h) != len(x):
        return []
    if h==[None]*len(h):
        return [x]
    generalization = h[:]
    for i in range(len(h)):
        if h[i] == '?':
            generalization[i] = h[i]
        elif h[i] is None:
            generalization[i] = x[i]
        elif h[i] != x[i] :
            generalization[i] = '?'
    return generalization



def get_minimal_specializations(h, x, unique_values):
    if len(h) != len(x):
        return []
    list_of_specializations = []
    for i in range(len(h)):
        if h[i] == '?' :
            for item in unique_values[i]:
                if item != x[i]:
                    list_of_specializations.append(h[:i] + [item] + h[i+1:])
    return list_of_specializations


def remove_less_general(G):
    return [g for g in G if not any(is_more_general(g1, g) and g1 != g for g1 in G)]


def remove_more_general(S):
    return [s for s in S if not any(is_more_general(s, s1) and s1 != s for s1 in S)]


def test_data(S0, G0, df, unique_values):
    print(S0)
    print(G0)
    for value in unique_values:        
        print(value)
    for index, row in df.iterrows():
        print(index, row.values)




def trait_positive_hypothesis(row, S, G):
    G[:] = [g for g in G if is_consistent(g, row)]
    S_copy = S[:]
    for s in S_copy:
        if not is_consistent(s, row):
            S.remove(s)
            for generalization in get_minimal_generalizations(s, row):
                if is_consistent(generalization, row):
                    S.append(generalization)
    S[:] = remove_more_general(S)



def trait_negative_hypothesis(row, S, G, unique_values):
    S[:] = [s for s in S if not is_consistent(s, row)]
    G_copy = G.copy()
    for g in G_copy:
        if is_consistent(g, row):
            G.remove(g)
            for specialization in get_minimal_specializations(g, row, unique_values):
                if not is_consistent(specialization, row):
                    G.append(specialization)
            G = remove_less_general(G)


def trait_row(row, S, G, unique_values):
    row = row.tolist()
    if row[-1] == 'Yes':
        trait_positive_hypothesis(row, S, G)
    else:
        trait_negative_hypothesis(row, S, G, unique_values)




def main():
    #set the path of the data file
    data_path = 'driving_behavior.csv'
    df, unique_values, S, G = load_data(data_path)
    for value in unique_values:
        print(value)

    for index, row in df.iterrows():
        trait_row(row[:-1], S, G, unique_values)

    print('Final S:', S)
    print('Final G:', G)
    
        




if __name__ == '__main__':
    S = [
        ['Sunny', 'Hot', 'High', 'Weak'],  # Most specific hypothesis
        ['Sunny', '?', 'High', '?'],       # More general
        ['?', '?', '?', '?']               # Most general
    ]

    reduced_S = remove_more_general(S)
    print("Reduced S:")
    for s in reduced_S:
        print(s)