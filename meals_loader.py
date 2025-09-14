from typing import List, Dict, Any
import json

def load_meals(path: str) -> list[dict[str, any]]:
    with open(path,'r',encoding='utf-8') as f:
        return json.load(f)
