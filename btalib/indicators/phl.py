from . import Indicator


class phl(Indicator):
    '''
    Pivot Point Highs are calculated by the number of bars with lower highs
    on either side of a Pivot Point High calculation. 
    Similarly, Pivot Point Lows are calculated by the number of bars with higher lows
    on either side of a Pivot Point Low calculation.
    
    In order to counteract look-ahead bias & re-painting, Pivot Points
    can be marked on the indexes they were discovered,
    instead of being marked on theirs actual indexes. It allows the study
    to behave in realistic manner, both during backtesting and live calculations.
    '''
    group   = 'trend'
    alias   = 'PPHL', 'PivotHighLow'
    outputs = 'pivothighlow'
    params  = (('number'  , 1    , 'number of bars to the left and to the right'),
               ('location', 'low', "'high', 'low' or 'both'"),
               ('shift'   , True , 'marks Pivot Points either on their actual indexex, or on the indexes when they were discovered'),)
    
    def __init__(self):
            
        if   (self.p.location == 'low' ):

            if (self.p.shift):
                self.o.pl = self.i0.apply(lambda x: self._pl(x.name, self.p.number), axis=1)
                self.o.pl = self.o.pl.shift(self.p.number)
            else:
                self.o.pl = self.i0.apply(lambda x: self._pl(x.name, self.p.number), axis=1)

        elif (self.p.location == 'high'):

            if (self.p.shift):
                self.o.ph = self.i0.apply(lambda x: self._ph(x.name, self.p.number), axis=1)                        
                self.o.ph = self.o.ph.shift(self.p.number)
            else:
                self.o.ph = self.i0.apply(lambda x: self._ph(x.name, self.p.number), axis=1)   

        else:

            if (self.p.shift):
                self.o.pl = self.i0.apply(lambda x: self._pl(x.name, self.p.number), axis=1)
                self.o.ph = self.i0.apply(lambda x: self._ph(x.name, self.p.number), axis=1)
                self.o.pl = self.o.pl.shift(self.p.number)
                self.o.ph = self.o.ph.shift(self.p.number)
            else:
                self.o.pl = self.i0.apply(lambda x: self._pl(x.name, self.p.number), axis=1)
                self.o.ph = self.i0.apply(lambda x: self._ph(x.name, self.p.number), axis=1)        
        

    def _pl(self, i, n):

        if (i > n) and (i < len(self.i0)-n):

            for j in range(1, n+1):

                if (self.i0.low [i] < self.i0.low [i-j]) and (self.i0.low [i] < self.i0.low [i+j]):
                    pl = self.i0.low [i]
                else:
                    pl = None
                    break


        else:
            pl = None

        return pl

    def _ph(self, i, n):

        if (i > n) and (i < len(self.i0)-n):

            for j in range(1, n+1):

                if (self.i0.high[i] > self.i0.high[i-j]) and (self.i0.high[i] > self.i0.high[i+j]):
                    ph = self.i0.high[i]
                else:
                    ph = None
                    break


        else:
            ph = None

        return ph
