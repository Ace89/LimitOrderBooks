
from Enums.NonLinearModel import NonLinearModel
from Analytics.GarchModel import GarchModel


class NonLinearModelFactory:

    def __init__(self):
        None

    def get_non_linear_model(self, non_linear_model):

        if non_linear_model == NonLinearModel.Garch:
            return GarchModel()

        return None
