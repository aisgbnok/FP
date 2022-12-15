import os

import pandas as pd
import whois


def merge_raw(seed=75, save=False):
    """
    Loads our separate dataframes and merges them together.
    Ensures the columns are equal, normalizes the labels,
    and finally shuffles the columns using the seed.

    :param seed: Integer value that ensures reproduction of resulting dataframe.
    :param save: Whether to save the pandas dataframe. Can be False (default), 'CSV', or 'PICKLE'.
    :return: A pandas dataframe that contains a url and label column.
             The label column is 0 for benign and 1 for malicious.
    """
    # Get all of our datasets
    df_aj = pd.read_csv(os.path.join('datasets', 'raw', 'urls-antonyj.csv'))
    df_ms = pd.read_csv(os.path.join('datasets', 'raw', 'urls-manu-siddhartha.csv'))

    # Ensure Columns Match
    df_ms.columns = df_aj.columns

    # Normalize Data, 1 is malicious, 0 is benign
    df_aj['label'] = (df_aj['label'] == 'bad').astype(int)
    df_ms['label'] = (df_ms['label'] != 'benign').astype(int)

    # Merge dataframes
    df = pd.merge(df_aj, df_ms, how='outer')

    # Keep first exact matches
    df = df.drop_duplicates()

    # Drop all duplicate urls with conflicting labels
    # Prevents some data poisoning, and promotes data integrity
    df = df.drop_duplicates(subset='url', keep=False)

    # Shuffle using seed value
    df = df.sample(frac=1, random_state=seed)

    # Reset Index
    df = df.reset_index(drop=True)

    if save == 'PICKLE':
        df.to_pickle('datasets/t4-urls.zip')
    elif save == 'CSV':
        df.to_csv('datasets/t4-urls.csv')

    return df


def gather_whois(urls, range_start, range_end):
    samples = []

    for i, url in enumerate(urls):
        try:
            response = whois.whois(url)
        except:
            continue

        if response.domain_name != "null" and response.domain_name is not None:
            response['sample_url'] = url
            samples.append(dict(response))

        print(f'Completed {i} of {len(urls)}, {i / len(urls) * 100}%')

    df = pd.DataFrame(samples)
    df.to_csv(f'datasets/t4-whois-{range_start}-{range_end}.csv')


def main():
    dataset = merge_raw()

    gather_whois(dataset['url'].iloc[:10000].values, 0, 10000)


if __name__ == '__main__':
    main()
