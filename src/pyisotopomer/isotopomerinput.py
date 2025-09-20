"""
File: isotopomerinput.py
---------------------------
Created on Weds June 2nd, 2021

Functions and Input class to read in and parse data
from excel template.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


import pandas as pd
import numpy as np
from itertools import combinations


class IsotopomerInput:
    """
    Read in data from the data corrections spreadsheet.

    USAGE: R = IsotopomerInput(inputfile, tabname)

    INPUT:
        :param filename: filename for spreadsheet template, e.g. "00_excel_template.xlsx"
        :type R: string
        :param tabname: name of tab containing size-corrected isotope ratios (default: "size_correction")
        :type R: string
        :param datadf: dataframe for input in same format as spreadsheet template
        :type datadf: Pandas DataFrame

    OUTPUT:
        :returns: self.data, self.sizecorrected, self.ratiosscrambling

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """

    def __init__(self, filename=None, tabname=None, datadf=None):

        if (filename is not None) and (datadf is not None):
            raise ValueError("Both input file and dataframe provided")
        
        if filename is not None:
            
            self.filename = filename
    
            if tabname is not None:
                self.tabname = tabname
            elif tabname is None:
                self.tabname = "size_correction"
    
            try:
                # full contents of excel template, first tab
                self.data = self.readin(self.filename, self.tabname)
            except FileNotFoundError:
                if self.filename[-5:] != ".xlsx":
                    self.filename = self.filename + ".xlsx"
                    self.data = self.readin(self.filename, self.tabname)

        elif datadf is not None:
            self.data = datadf.copy()

        # subset of data to be used for Isotopomers
        self.sizecorrected = self.parseratios(self.data)

        self.ratiosscrambling = self.parseisotopomerinput(self.data)

    def readin(self, filename, tabname):
        # return Pandas DataFrame of all input data
        return pd.read_excel(filename, tabname, skiprows=1)

    def parseratios(self, data):
        # return just the size-corrected isotope ratios in a numpy array
        # for input to calcSPmain
        return np.array(
            data[
                ["size corrected 31R", "size corrected 45R", "size corrected 46R"]
            ].dropna()
        )

    def parseisotopomerinput(self, data):
        # return just the size-corrected isotope ratios in a numpy array
        # for input to calcSPmain
        return np.array(
            data[
                [
                    "size corrected 31R",
                    "size corrected 45R",
                    "size corrected 46R",
                    "D17O",
                    "gamma",
                    "kappa",
                ]
            ].dropna()
        )

    def __repr__(self):
        return f"{self.sizecorrected}"


if __name__ == "__main__":
    print(Input(filename="00_Python_template_v3.xlsx"))
