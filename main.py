import pandas as pd 


def load_data(data_path):
    df = pd.read_csv(data_path)
    return df

def main():
    data_path = 'data.csv'
    df = load_data(data_path)
    print(df.items())

if __name__ == '__main__':
    main()