"""save the data into db"""
import os
from typing import List, Dict
import pickle
from copy import deepcopy
from type import DataNodeStatus
import dataclasses


class DB:
    """abstract class for save and search data"""
    def save(self, key: str, value: DataNodeStatus):
        raise NotImplementedError

    def get(self, key: str) -> List[DataNodeStatus]:
        raise NotImplementedError

    def get_all(self) -> Dict[str, List[DataNodeStatus]]:
        raise NotImplementedError


class MemoryDB(DB):
    """save data to the memory"""

    def get_all(self) -> Dict[str, List[DataNodeStatus]]:
        return deepcopy(self.memory_cache)

    def __init__(self):
        self.memory_cache: Dict[str, List[DataNodeStatus]] = {}

    def save(self, key: str, value: DataNodeStatus):
        """save data to the memory"""
        if key not in self.memory_cache:
            self.memory_cache[key] = []
        self.memory_cache[key].append(value)

    def get(self, key: str) -> List[DataNodeStatus]:
        if key not in self.memory_cache:
            return []
        return self.memory_cache[key]


class FileDB(DB):
    """save data to be json file"""

    def get_all(self) -> Dict[str, List[DataNodeStatus]]:
        """read data from the json file"""
        with open(self.file, 'rb') as f:
            data: Dict[str, List[DataNodeStatus]] = pickle.load(f)
            return data

    def __init__(self, file: str):
        self.file: str = file

        # init the json file
        if not os.path.exists(file):
            with open(file, 'wb') as f:
                pickle.dump({}, f)

    def save(self, key: str, value: DataNodeStatus):
        """read data from the json file"""
        with open(self.file, 'rb') as f:
            data: Dict[str, List[DataNodeStatus]] = pickle.load(f)
            if key not in data:
                data[key] = []
            data[key].append(value)

        # save data into the json file
        with open(self.file, 'wb') as f:
            pickle.dump(data, f)

    def get(self, key: str) -> List[DataNodeStatus]:
        """read data from the json file"""
        with open(self.file, 'rb') as f:
            data: Dict[str, List[DataNodeStatus]] = pickle.load(f)
            if key not in data:
                data[key] = []
            return data[key]
