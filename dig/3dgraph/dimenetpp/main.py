import torch
import time
import numpy as np
from model import dimenetpp
import argparse
from train import run
import sys
sys.path.append('..')
from utils import load_qm9, load_md17

parser = argparse.ArgumentParser()

parser.add_argument('--dataset', type=str, default="qm9", help='dataset name') # qm9, aspirin, benzene, ethanol, malonaldehyde, naphthalene, salicylic, toluene, uracil
parser.add_argument('--target', type=str, default='U0') # For QM9, the target can be mu, aplha, homo, lumo, gap, r2, zpve, U0, U, H, G, Cv.
parser.add_argument('--num_task', type=int, default=1)
parser.add_argument('--output_init', type=str, default='GlorotOrthogonal') # in DimeNet++, for QM9, 'zeros' for mu, homo, lumo, and zpve; 'GlorotOrthogonal' for alpha, R2, U0, U, H, G, and Cv

parser.add_argument('--save_dir', type=str, default='../trained_models/')
parser.add_argument('--log_dir', type=str, default='../logs/')

parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--epochs', type=int, default=300)
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--lr_decay_factor', type=float, default=0.5)
parser.add_argument('--lr_decay_step_size', type=int, default=50)
parser.add_argument('--weight_decay', type=float, default=0)

parser.add_argument('--energy_and_force', type=bool, default=False)
parser.add_argument('--num_atom', type=int, default=1)
parser.add_argument('--p', type=int, default=100)

parser.add_argument('--cutoff', type=float, default=5.0)
parser.add_argument('--num_layer', type=int, default=4)
parser.add_argument('--hidden_channels', type=int, default=128)
parser.add_argument('--int_emb_size', type=int, default=64)
parser.add_argument('--basis_emb_size', type=int, default=8)
parser.add_argument('--out_emb_size', type=int, default=256)
parser.add_argument('--num_spherical', type=int, default=7)
parser.add_argument('--num_radial', type=int, default=6)

args = parser.parse_args()
print('Loading data')
t_start = time.perf_counter()
if args.dataset == 'qm9':
    train_size = 110000
    val_size = 10000
    train_dataset, val_dataset, test_dataset = load_qm9(args.dataset, args.target, train_size, val_size)
    t_end = time.perf_counter()
    print('time',t_end-t_start)
    print('Loaded data')

elif args.dataset in ['aspirin', 'benzene', 'ethanol', 'malonaldehyde', 'naphthalene', 'salicylic', 'toluene', 'uracil']: #md17
    train_size = 1000
    val_size = 10000
    train_dataset, val_dataset, test_dataset, num_atom = load_md17(args.dataset, train_size, val_size)
    args.energy_and_force = True
    args.num_atom = num_atom
    t_end = time.perf_counter()
    print('time',t_end-t_start)
    print('Loaded data')

else:
    print("This dataset name is not supported!")

print(args)
print('Loading model')
model = dimenetpp(args.energy_and_force, args.cutoff, args.num_layer, args.hidden_channels, args.num_task, args.int_emb_size, args.basis_emb_size, args.out_emb_size, args.num_spherical, args.num_radial, output_init=args.output_init)
print('Loaded model')
run(train_dataset, val_dataset, test_dataset, args.save_dir, args.log_dir, model, args.epochs, args.batch_size, args.lr, args.lr_decay_factor, args.lr_decay_step_size, args.weight_decay, args.energy_and_force, args.num_atom, args.p)