export ROOTDIR=/procesa
cd $ROOTDIR
export PYTHONPATH=$PWD:$PYTHONPATH
export DATANAME='deepstabp'
export MODELNAME='esmc'
export EXPNAME='model0'
export DATAROOT=/datasets/procesa_data/$DATANAME

export PKLNAME='pkls'

for SEED in 101 400 668
do
	export RESULT_PATH=$ROOTDIR/results/${DATANAME}_${MODELNAME}/seed-${SEED}/${EXPNAME}
	python train.py \
		configs/${DATANAME}_${MODELNAME}/${EXPNAME}.py \
		--result_path $RESULT_PATH \
		--dataroot $DATAROOT \
		--dataname $DATANAME \
		--modelname $MODELNAME \
		--pklname $PKLNAME \
		--seed ${SEED}
done
