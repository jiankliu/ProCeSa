export ROOTDIR=/procesa
cd $ROOTDIR
export PYTHONPATH=$PWD:$PYTHONPATH
export MODELNAME='esmc'
export EXPNAME='model0'
export DATAROOT=/datasets/procesa_data/hotprotein
export TASK=cls
export DATANAME=S
for SEED in  101 400 668 
do
	export RESULT_PATH=$ROOTDIR/results/${DATANAME}_${MODELNAME}_${TASK}/seed-${SEED}/${EXPNAME}
	python train.py \
		configs/${DATANAME}_${MODELNAME}_${TASK}/${EXPNAME}.py \
		--result_path $RESULT_PATH \
		--dataroot $DATAROOT \
		--dataname $DATANAME \
		--modelname $MODELNAME \
		--seed ${SEED} \
		--task ${TASK}
done
