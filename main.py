import pandas as pd

def load_data(data_path):
    """
    # data must be in the form of a CSV file
    # data must have the last column as the target column
    # target column must have values 'Yes' or 'No'
    Loads data from a CSV file, extracts unique values from each column,
    and initializes the S0 and G0 hypotheses.

    Args:
        data_path (str): The path to the CSV file.

    Returns:
        tuple: A tuple containing the DataFrame, unique values per column,
               initial specific hypothesis (S0), and initial general hypothesis (G0).
    """
    df = pd.read_csv(data_path)
    unique_values = [df[column].unique().tolist() for column in df.columns]
    S0 = [None] * (len(unique_values)-1)
    G0 = ['?'] * (len(unique_values)-1)
    return df, unique_values, [S0], [G0]


def is_consistent(h, x):
    """
    Checks if a hypothesis is consistent with an example.

    Args:
        h (list): The hypothesis.
        x (list): The example.

    Returns:
        bool: True if the hypothesis is consistent with the example, False otherwise.
    """
    if len(h) != len(x):
        return False
    return all(h[i] == x[i] or h[i] == '?' or x[i] == '?' for i in range(len(h)))


def is_more_general(h1, h2):
    """
    Checks if hypothesis h1 is more general than hypothesis h2.

    Args:
        h1 (list): The first hypothesis.
        h2 (list): The second hypothesis.

    Returns:
        bool: True if h1 is more general than h2, False otherwise.
    """
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
                if h2[i] is not None:
                    return False
                else:
                    moreGeneral = True
    if moreGeneral:
        return True
    else:
        return False
    

def get_minimal_generalizations(h, x):
    """
    Computes the minimal generalization of a hypothesis given an example.

    Args:
        h (list): The hypothesis.
        x (list): The example.

    Returns:
        list: A list containing the minimal generalization of h with respect to x.
    """
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
    return [generalization]


def get_minimal_specializations(h, x, unique_values):
    """
    Computes the minimal specializations of a hypothesis given an example and unique values.

    Args:
        h (list): The hypothesis.
        x (list): The example.
        unique_values (list): List of unique values for each attribute.

    Returns:
        list: A list of minimal specializations of h with respect to x.
    """
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
    """
    Removes hypotheses from G that are less general than another hypothesis in G.

    Args:
        G (list): The list of general hypotheses.

    Returns:
        list: A list of hypotheses from G with less general hypotheses removed.
    """
    return [g for g in G if not any(is_more_general(g1, g) and g1 != g for g1 in G)]


def remove_more_general(S):
    """
    Removes hypotheses from S that are more general than another hypothesis in S.

    Args:
        S (list): The list of specific hypotheses.

    Returns:
        list: A list of hypotheses from S with more general hypotheses removed.
    """
    return [s for s in S if not any(is_more_general(s, s1) and s1 != s for s1 in S)]


def trait_positive_hypothesis(row, S, G):
    """
    Updates the specific and general hypotheses based on a positive training example.

    Args:
        row (list): A positive training example.
        S (list): The current specific hypotheses.
        G (list): The current general hypotheses.
    """
    G[:] = [g for g in G if is_consistent(g, row)]
    S_copy = S[:]
    for s in S_copy:
        if not is_consistent(s, row):
            S.remove(s)
            generalization = get_minimal_generalizations(s, row)
            S.append(generalization[0])
    S[:] = remove_more_general(S)


def trait_negative_hypothesis(row, S, G, unique_values):
    """
    Updates the specific and general hypotheses based on a negative training example.

    Args:
        row (list): A negative training example.
        S (list): The current specific hypotheses.
        G (list): The current general hypotheses.
        unique_values (list): List of unique values for each attribute.
    """
    S[:] = [s for s in S if not is_consistent(s, row)]
    G_copy = G[:]
    for g in G_copy:
        if is_consistent(g, row):
            G.remove(g)
            for specialization in get_minimal_specializations(g, row, unique_values):
                if (not is_consistent(specialization, row) and 
                    any(is_consistent(specialization, s) or is_more_general(specialization, s) for s in S)):
                    G.append(specialization)
    G[:] = remove_less_general(G)


def trait_row(row, S, G, unique_values):
    """
    Processes a single row from the dataset to update the hypotheses.

    Args:
        row (pandas.Series): A row from the DataFrame.
        S (list): The current specific hypotheses.
        G (list): The current general hypotheses.
        unique_values (list): List of unique values for each attribute.
    """
    row = row.tolist()
    if row[-1] == 'Yes':
        trait_positive_hypothesis(row[:-1], S, G)
    else:
        trait_negative_hypothesis(row[:-1], S, G, unique_values)


def main(data_path):
    """
    Main function to execute the Candidate Elimination algorithm.

    Args:
        data_path (str): The path to the CSV file.
    """
    df, unique_values, S, G = load_data(data_path)
    for index, row in df.iterrows():
        trait_row(row, S, G, unique_values)

    print('Final S:', S)
    print('Final G:', G)
    

if __name__ == '__main__':
    main('driving_behavior.csv')