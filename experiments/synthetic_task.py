import torch
from config import get_device
import itertools
from utils.sae_trainer import SAETrainer
from utils.data_utils import generate_synthetic_data
from utils.general_utils import find_combinations
from torch.utils.data import DataLoader, TensorDataset
import os
from models.sae import SparseAutoencoder


def train_synthetic_sae(params, true_features, train_loader):
    model = torch.compile(SparseAutoencoder(params))
    device = get_device()
    trainer = SAETrainer(model, device, params, true_features)
    
    trainer.train(train_loader, params["num_epochs"])


def run(device, config):
    dataset_path = 'synthetic_dataset.pt'
    true_features_path = 'true_features.pt'

    if os.path.exists(dataset_path) and os.path.exists(true_features_path):
        train_dataset = torch.load(dataset_path)
        true_features = torch.load(true_features_path)
    else:
        train_data, true_features = generate_synthetic_data(config, device=device)
        train_dataset = TensorDataset(train_data)
        torch.save(train_dataset, dataset_path)
        torch.save(true_features, true_features_path)

    train_loader = DataLoader(train_dataset, batch_size=config['training_batch_size'],
                              num_workers=2, pin_memory=True, prefetch_factor=2, shuffle=True)

    parameter_grid = {k: [v] if not isinstance(v, list) else v for k, v in config.items()
                      if k in ['learning_rate', 'input_size', 'k_sparse', 'num_epochs', 'hidden_size', 'penalize_proportion', 'num_saes', 'ensemble_consistency_weight', 'auxiliary_loss_weight']}

    return [train_synthetic_sae(params, true_features, train_loader)
            for params in find_combinations(parameter_grid)]
