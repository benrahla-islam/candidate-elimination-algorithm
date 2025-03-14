import pandas as pd 


def load_data(data_path):
    df = pd.read_csv(data_path)
    i=0
    unique_values = [None]*len(df.columns)
    for column in df.columns:
        unique_values[i] = df[column].unique()
        i+=1
    return df, unique_values



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
    df, unique_values = load_data(data_path)

    #initialize S and G for data set
    S = []
    G = []
    S0=[None]*len(unique_values)
    G0=['?']*len(unique_values)
    S.append(S0)
    G.append(G0)

    #test the data viability
    for index, row in df.iterrows():
        trait_row(row, S, G)



if __name__ == '__main__':
    main()