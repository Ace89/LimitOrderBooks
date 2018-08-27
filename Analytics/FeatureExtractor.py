"""
For my class feature extractor

Have features as delegates which user can plug in and play

"""


class FeatureExtractor:

    def __init__(self, data):
        self.data = data

    def extract_feature(self, feature):
        # feature must be of a particular type and accept a data frame
        # use interfaces
        time_series = feature(self.data)
