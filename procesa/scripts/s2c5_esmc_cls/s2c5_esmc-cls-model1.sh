export ROOTDIR=/procesa
cd $ROOTDIR
export PYTHONPATH=$PWD:$PYTHONPATH
export MODELNAME='esmc'
export EXPNAME='model1'
export DATAROOT=/datasets/procesa_data/hotprotein
export TASK=cls

for DATANAME in s2c5_0 s2c5_1 s2c5_2 s2c5_3 s2c5_4 s2c5_5 s2c5_6 s2c5_7 s2c5_8 s2c5_9
do
	for SEED in 101 400 668
	do
		export RESULT_PATH=$ROOTDIR/results/${DATANAME}_${MODELNAME}_$TASK/seed-${SEED}/${EXPNAME}
		python train.py \
			configs/${DATANAME:0:4}_${MODELNAME}_$TASK/${EXPNAME}.py \
			--result_path $RESULT_PATH \
			--dataroot $DATAROOT \
			--dataname $DATANAME \
			--modelname $MODELNAME \
			--seed ${SEED} \
			--task $TASK
	done
done
