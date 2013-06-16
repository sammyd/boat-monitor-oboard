import unittest
from onboard.input.gpio_input import PiADCInput

class TestPiADCInput(unittest.TestCase):

    def test_InvalidAccuraciesThrow(self):
        self.assertRaises(ValueError, PiADCInput, [0], 13)
        self.assertRaises(ValueError, PiADCInput, [0], 10)

    def test_ValidAccuraciesAreAccepted(self):
        try:
            PiADCInput([0], 12)
            PiADCInput([0], 14)
            PiADCInput([0], 16)
            PiADCInput([0], 18)
        except ValueError:
            self.fail("Valid Accuracies should be allowed")

    def test_InvalidChannelsThow(self):
        self.assertRaises(ValueError, PiADCInput, [], 12)
        self.assertRaises(ValueError, PiADCInput, [-1], 12)
        self.assertRaises(ValueError, PiADCInput, [8], 12)
        self.assertRaises(ValueError, PiADCInput, [1.5], 12)

    def test_ValidChannelsAreAccepted(self):
        try:
            PiADCInput([0,1,2,3,4,5,6,7], 12)
            PiADCInput([3], 12)
        except ValueError:
            self.fail("Valid channels should be accepted")

    def test_DivisorMethodWorksCorrectly(self):
        lookup_table = [(12, 1), (14, 4), (16, 16), (18, 64)]
        for kv in lookup_table:
            adc = PiADCInput([0], kv[0])
            self.assertEqual(kv[1], adc._divisor())

    def test_ADCConfigMethodReturnsCorrectAddresses(self):
        lookup_table = [0x68, 0x68, 0x68, 0x68, 0x69, 0x69, 0x69, 0x69]
        adc = PiADCInput([0], 12)
        for i in range(0, len(lookup_table)):
            self.assertEqual(lookup_table[i], adc._adcConfig(i)[0])

    def test_ADCConfigMethodReturnsCorrectConfigMask(self):
        lookup_table = [(0, 12, 0x90), (0, 14, 0x94), (0, 16, 0x98), (0, 18, 0x9C),
                        (1, 12, 0xB0), (1, 14, 0xB4), (1, 16, 0xB8), (1, 18, 0xBC),
                        (2, 12, 0xD0), (2, 14, 0xD4), (2, 16, 0xD8), (2, 18, 0xDC),
                        (3, 12, 0xF0), (3, 14, 0xF4), (3, 16, 0xF8), (3, 18, 0xFC)]
        for i in range(0,2):
            for j in lookup_table:
                adc = PiADCInput([0], j[1])
                self.assertEqual(j[2], adc._adcConfig(4*i + j[0])[1])