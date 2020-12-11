import argparse
import requests

from tqdm import tqdm

query_file = 'msmarco-docdev-queries.tsv'
corpus_file = 'msmarco-corpus.tsv'

parser = argparse.ArgumentParser(description='Generates a run.')
parser.add_argument('--output', required=True, type=str, help='Output run file.')
parser.add_argument('--k', required=True, type=int, help='Number of hits.')

args = parser.parse_args()

queries = []
with open(query_file, 'r') as f:
    for line in f:
        qid, query = line.rstrip().split('\t')
        queries.append([qid, query])

corpus = {}
with open(corpus_file, 'r') as f:
    for line in tqdm(f):
        doc_id, doc = line.rstrip().split('\t')
        corpus[doc_id] = doc

with open(args.output, 'w') as out:
    for entry in tqdm(queries):
        qid = entry[0]
        query = entry[1]
        #print(f'{qid}----{query}')
        L1_response = requests.get('http://127.0.0.1:8000/search/', params={'q': query, 'k': args.k})
        L1_response = L1_response.json()
        L2_request = {"query": query,
                      "passages": [{"docid": h["docid"],
                                    "score": h["score"],
                                    "text": corpus[h["docid"]]} for h in L1_response]}
        L2_response = requests.post('http://127.0.0.1:8000/rerank/', json=L2_request)
        rank = 1
        for h in L2_response['results']:
            out.write(f'{qid} Q0 {h["docid"]} {rank} {h["score"]:.6f} monoBERT\n')
            rank = rank + 1