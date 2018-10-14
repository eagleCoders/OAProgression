import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default='')
    parser.add_argument('--snapshots', default='')
    parser.add_argument('--logs', default='')
    parser.add_argument('--backbone', type=str, choices=['seresnet50'], default='seresnet50')
    parser.add_argument('--optimizer', type=str, choices=['adam', 'sgd'], default='adam')
    parser.add_argument('--bs', type=int, default=64)
    parser.add_argument('--val_bs', type=int, default=96)
    parser.add_argument('--n_folds', type=int, default=5)
    parser.add_argument('--fold', type=int, default=-1)
    parser.add_argument('--n_epochs', type=int, default=40)
    parser.add_argument('--n_threads', type=int, default=12)
    parser.add_argument('--start_val', type=int, default=-1)
    parser.add_argument('--loss_weight', type=float, default=0.5)
    parser.add_argument('--unfreeze_epoch', type=int, default=5)
    parser.add_argument('--crop_y', type=int, default=512)
    parser.add_argument('--lr', type=float, default=1e-2)
    parser.add_argument('--lr_drop', default=[10, 20, 30])
    parser.add_argument('--wd', type=float, default=5e-5)
    parser.add_argument('--seed', type=int, default=445789)
    args = parser.parse_args()

    return args
