import torch.nn as nn
import torch.nn.functional as F
from models import LOSSES

@LOSSES.register_module()
class CrossEntropyLoss(nn.Module):
    def __init__(self, loss_weight=1.0):
        super(CrossEntropyLoss, self).__init__()
        self.loss_weight = loss_weight

    def forward(self, pred, target):
        pred = pred.float()
        target = target.long().reshape(-1)  # CrossEntropyLoss expects target to be of type long
        loss = F.cross_entropy(pred, target, reduction='mean') * self.loss_weight
        loss_dict = {'loss_cls': loss}
        return loss_dict
        