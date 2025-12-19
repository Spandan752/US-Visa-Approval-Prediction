import pandas as pd
from us_visa.exceptions import CustomException
from us_visa.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1
    def _asdict(self):
        return self._asdict
    def reverse_mapping(self):
        mapping_result = self._asdict()
        return dict(zip(mapping_result.values(), mapping_result.keys()))