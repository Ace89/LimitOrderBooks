
from enum import Enum


class TimeSeriesTypes(Enum):
    price = 'price'
    size = 'size'
    mid_price = 'mid_price'
    imbalance = 'imbalance'
    full_size = 'full_size'
