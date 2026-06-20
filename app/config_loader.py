import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / 'config.json'
DEFAULTS = json.loads((ROOT / 'config.example.json').read_text())

def load_config():
    if CONFIG_PATH.exists():
        try:
            user_cfg = json.loads(CONFIG_PATH.read_text())
        except Exception:
            user_cfg = {}
    else:
        user_cfg = {}
    cfg = DEFAULTS.copy()
    cfg.update(user_cfg)
    cfg['root_dir'] = str(ROOT)
    cfg['dataset_dir'] = str(ROOT / 'dataset')
    cfg['models_dir'] = str(ROOT / 'models')
    cfg['logs_dir'] = str(ROOT / 'logs')
    cfg['db_path'] = str(ROOT / 'logs' / 'events.db')
    cfg['latest_intruder_image'] = str(ROOT / 'static' / 'latest_intruder.jpg')
    for d in ['dataset_dir','models_dir','logs_dir']:
        os.makedirs(cfg[d], exist_ok=True)
    return cfg
