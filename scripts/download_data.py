from pathlib import Path
from nlp_finetuning.data import Data

if __name__ == '__main__':
    data = Data()
    data.download(dst=Path(__file__).parent.parent/"nlp_finetuning"/"data"/"posts.csv")
