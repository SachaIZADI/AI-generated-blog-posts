from pathlib import Path
from ai_articles.data import Data

if __name__ == '__main__':
    data = Data()
    data.download(dst=Path(__file__).parent.parent/"ai_articles"/"data"/"posts.csv")
