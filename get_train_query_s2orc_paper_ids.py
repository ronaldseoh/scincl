import json
import csv
import gzip

import tqdm


if __name__ == '__main__':

    scincl_data_file_path = "train_triples.csv.gz"
    train_query_s2orc_paper_ids = set()

    with gzip.open(scincl_data_file_path, 'r') as f_in:
        reader = csv.reader(f_in, delimiter=',')

        for row in tqdm.tqdm(reader):
            train_query_s2orc_paper_ids.add(row[0])

    train_query_s2orc_paper_ids = list(train_query_s2orc_paper_ids)
            
    with open('train_query_s2orc_paper_ids.json', 'w') as train_query_s2orc_paper_ids_file:
        json.dump(train_query_s2orc_paper_ids, train_query_s2orc_paper_ids_file)
