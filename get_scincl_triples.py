import argparse
import json
import os
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG)

import numpy as np

from gdt.triples_miner import TriplesMinerArguments
from gdt.triples_miner.generic import get_generic_triples
from cli_triples import get_metadata
from gdt.utils import get_graph_embeddings, get_workers

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--graph_paper_ids_path')
    parser.add_argument('--graph_embeddings_path')

    parser.add_argument('--train_s2orc_paper_ids_path')
    parser.add_argument('--train_query_s2orc_paper_ids_path')

    parser.add_argument('--triples_miner_kwargs', type=json.loads)

    parser.add_argument('--s2orc_metadata_dir')

    parser.add_argument('--output_path')
    parser.add_argument('--workers', default=24, type=int)

    args = parser.parse_args()

    pathlib.Path(args.output_path).mkdir(parents=True, exist_ok=True)

    triples_miner_args = TriplesMinerArguments(**args.triples_miner_kwargs)
    workers = get_workers(args.workers)

    with open(args.graph_paper_ids_path) as f:
        s2orc_paper_ids = json.load(f)  # S2ORC Ids
    
    if args.train_s2orc_paper_ids_path is not None:
        with open(args.train_s2orc_paper_ids_path) as f:
            train_s2orc_paper_ids = json.load(f)

    with open(args.train_query_s2orc_paper_ids_path) as f:
        train_query_s2orc_paper_ids = json.load(f)

    # Load embeddings from disk # TODO loading embeddings later would be better
    graph_embeddings = get_graph_embeddings(
        args.graph_embeddings_path,
        # do_normalize=triples_miner_args.ann_normalize_embeddings,
        do_normalize=False,  # normalize with ANN backend
        placeholder=triples_miner_args.ann_index_path is not None and os.path.exists(triples_miner_args.ann_index_path))

    if args.train_s2orc_paper_ids_path is not None:
        # Limit citation graph to the papers included in train_s2orc_paper_ids

        # Find indices in graph embeddings and extract vectors
        s2orc_paper_id_to_paper_idx = {pid: idx for idx, pid in enumerate(s2orc_paper_ids)}

        if not isinstance(train_s2orc_paper_ids, list):
            train_s2orc_paper_ids = list(train_s2orc_paper_ids)  # python sets are unordered -> convert to list!

        print('Limiting graph embedding to the selected paper ids')

        if triples_miner_args.ann_index_path is None or not os.path.exists(triples_miner_args.ann_index_path):
            train_embeddings = np.array(
                [graph_embeddings[s2orc_paper_id_to_paper_idx[s2orc_id], :] for s2orc_id in train_s2orc_paper_ids])
        else:
            train_embeddings = graph_embeddings  # do not filter if ANN exist

        print(f'New graph embeddings: {train_embeddings.shape}')

        train_idx_to_s2orc_paper_id = {idx: pid for idx, pid in enumerate(train_s2orc_paper_ids)}
        train_s2orc_paper_id_to_idx = {pid: idx for idx, pid in enumerate(train_s2orc_paper_ids)}
    else:
        # Do not change input graph
        # - None: no change
        # - S2ORC: Utilize full citation graph of S2ORC without filtering
        train_embeddings = graph_embeddings
        train_s2orc_paper_id_to_idx = {pid: idx for idx, pid in enumerate(s2orc_paper_ids)}
        train_idx_to_s2orc_paper_id = {idx: pid for idx, pid in enumerate(s2orc_paper_ids)}

    get_generic_triples(train_s2orc_paper_id_to_idx,
                        train_idx_to_s2orc_paper_id,
                        train_query_s2orc_paper_ids,
                        train_embeddings,
                        os.path.join(args.output_path, 'train_triples.csv'),
                        triples_miner_args=triples_miner_args,
                        workers=workers,
                        output_csv_header='query_paper_id,positive_id,negative_id')

    print('Generating triple metadata')

    # Extract metadata for triples
    get_metadata(input_path=os.path.join(args.output_path, 'train_triples.csv'),
                 output_path=os.path.join(args.output_path, 'train_metadata.jsonl'),
                 s2orc_metadata_dir=args.s2orc_metadata_dir,
                 workers=workers)
