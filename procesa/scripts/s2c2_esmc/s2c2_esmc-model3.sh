export ROOTDIR=/procesa
cd $ROOTDIR
export PYTHONPATH=$PWD:$PYTHONPATH
export MODELNAME='esmc'
export EXPNAME='model3'
export DATAROOT=/datasets/procesa_data/hotprotein

for DATANAME in s2c2_0 s2c2_1 s2c2_2 s2c2_3 s2c2_4 s2c2_5 s2c2_6 s2c2_7 s2c2_8 s2c2_9
do
	for SEED in 101 400 668
	do
		export RESULT_PATH=$ROOTDIR/results/${DATANAME}_${MODELNAME}/seed-${SEED}/${EXPNAME}
		python train.py \
			configs/${DATANAME:0:4}_${MODELNAME}/${EXPNAME}.py \
			--result_path $RESULT_PATH \
			--dataroot $DATAROOT \
			--dataname $DATANAME \
			--modelname $MODELNAME \
			--seed ${SEED}
	done
done
