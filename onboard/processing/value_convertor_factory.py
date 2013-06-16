from onboard.processing.value_convertor import ValueConvertor, ResistanceValueConvertor, TemperatureValueConvertor

class ValueConvertorFactory:
    def create_value_convertor(self, type, properties):
        raise NotImplementedError


class OnboardValueConvertorFactory:
    def create_value_convertor(self, type, properties):
        if(type == "resistance"):
            return self._create_resistance_convertor(properties)
        elif(type == "temperature"):
            return self._create_temperature_convertor(properties)
        else:
            return ValueConvertor()


    def _create_resistance_convertor(self, properties):
        return ResistanceValueConvertor(properties['v_in'],
            properties['r_ref'])



    def _create_temperature_convertor(self, properties):
        res = self._create_resistance_convertor(properties)
        temp = TemperatureValueConvertor(properties['ref_temp'],
            properties['beta'],
            properties['r_at_ref_temp'],
            convertor=res)
        return temp
