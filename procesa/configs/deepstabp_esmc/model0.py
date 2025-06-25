model = dict(
    type='GraphModel0',
    in_features=1152,
    loss_reg=dict(type='RMSELoss', loss_weight=1.0),
    loss_triplet=dict(type='TripletLoss', loss_weight=0.01))

seed = 42
num_workers = 4
learning_rate = 1e-4
wd = 0.0

earlystop = True
sep_train_strategy = None
best_metrics = ['spearmanr', 'pearson']

max_epochs = 10
batch_size = 8
lr_config = dict(
    _delete_=True,
    policy='NotChange',
    warmup='linear',
    warmup_steps=70)
