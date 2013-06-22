# Wrap this import in a try/catch so we can run unit tests not on device
try:
    import quick2wire.i2c as i2c
except:
    print("Module not found")

class PiADCInput:
    def __init__(self, channels, accuracy):
        '''
        Channel is an array containing integers of the channels to sample. Values
        are in the range [0,7].
        Accuracy is the number of bits to which the samples are measured. Allowed
        values are in the set {18, 16, 14, 12}
        '''
        if len(channels) < 1:
            raise ValueError
        allowed_channels = range(0,8)
        for channel in channels:
            if channel not in allowed_channels:
                raise ValueError
        self._channels = channels

        allowed_accuracies = [12, 14, 16, 18]
        if accuracy not in allowed_accuracies:
            raise ValueError
        self._accuracy = accuracy

        self._adcAddresses = [0x68, 0x69]

    def getSamples(self):
        results = {}
        varDivisior = self._divisor()
        varMultiplier = ( 2.4705882 / varDivisior) / 1000
        try:
            with i2c.I2CMaster() as bus:
                for channel in self._channels:
                    (address, adcConfig) = self._adcConfig(channel)
                    bus.transaction(i2c.writing_bytes(address, adcConfig))
                    h, m, l ,s = bus.transaction(i2c.reading(address,4))[0]
                    while (s & 128):
                        h, m, l, s  = bus.transaction(i2c.reading(address,4))[0]
                    # shift bits to product result
                    t = ((h & 0b00000001) << 16) | (m << 8) | l
                    # check if positive or negative number and invert if needed
                    if (h > 128):
                        t = ~(0x020000 - t)
                    results[channel] = t * varMultiplier
        except:
            print("There was a problem")


    def _divisor(self):
        return pow(4, (self._accuracy / 2 - 6))

    def _adcConfig(self, channel):
        '''
        Channel is in [0,7]. Returns a tuple of (address, adcConfig)
        '''
        if channel < 4:
            address = self._adcAddresses[0]
        else:
            address = self._adcAddresses[1]
            channel -= 4

        # Now we fiddle around with the values a little
        channel_start_config = 0x90 + channel * 0x20
        accuracy_offset = (self._accuracy / 2 - 6)
        adcConfig = channel_start_config + 4 * accuracy_offset
        return (address, adcConfig)

