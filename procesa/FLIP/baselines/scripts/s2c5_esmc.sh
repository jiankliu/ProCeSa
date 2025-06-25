export MODELNAME=esmc
DATALIST=(s2c5_0 s2c5_1 s2c5_2 s2c5_3 s2c5_4 s2c5_5 s2c5_6 s2c5_7 s2c5_8 s2c5_9)
NAMELIST=(hotprotein_10 hotprotein_11 hotprotein_12 hotprotein_13 hotprotein_14 hotprotein_15 hotprotein_16 hotprotein_17 hotprotein_18 hotprotein_19)

for i in "${!DATALIST[@]}"
do
	cd /procesa/FLIP/baselines
	export PYTHONPATH=$PWD
	DATANAME=${DATALIST[i]}
	KEYNAME=${NAMELIST[i]}
	python embeddings/embeddings.py \
		${KEYNAME} \
		$MODELNAME \
		--datadir /datasets/procesa_data/ \
		--bulk_compute \
		--outdir /datasets/procesa_data/hotprotein/$DATANAME/$MODELNAME \
		--make_fasta \
		--truncate 1 \
		--trunc_len 800 \
		--toks_per_batch 1024 \
		# --concat_tensors \
	
	cd /procesa 
	export PYTHONPATH=$PWD
	python build_dgl_graph.py \
		--dataroot /datasets/procesa_data/hotprotein \
		--dataset ${DATANAME} \
		--model ${MODELNAME}

done
