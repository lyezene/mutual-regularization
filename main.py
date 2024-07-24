import argparse
import yaml
import wandb
from config import get_device
from experiments import synthetic_task, feature_correlation, sae_3d_visualization
from utils.data_utils import generate_synthetic_data
import traceback

def load_config(config_path):
    if config_path:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    else:
        return {}

def init_wandb(config):
    default_config = {
        'project': 'alignment_regularization',
        'config': config
    }
    wandb.init(**default_config)

def run_experiment(config):
    init_wandb(config)
    device = get_device()
    try:
        if config['experiment'] == 'synthetic':
            print("Running Synthetic Experiment...")
            synthetic_task.run(device, config)
        elif config['experiment'] == 'feature_correlation':
            print("Running Feature Correlation Experiment...")
            feature_correlation.run(device, config)
        elif config['experiment'] == 'sae_3d_visualization':
            print("Running SAE 3D Visualization Experiment...")
            sae_3d_visualization.run(device, config)
        else:
            print(f"Unknown experiment: {config['experiment']}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()
    finally:
        wandb.finish()

def main():
    parser = argparse.ArgumentParser(description='Run experiments or generate datasets')
    parser.add_argument('--config', type=str, help='Path to the configuration file for experiments or dataset generation')
    args = parser.parse_args()
    
    if args.config:
        config = load_config(args.config)
        run_experiment(config)
    else:
        print("Error: No configuration file specified. Please provide a configuration file using --config.")

if __name__ == '__main__':
    main()
