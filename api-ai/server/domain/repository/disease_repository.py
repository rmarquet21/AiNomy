from abc import abstractmethod


class DiseaseRepository:

    @abstractmethod
    def get_disease_by_name(self, disease: str):
        """
        Get the details of the disease.

        :param disease: The disease.
        :return: The details of the disease.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_diseases(self):
        """
        Get the list of diseases.

        :return: The list of diseases.
        """
        raise NotImplementedError()
