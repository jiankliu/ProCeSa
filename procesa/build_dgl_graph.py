import dgl
import torch
import pickle
import numpy as np
import pandas as pd
import joblib
import argparse
import os
import time

def normalize_adj(mx):
    rowsum = np.array(mx.sum(1))
    r_inv = (rowsum ** -0.5).flatten()
    r_inv[np.isinf(r_inv)] = 0
    r_mat_inv = np.diag(r_inv)
    result = r_mat_inv @ mx @ r_mat_inv
    return result

def get_feats(ptdir, name):
    data = torch.load(os.path.join(ptdir, f'{name}.pt'))
    nodefeat = data['representations'][KEY].detach().float().cpu().numpy()
    edgefeat = data['contacts'].detach().float().cpu().numpy()
    return nodefeat, edgefeat

def build_dgl_graph(
        names,
        sequences,
        dataroot='/datasets/procesa_data/meltome',
        dataset='s2c2_0',
        split='train',
        model='esm1b',
        trunc_len=800):


    start_time = time.time()
    for index, (name, sequence) in enumerate(zip(names, sequences)):
        names_list, sequences_dict, graphs_dict = list(), dict(), dict()
        if index % 1000 == 0:
            print("{} / {}".format(index, len(names)))
        node_features, edge_features = get_feats(os.path.join(dataroot, dataset, model, split), name)

        if len(sequence) > trunc_len:
            sequence = sequence[:trunc_len]
        src, dst = np.nonzero(edge_features)

        # [L, L] -> [num_edges]
        edge_features = normalize_adj(edge_features) #[L,L]
        edge_features = edge_features[np.nonzero(edge_features)]

        graph = dgl.graph((src, dst), num_nodes=len(sequence))

        if not len(sequence) == node_features.shape[0]:
            print(f"{dataset} {model} {split} {name} node features error!")
            assert False
        if not len(edge_features) == len(src) == len(dst):
            print(f"{dataset} {model} {split} {name} edge features error!")
            assert False
        
        # add features
        graph.ndata['x'] = torch.from_numpy(node_features).float()
        graph.edata['x'] = torch.from_numpy(edge_features).float()
        
        # add all
        names_list.append(name)
        sequences_dict[name] = sequence
        graphs_dict[name] = graph
        
        saveroot = os.path.join(dataroot, dataset, model, 'pkls', split)
        os.makedirs(saveroot, exist_ok=True)
        with open(os.path.join(saveroot, f"{name}.pickle"), 'wb') as fw:
            joblib.dump(
                [names_list,
                 sequences_dict,
                 graphs_dict], fw)
    print(time.time() - start_time)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataroot', type=str, default='/dataset/procesa_data/meltome')
    parser.add_argument('--dataset', type=str, default='s2c2_0')
    parser.add_argument('--model', type=str, default='esm1b')
    parser.add_argument('--trunc_len', type=int, default=800)
    args = parser.parse_args()
    KEY = 0 if args.model == 'esmc' else 33

    # build the dgl graph cache
    for split in ['train', 'test']:
        data = pd.read_csv(os.path.join(args.dataroot, 'splits', f"{args.dataset}_{split}.csv"), sep=',')

        names = data['gene'].values.tolist()
        sequences = data['sequence'].values.tolist()

        build_dgl_graph(
                names,
                sequences,
                dataroot=args.dataroot,
                dataset=args.dataset,
                split=split,
                model=args.model,
                trunc_len=args.trunc_len)

