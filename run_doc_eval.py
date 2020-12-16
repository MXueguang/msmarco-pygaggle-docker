import argparse
import requests

from tqdm import tqdm

query_file = 'msmarco-docdev-queries.tsv'
corpus_file = 'msmarco-docs.tsv'

parser = argparse.ArgumentParser(description='Generates a run.')
parser.add_argument('--output', required=True, type=str, help='Output run file.')
parser.add_argument('--k', required=True, type=int, help='Number of hits.')
parser.add_argument('--l1_url', type=str, default="http://127.0.0.1:8000/search/", help='url of L1')
parser.add_argument('--l2_url', type=str, default="http://127.0.0.1:9000/rerank/", help='url of L2')

args = parser.parse_args()

queries = []
with open(query_file, 'r') as f:
    for line in f:
        qid, query = line.rstrip().split('\t')
        queries.append([qid, query])

corpus = {}
with open(corpus_file, 'r') as f:
    for line in tqdm(f):
        info = line.rstrip().split("\t")
        if len(info)==4:
            doc_id, _, _, doc = info
            corpus[doc_id] = doc

with open(args.output, 'w') as out:
    for entry in tqdm(queries):
        qid = entry[0]
        query = entry[1]
        #print(f'{qid}----{query}')
        L1_response = requests.get(args.l1_url, params={'q': query, 'k': args.k})
        L1_response = L1_response.json()
        L2_request = {"query": query,
                      "passages": [{"docid": h["docid"],
                                    "score": h["score"],
                                    "text": corpus[h["docid"]]} for h in L1_response["results"]]}
        L2_response = requests.post(args.l2_url, json=L2_request).json()
        rank = 1
        for h in L2_response['results']:
            out.write(f'{qid} Q0 {h["docid"]} {rank} {h["score"]:.6f} monoBERT\n')
            rank = rank + 1

