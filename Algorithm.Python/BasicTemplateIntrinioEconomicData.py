﻿# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from clr import AddReference
AddReference("System")
AddReference("QuantConnect.Algorithm")
AddReference("QuantConnect.Common")
AddReference("QuantConnect.Indicators")


from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
from QuantConnect.Data.Custom import *
from QuantConnect.Data.Custom.Intrinio import *
from numpy import sign

class BasicTemplateIntrinioEconomicData(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.SetStartDate(2010, 1, 1)  #Set Start Date
        self.SetEndDate(2013, 12, 31)  #Set End Date
        self.SetCash(100000)           #Set Strategy Cash

        # Set your Intrinino user and password.
        IntrinioConfig.SetUserAndPassword(self.GetParameter("intrinio-username"), self.GetParameter("intrinio-password"))
        # The Intrinio user and password can be also defined in the config.json file for local backtest.

        # United States Oil Fund LP
        self.uso = self.AddEquity("USO", Resolution.Daily).Symbol
        self.Securities[self.uso].SetLeverage(2)
        # United States Brent Oil Fund LP
        self.bno = self.AddEquity("BNO", Resolution.Daily).Symbol
        self.Securities[self.bno].SetLeverage(2)

        self.AddData(IntrinioEconomicData, "$DCOILWTICO", Resolution.Daily)
        self.AddData(IntrinioEconomicData, "$DCOILBRENTEU", Resolution.Daily)


    def OnData(self, slice):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        Arguments:
            data: Slice object keyed by symbol containing the stock data
        '''
        if (slice.ContainsKey("$DCOILBRENTEU") or slice.ContainsKey("$DCOILWTICO")):
            spread = slice["$DCOILBRENTEU"].Value - slice["$DCOILWTICO"].Value
        else:
            return

        if ((spread > 0 and not self.Portfolio[self.bno].IsLong) or
            (spread < 0 and not self.Portfolio[self.uso].IsShort)):
            self.SetHoldings(self.bno, 0.25 * sign(spread))
            self.SetHoldings(self.uso, -0.25 * sign(spread))