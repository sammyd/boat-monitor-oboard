import unittest
from unittest.mock import Mock
from onboard.processing.value_convertor import ValueConvertor, ResistanceValueConvertor, TemperatureValueConvertor

class TestValueConvertor(unittest.TestCase):
    def setUp(self):
        self.mock_vc = Mock()

    def test_ConvertReturnsValueWhenNotDecorated(self):
        vc = ValueConvertor(None)
        self.assertEqual(10, vc.convert(10))

    def test_ConvertChainsMethodCallsAppropriately(self):
        vc = ValueConvertor(self.mock_vc)
        vc.convert(10)
        self.mock_vc.convert.assert_called_once_with(10)


class TestResistanceValueConvertor(unittest.TestCase):
    def test_ConvertorChainingWorksAsExpected(self):
        mock_vc = Mock()
        mock_vc.convert.return_value = 5
        rvc = ResistanceValueConvertor(10, 10, mock_vc)
        rvc.convert(5)
        mock_vc.convert.assert_called_once_with(5)

    def test_ConstructorDoesntRequireConvertor(self):
        rvc = ResistanceValueConvertor(10, 10)
        rvc.convert(5)


class TestTemperatureValueConvertor(unittest.TestCase):
    def test_ConvertorChainingWorksAsExpected(self):
        mock_vc = Mock()
        mock_vc.convert.return_value = 5
        tvc = TemperatureValueConvertor(10, 10, 10, mock_vc)
        tvc.convert(5)
        mock_vc.convert.assert_called_once_with(5)

    def test_ConstructorDoesntRequireConvertor(self):
        tvc = TemperatureValueConvertor(10, 10, 10)
        tvc.convert(5)