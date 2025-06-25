export ROOTDIR=/procesa
cd $ROOTDIR
export PYTHONPATH=$PWD:$PYTHONPATH
export MODELNAME='esmc'
export EXPNAME='model3'
export DATAROOT=/datasets/procesa_data/hotprotein
export DATANAME=S

for SEED in 101 400 668
do
	export RESULT_PATH=$ROOTDIR/results/${DATANAME}_${MODELNAME}/seed-${SEED}/${EXPNAME}
	python train.py \
		configs/${DATANAME}_${MODELNAME}/${EXPNAME}.py \
		--result_path $RESULT_PATH \
		--dataroot $DATAROOT \
		--dataname $DATANAME \
		--modelname $MODELNAME \
		--seed ${SEED}
done
