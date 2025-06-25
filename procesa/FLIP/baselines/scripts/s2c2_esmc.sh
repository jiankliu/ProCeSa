export MODELNAME=esmc
DATALIST=(s2c2_0 s2c2_1 s2c2_2 s2c2_3 s2c2_4 s2c2_5 s2c2_6 s2c2_7 s2c2_8 s2c2_9)
NAMELIST=(hotprotein_0 hotprotein_1 hotprotein_2 hotprotein_3 hotprotein_4 hotprotein_5 hotprotein_6 hotprotein_7 hotprotein_8 hotprotein_9)

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
