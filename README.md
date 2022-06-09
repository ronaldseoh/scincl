# SciNCL

```bash
python get_scincl_triples.py --graph_paper_ids_path /iesl/canvas/bseoh/s2orc_without_scidocs/entity_names_paper_id_0.json --graph_embeddings_path 
/iesl/canvas/bseoh/s2orc_without_scidocs/embeddings_paper_id_0.v200.h5  --train_s2orc_paper_ids_path /iesl/canvas/bseoh/without_leakage/s2orc_paper_ids.seed_0.json --train_query_s2orc_paper_ids_path 
/iesl/canvas/bseoh/without_leakage/query_s2orc_paper_ids.seed_0.json --triples_miner_kwargs '{"ann_index_path": "/iesl/canvas/bseoh/without_leakage/index", "triples_per_query": 5, 
"easy_positives_count": 5, "easy_positives_strategy": "knn", "easy_positives_k_min": 20, "easy_positives_k_max": 25, "easy_negatives_count": 3, "easy_negatives_strategy": "random_without_knn", 
"hard_negatives_count": 2, "hard_negatives_strategy": "knn", "hard_negatives_k_min": 3998, "hard_negatives_k_max": 4000}' --s2orc_metadata_dir /iesl/canvas/bseoh/new/20200705v1/full/metadata 
--output_path /iesl/canvas/bseoh/without_leakage/new --workers 24
```
