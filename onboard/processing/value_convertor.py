import math

class ValueConvertor:
    def __init__(self, convertor):
        self._convertor = convertor

    def convert(self, value):
        if self._convertor is not None:
            return self._convertor.convert(value)
        else:
            return value


class ResistanceValueConvertor(ValueConvertor):
    def __init__(self, v_in, r_ref, convertor=None):
        super().__init__(convertor)
        self._v_in  = v_in
        self._r_ref = r_ref

    def convert(self, value):
        '''
        Converts a voltage to a resistance
        '''
        voltage = super().convert(value)
        return (self._r_ref / ((self._v_in / voltage) - 1))


class TemperatureValueConvertor(ValueConvertor):
    def __init__(self, ref_temp, beta, r_at_ref_temp, convertor=None):
        super().__init__(convertor)
        self._ref_temp = ref_temp
        self._beta = beta
        self._r_at_ref_temp = r_at_ref_temp

    def convert(self, value):
        '''
        Converts a resistance to a temperature
        '''
        resistance = super().convert(value)
        t = 1 / ( 1 / self._ref_temp + 1 / self._beta * math.log(resistance / self._r_at_ref_temp))
        return t

