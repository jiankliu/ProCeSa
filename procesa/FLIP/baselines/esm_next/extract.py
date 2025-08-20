#!/usr/bin/env python3 -u
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import pathlib

import torch

from esm_local import FastaBatchedDataset
import os
from esm_next.models.esmc import ESMC

def create_parser():
    parser = argparse.ArgumentParser(
        description="Extract per-token representations and model outputs for sequences in a FASTA file"  # noqa
    )

    parser.add_argument(
        "fasta_file",
        type=pathlib.Path,
        help="FASTA file on which to extract representations",
    )
    parser.add_argument(
        "output_dir",
        help="output directory for extracted representations",
    )

    parser.add_argument("--toks_per_batch", type=int, default=4096, help="maximum batch size")

    # zs
    parser.add_argument("--truncate", type=int, default=0,
        help="Truncate sequences longer than 1024 to match the training setup")
    parser.add_argument('--trunc_len', type=int, default=1022)
    parser.add_argument("--nogpu", type=int, default=0, help="Do not use GPU even if available")
    # zs
    return parser


def main(args):
    model = ESMC.from_pretrained("esmc_600m")
    model.eval()

    if torch.cuda.is_available() and not args.nogpu:
        model = model.cuda()
        print("Transferred model to GPU")
    dataset = FastaBatchedDataset.from_file(args.fasta_file, trunc_len=args.trunc_len, truncate=args.truncate)
    batches = dataset.get_batch_indices(args.toks_per_batch, extra_toks_per_seq=1)
    # data_loader = torch.utils.data.DataLoader(dataset, collate_fn=BatchConverter(), batch_sampler=batches)
    data_loader = torch.utils.data.DataLoader(dataset, batch_sampler=batches)
    print(f"Read {args.fasta_file} with {len(dataset)} sequences")
    
    os.makedirs(args.output_dir, exist_ok=True)

    import time
    start_time = time.time()
    with torch.no_grad():
        for batch_idx, (labels, strs) in enumerate(data_loader):
            toks = model._tokenize(strs)
            print(
                f"Processing {batch_idx + 1} of {len(batches)} batches ({toks.size(0)} sequences)"
            )            
            if torch.cuda.is_available() and not args.nogpu:
                toks = toks.to(device="cuda", non_blocking=True)            
            _, embedding, _, attentions = model(toks)
            representations = {0: embedding}
            attentions = attentions.to(device="cpu")

            for i, label in enumerate(labels):
                # zs
                args.output_file = os.path.join(args.output_dir, f"{label}.pt")
                # zs
                result = {"label": label}
                result["representations"] = {
                    layer: t[i, 1 : len(strs[i]) + 1].clone()
                    for layer, t in representations.items()
                }
                result["contacts"] = attentions[i, :len(strs[i]), :len(strs[i])].clone()

                torch.save(result, args.output_file)
    print(time.time()-start_time)

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)