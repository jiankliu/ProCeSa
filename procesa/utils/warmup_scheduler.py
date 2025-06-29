import math
from contextlib import contextmanager
from torch.optim import Optimizer


class BaseWarmup(object):
    """Base class for all warmup schedules

    Arguments:
        optimizer (Optimizer): an instance of a subclass of Optimizer
        warmup_params (list): warmup paramters
        last_step (int): The index of last step. (Default: -1)
    """

    def __init__(self, optimizer, warmup_params, last_step=-1):
        if not isinstance(optimizer, Optimizer):
            raise TypeError('{} is not an Optimizer'.format(
                type(optimizer).__name__))
        self.optimizer = optimizer
        self.warmup_params = warmup_params
        self.last_step = last_step
        self.lrs = [group['lr'] for group in self.optimizer.param_groups]
        self.dampen()

    def state_dict(self):
        """Returns the state of the warmup scheduler as a :class:`dict`.

        It contains an entry for every variable in self.__dict__ which
        is not the optimizer.
        """
        return {key: value for key, value in self.__dict__.items() if key != 'optimizer'}

    def load_state_dict(self, state_dict):
        """Loads the warmup scheduler's state.

        Arguments:
            state_dict (dict): warmup scheduler state. Should be an object returned
                from a call to :meth:`state_dict`.
        """
        self.__dict__.update(state_dict)

    def dampen(self, step=None):
        """Dampen the learning rates.

        Arguments:
            step (int): The index of current step. (Default: None)
        """
        if step is None:
            step = self.last_step + 1
        self.last_step = step

        for group, params in zip(self.optimizer.param_groups, self.warmup_params):
            omega = self.warmup_factor(step, **params)
            group['lr'] *= omega

    @contextmanager
    def dampening(self):
        for group, lr in zip(self.optimizer.param_groups, self.lrs):
            group['lr'] = lr
        yield
        self.lrs = [group['lr'] for group in self.optimizer.param_groups]
        self.dampen()

    def warmup_factor(self, step, **params):
        raise NotImplementedError


def get_warmup_params(warmup_period, group_count):
    if type(warmup_period) == list:
        if len(warmup_period) != group_count:
            raise ValueError(
                'size of warmup_period does not equal {}.'.format(group_count))
        for x in warmup_period:
            if type(x) != int:
                raise ValueError(
                    'An element in warmup_period, {}, is not an int.'.format(
                        type(x).__name__))
        warmup_params = [dict(warmup_period=x) for x in warmup_period]
    elif type(warmup_period) == int:
        warmup_params = [dict(warmup_period=warmup_period)
                         for _ in range(group_count)]
    else:
        raise TypeError('{} is not a list nor an int.'.format(
            type(warmup_period).__name__))
    return warmup_params


class LinearWarmup(BaseWarmup):
    """Linear warmup schedule.

    Arguments:
        optimizer (Optimizer): an instance of a subclass of Optimizer
        warmup_period (int or list): Warmup period
        last_step (int): The index of last step. (Default: -1)
    """

    def __init__(self, optimizer, warmup_period, last_step=-1):
        self.warmup_steps = warmup_period
        group_count = len(optimizer.param_groups)
        warmup_params = get_warmup_params(warmup_period, group_count)
        super(LinearWarmup, self).__init__(optimizer, warmup_params, last_step)

    def warmup_factor(self, step, warmup_period):
        return min(1.0, (step+1) / warmup_period)

if __name__ == '__main__':
    from torchvision.models import resnet50
    from torch.optim.lr_scheduler import CosineAnnealingLR, MultiStepLR
    from torch.optim import SGD
    
    model = resnet50()
    optimizer = SGD(model.parameters(), lr=0.1)
    warmup_steps = 50
    steps_per_epoch = 91
    # scheduler = CosineAnnealingLR(optimizer, T_max=10*91-warmup_steps, eta_min=0.001)
    scheduler = MultiStepLR(optimizer, milestones=[6 * steps_per_epoch,8 * steps_per_epoch], gamma=0.1)
    warmup_scheduler = LinearWarmup(optimizer, warmup_period=warmup_steps)
    
    epochs = 10
    with open("lr.log", 'w') as f:
        for epoch in range(epochs):
            for k in range(steps_per_epoch):
                optimizer.step()
                optimizer.zero_grad()
                with warmup_scheduler.dampening():
                    if warmup_scheduler.last_step + 1 >= warmup_steps:
                        scheduler.step()
                f.write(f"{epoch*91+k},{optimizer.param_groups[-1]['lr']}\n")