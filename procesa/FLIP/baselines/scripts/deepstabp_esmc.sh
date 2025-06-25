export PYTHONPATH=$PWD:$PYTHONPATH
export DATANAME=deepstabp
export MODELNAME=esmc
export KEYNAME=deepstabp

python embeddings/embeddings.py \
	${KEYNAME} \
	$MODELNAME \
	--datadir /datasets/procesa_data/ \
	--bulk_compute \
	--outdir /datasets/procesa_data/$DATANAME/$DATANAME/$MODELNAME \
	--make_fasta \
	--truncate 1 \
	--trunc_len 800 \
	--toks_per_batch 1024 \
	# --concat_tensors \

cd /procesa
export PYTHONPATH=$PWD
python build_dgl_graph.py \
	--dataroot /datasets/procesa_data/$DATANAME \
	--dataset ${DATANAME} \
	--model ${MODELNAME}

