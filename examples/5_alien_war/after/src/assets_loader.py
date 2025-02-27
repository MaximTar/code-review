import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

from settings import ASSETS_DIR


class Asset(Enum):
    BACKGROUND = (
        "background.jpg",
        "https://drive.usercontent.google.com/u/0/uc?id=1YeQGIUjfLgv1H5w2Zh5sEInAI8dO1g_s&export=download",
    )
    ALIEN = (
        "alien.png",
        "https://drive.usercontent.google.com/u/0/uc?id=1V2hlAR1hI0gpBC64qsoyol4Q4ejaTCI4&export=download",
    )
    PLAYER = (
        "player.png",
        "https://drive.usercontent.google.com/u/0/uc?id=1fdGfMGHCZ0Pi8jxFCLCQw_Fic_enUISS&export=download",
    )
    BULLET = (
        "bullet.png",
        "https://drive.usercontent.google.com/u/0/uc?id=1YYcBOUPqerpeZ2TxZG4otqr8gBGRgrKc&export=download",
    )
    SHOOT_SOUND = (
        "shoot.wav",
        "https://drive.usercontent.google.com/u/0/uc?id=1detZdbBHrkDLdDdrVm5JzGlC4C8rJKUa&export=download",
    )
    HIT_SOUND = (
        "hit.wav",
        "https://drive.usercontent.google.com/u/0/uc?id=1NxFduvac5PSGSM2mj4d4Q2o5Sijkm34_&export=download",
    )
    EXPLOSION_SOUND = (
        "explosion.wav",
        "https://drive.usercontent.google.com/u/0/uc?id=1VKCV2xWT32-glKj0WT8FQ38otniSsjab&export=download",
    )
    MUSIC = (
        "background.wav",
        "https://drive.usercontent.google.com/u/0/uc?id=1sKO-Xs7nIkTSr-3npNueRjyMD2b_QTQ0&export=download",
    )

    def __init__(self, filename, url):
        self.filename = filename
        self.url = url


def ensure_assets():
    os.makedirs(ASSETS_DIR, exist_ok=True)

    def download_file(asset: Asset):
        path = os.path.join(ASSETS_DIR, asset.filename)
        if not os.path.exists(path):
            print(f"Downloading {asset.filename}...")
            urllib.request.urlretrieve(asset.url, path)

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_file, Asset)


def load_asset(filename):
    return os.path.join(ASSETS_DIR, filename)
