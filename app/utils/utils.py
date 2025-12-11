from typing import List

def split_list(lst: List, size: int):
    return [lst[i:i + size] for i in range(0, len(lst), size)]
