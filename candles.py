class SingleCandleStick(object):

    __slots__ = ['__open', '__high', '__low', '__close', '__volume']

    def __init__(self, ohlcv: dict):
        try:
            self.__open = float(ohlcv["1. open"])
            self.__high = float(ohlcv["2. high"])
            self.__low = float(ohlcv["3. low"])
            self.__close = float(ohlcv["4. close"])
            self.__volume = float(ohlcv["5. volume"])
        except KeyError:
            print("Error: Invalid OHLCV data(Single candle stick).")

    @property
    def ohlvc_value(self):
        return {"1. open": self.__open,
                "2. high": self.__high,
                "3. low": self.__low,
                "4. high": self.__close,
                "5. volume": self.__volume}

    @ohlvc_value.setter
    def ohlvc_value(self, ohlcv: dict):
        try:
            self.__open = float(ohlcv["1. open"])
            self.__high = float(ohlcv["2. high"])
            self.__low = float(ohlcv["3. low"])
            self.__close = float(ohlcv["4. close"])
            self.__volume = float(ohlcv["5. volume"])
        except KeyError:
            print("Error: Invalid OHLCV data")

    @ohlvc_value.getter
    def ohlvc_value(self):

        marubozu = self.__marubozu()
        spinnig_top = self.spinnig_top()
        hammer = self.__hammer()
        shooting_star = self.__shooting_star()

        if marubozu is not False:
            return "marubozu", marubozu
        elif spinnig_top is not False:
            return "spinning_top", spinnig_top
        elif hammer is not False:
            return "hammer", hammer
        elif shooting_star is not False:
            return "shooting_star", shooting_star
        else:
            return 0, 0

    def length(self):
        b_length = (max(self.__open, self.__close) - min(self.__open, self.__close)) + 0.0001
        w_length = abs(self.__high - self.__low) + 0.0001
        up_w_length = (self.__high - max(self.__open, self.__close)) + 0.0001
        low_w_length = (min(self.__open, self.__close) - self.__low) + 0.0001
        return b_length, w_length, up_w_length, low_w_length

    def __marubozu(self):
        # unpacking the tupple(b_length, w_length)
        body_length = self.length()[0]
        wick_length = self.length()[1]

        if body_length / wick_length > 0.95:
            if self.__open < self.__close:
                return "Bullish"
            else:
                return "Bearish"
        else:
            return False

    def spinnig_top(self):
        bd_length, wick_length, up_wick, low_wick = self.length()

        wick_ratio = min(up_wick, low_wick)/max(up_wick, low_wick)
        if (bd_length / wick_length) < 0.02 and (wick_ratio < 0.05):
            return True
        else:
            return False

    def __hammer(self):
        bd_length, wick_length, up_wick, low_wick = self.length()

        if ((up_wick/2) < bd_length) and (low_wick > (3*bd_length)):
            if self.__open < self.__close:
                return "Bullish"
            else:
                return "Bearish"
        else:
            return False

    def __shooting_star(self):
        bd_length, wick_length, up_wick, low_wick = self.length()

        if((low_wick/2) < bd_length) and (up_wick > (3*bd_length)):
            if self.__open < self.__close:
                return "Bullish"
            else:
                return "Bearish"
        else:
            return False


class DoubleCandleStick(SingleCandleStick):

    __slots__ = ['__open1', '__high1', '__low1', '__close1', '__volume1', '__open2', '__high2', '__low2', '__close2', '__volume2']

    def __init__(self, candle1: dict, candle2: dict):
        super().__init__(candle1)
        try:
            self.__open1 = float(candle1["1. open"])
            self.__high1 = float(candle1["2. high"])
            self.__low1 = float(candle1["3. low"])
            self.__close1 = float(candle1["4. close"])
            self.__volume1 = float(candle1["5. volume"])

            self.__open2 = float(candle2["1. open"])
            self.__high2 = float(candle2["2. high"])
            self.__low2 = float(candle2["3. low"])
            self.__close2 = float(candle2["4. close"])
            self.__volume2 = float(candle2["5. volume"])
        except KeyError:
            print("Invalid OHLCV data (Double Canlde stick)")

    @property
    def patten_detect(self):
        return {"candle1": {"1. open": self.__open1,
                            "2. high": self.__high1,
                            "3. low": self.__low1,
                            "4. close": self.__close1,
                            "5. volume": self.__volume1},
                "candle2": {"1. open": self.__open2,
                            "2. high": self.__high2,
                            "3. low": self.__low2,
                            "4. close": self.__close2,
                            "5. volume": self.__volume2}}

    @patten_detect.setter
    def patten_detect(self, candle1: dict, candle2: dict):
        try:
            self.__open1 = float(candle1["1. open"])
            self.__high1 = float(candle1["2. high"])
            self.__low1 = float(candle1["3. low"])
            self.__close1 = float(candle1["4. close"])
            self.__volume1 = float(candle1["5. volume"])

            self.__open2 = float(candle2["1. open"])
            self.__high2 = float(candle2["2. high"])
            self.__low2 = float(candle2["3. low"])
            self.__close2 = float(candle2["4. close"])
            self.__volume2 = float(candle2["5. volume"])
        except KeyError:
            print("Invalid OHLCV data ")

    # @patten_detect.getter
    def get_value(self):
        engulfing = self.engulfing()
        piercing = self.piercing()
        dark_cloud = self.dark_cloud()
        harami = self.harami()
        gap = self.gap()

        if engulfing is not False:
            return "engulfing", engulfing
        if piercing is not False:
            return "piercing", piercing
        elif dark_cloud is not False:
            return "dark_cloud", dark_cloud
        elif harami is not False:
            return "harami", harami
        elif gap is not False:
            return "gap", gap
        else:
            return 0, 0

    def engulfing(self):
        c1_bd_len, c1_wick_len, c1_up_wick, c1_lo_wick = SingleCandleStick(self.patten_detect["candle1"]).length()
        c2_bd_len, c2_wick_len, c2_up_wick, c2_lo_wick = SingleCandleStick(self.patten_detect["candle2"]).length()

        if (c1_bd_len < c2_bd_len) and (self.__close1 > self.__open2) and (self.__open1 < self.__close2):
            return "Bullish"
        elif (c1_bd_len < c2_bd_len) and (self.__open1 > self.__close2) and (self.__close1 < self.__open2):
            return "Bearish"
        else:
            return False

    def piercing(self):
        c1_bd_len, c1_wick_len, c1_up_wick, c1_lo_wick = SingleCandleStick(self.patten_detect["candle1"]).length()
        c2_bd_len, c2_wick_len, c2_up_wick, c2_lo_wick = SingleCandleStick(self.patten_detect["candle2"]).length()

        if ((c2_bd_len / c1_bd_len) > 0.5) and (self.__close1 > self.__open2) and (self.__open1 > self.__close2):
            return "Bullish"
        else:
            return False

    def dark_cloud(self):
        c1_bd_len, c1_wick_len, c1_up_wick, c1_lo_wick = SingleCandleStick(self.patten_detect["candle1"]).length()
        c2_bd_len, c2_wick_len, c2_up_wick, c2_lo_wick = SingleCandleStick(self.patten_detect["candle2"]).length()

        if ((c2_bd_len / c1_bd_len) > 0.5) and (self.__open1 < self.__close2) and (self.__close1 < self.__open2):
            return "Bearish"
        else:
            return False

    def harami(self):
        c1_bd_len, c1_wick_len, c1_up_wick, c1_lo_wick = SingleCandleStick(self.patten_detect["candle1"]).length()
        c2_bd_len, c2_wick_len, c2_up_wick, c2_lo_wick = SingleCandleStick(self.patten_detect["candle2"]).length()

        if ((c2_bd_len / c1_bd_len) < 0.8) and (self.__close1 < self.__open2) and (self.__open2 < self.__close2):
            return "Bullish"
        elif ((c2_bd_len / c1_bd_len) < 0.8) and (self.__open1 < self.__close2) and (self.__close2 < self.__open2):
            return "Bearish"
        else:
            return False

    def gap(self):
        if (self.__open1 < self.__close1) and (self.__open2 < self.__close2) and (self.__open2 > self.__high1):
            return "Bullish"
        elif (self.__close1 < self.__open1) and (self.__close2 < self.__open2) and (self.__open2 < self.__low1):
            return "Bearish"
        else:
            return False


class TripleCandleStick(DoubleCandleStick):
    __slots__ = ['__open1', '__high1', '__low1', '__close1', '__volume1',
                 '__open2', '__high2', '__low2', '__close2', '__volume2',
                 '__open3', '__high3', '__low3', '__close3', '__volume3']

    def __init__(self, candle1: dict, candle2: dict, candle3: dict):
        super().__init__(candle1, candle2)
        try:
            self.__open1 = float(candle1["1. open"])
            self.__high1 = float(candle1["2. high"])
            self.__low1 = float(candle1["3. low"])
            self.__close1 = float(candle1["4. close"])
            self.__volume1 = float(candle1["5. volume"])

            self.__open2 = float(candle2["1. open"])
            self.__high2 = float(candle2["2. high"])
            self.__low2 = float(candle2["3. low"])
            self.__close2 = float(candle2["4. close"])
            self.__volume2 = float(candle2["5. volume"])

            self.__open3 = float(candle3["1. open"])
            self.__high3 = float(candle3["2. high"])
            self.__low3 = float(candle3["3. low"])
            self.__close3 = float(candle3["4. close"])
            self.__volume3 = float(candle3["5. volume"])
        except KeyError:
            print("Invalid OHLCV data (Tripple candle sitck).")

    @property
    def patten_detect(self):
        return {"candle1": {"1. open": self.__open1,
                            "2. high": self.__high1,
                            "3. low": self.__low1,
                            "4. close": self.__close1,
                            "5. volume": self.__volume1},
                "candle2": {"1. open": self.__open2,
                            "2. high": self.__high2,
                            "3. low": self.__low2,
                            "4. close": self.__close2,
                            "5. volume": self.__volume2},
                "candle3": {"1. open": self.__open3,
                            "2. high": self.__high3,
                            "3. low": self.__low3,
                            "4. close": self.__close3,
                            "5. volume": self.__volume3}}

    @patten_detect.setter
    def patten_detect(self, candle1: dict, candle2: dict, candle3: dict):
        try:
            self.__open1 = float(candle1["1. open"])
            self.__high1 = float(candle1["2. high"])
            self.__low1 = float(candle1["3. low"])
            self.__close1 = float(candle1["4. close"])
            self.__volume1 = float(candle1["5. volume"])

            self.__open2 = float(candle2["1. open"])
            self.__high2 = float(candle2["2. high"])
            self.__low2 = float(candle2["3. low"])
            self.__close2 = float(candle2["4. close"])
            self.__volume2 = float(candle2["5. volume"])

            self.__open3 = float(candle3["1. open"])
            self.__high3 = float(candle3["2. high"])
            self.__low3 = float(candle3["3. low"])
            self.__close3 = float(candle3["4. close"])
            self.__volume3 = float(candle3["5. volume"])
        except KeyError:
            print("Invalid OHLCV data ")

    #@patten_detect.getter
    def get_patten(self):
        morning_star = self.morning_star()
        evening_star = self.evening_star()
        englufing_doji = self.engulfing_doji()

        if morning_star is not False:
            return "morning_star", morning_star
        elif evening_star is not False:
            return "evening_star", evening_star
        elif englufing_doji is not False:
            return "englufing_doji", englufing_doji
        else:
            return 0, 0

    def morning_star(self):
        c1_bd_len = SingleCandleStick(self.patten_detect["candle1"]).length()[0]
        c1_lo_wick = SingleCandleStick(self.patten_detect["candle1"]).length()[3]

        gap1 = DoubleCandleStick(self.patten_detect["candle1"], self.patten_detect["candle2"]).gap()
        gap2 = DoubleCandleStick(self.patten_detect["candle2"], self.patten_detect["candle3"]).gap()
        midile = SingleCandleStick(self.patten_detect["candle2"]).spinnig_top()

        if ((c1_lo_wick / c1_bd_len) < 0.2) and (gap1 == "Bearish") and (midile== True) and (gap2 == "Bullish") \
            and (self.__open3 > self.__close1) and (self.__close3 > self.__open1):
            return True
        else:
            return False

    def evening_star(self):
        c1_bd_len = SingleCandleStick(self.patten_detect["candle1"]).length()[0]
        c1_up_wick = SingleCandleStick(self.patten_detect["candle1"]).length()[2]

        gap1 = DoubleCandleStick(self.patten_detect["candle1"], self.patten_detect["candle2"]).gap()
        gap2 = DoubleCandleStick(self.patten_detect["candle2"], self.patten_detect["candle3"]).gap()
        midile = SingleCandleStick(self.patten_detect["candle2"]).spinnig_top()

        if ((c1_up_wick / c1_bd_len) < 0.2) and (gap1 == "Bullish") and (midile== True) and (gap2 == "Bearish") \
            and (self.__open3 < self.__close1) and (self.__close3 < self.__open1):
            return True
        else:
            return False

    def engulfing_doji(self):

        engulfing = DoubleCandleStick(self.patten_detect["candle1"], self.patten_detect["candle2"]).engulfing()
        doji = SingleCandleStick(self.patten_detect["candle3"]).spinnig_top()

        if engulfing is not False and doji is not False:
            return "engulfing_doji", engulfing
        else:
            return False

