import unittest

from onboard.processing.value_convertor_factory import OnboardValueConvertorFactory


class TestOnboardValueConvertorFactory(unittest.TestCase):

    def setUp(self):
        self._factory = OnboardValueConvertorFactory()
        self._validProperties = { 'v_in' : 12, 'r_ref': 2400, 'beta': 1.23,
                                  'ref_temp': 25, 'r_at_ref_temp' : 240 }


    def test_resistanceRequiresCorrectProperties(self):
        try:
            self._factory.create_value_convertor("resistance", self._validProperties)
        except:
            self.fail("Resistance creator shouldn't throw")

    def test_resistanceRequiresInputVoltage(self):
        self._validProperties.pop('v_in')
        self.assertRaises(KeyError, self._factory.create_value_convertor, "resistance", self._validProperties)

    def test_resistanceRequiresRefResistance(self):
        self._validProperties.pop('r_ref')
        self.assertRaises(KeyError, self._factory.create_value_convertor, "resistance", self._validProperties)

    def test_temperatureRequiresInputVoltage(self):
        self._validProperties.pop('v_in')
        self.assertRaises(KeyError, self._factory.create_value_convertor, "temperature", self._validProperties)

    def test_temperatureRequiresRefResistance(self):
        self._validProperties.pop('r_ref')
        self.assertRaises(KeyError, self._factory.create_value_convertor, "temperature", self._validProperties)

    def test_temperatureRequiresBeta(self):
        self._validProperties.pop('beta')
        self.assertRaises(KeyError, self._factory.create_value_convertor, "temperature", self._validProperties)

    def test_temperatureRequiresRefTemp(self):
        self._validProperties.pop('ref_temp')
        self.assertRaises(KeyError, self._factory.create_value_convertor, "temperature", self._validProperties)

    def test_temperatureRequiresResistanceAtRefTemp(self):
        self._validProperties.pop('r_at_ref_temp')
        self.assertRaises(KeyError, self._factory.create_value_convertor, "temperature", self._validProperties)
    
