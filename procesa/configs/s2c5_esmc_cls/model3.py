model = dict(
    type='GraphModel65',
    num_classes=5,
    loss_cls=dict(type='CrossEntropyLoss', loss_weight=1.0),
    loss_triplet=dict(type='TripletLoss', loss_weight=1))

batch_size = 4
max_epochs = 10
seed = 42
num_workers = 4
learning_rate = 8e-5
wd = 0.0
lr_config = dict(
    policy='NotChange')
earlystop = True
sep_train_strategy = None
best_metrics = [
        'acc', 'prec-w', 'rec-w', 'f1-w',
        'prec-ma', 'rec-ma', 'f1-ma',
        'prec-mi', 'rec-mi', 'f1-mi']
