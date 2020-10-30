# Author: Colin Pollard
# Date: 10/30/2020
# This file encompasses methods to save trajectory data for export to MATLAB.
import csv


def exportToCSV(filename, xList, yList, zList):
    """
    Export x, y, z trajectory to csv files.

    :param filename: Name of the file to save inside the Export Folder
    :param xList: List of x positions
    :param yList: List of y positions
    :param zList: List of z positions
    :return: None
    """

    xName = "Export/" + filename + "X.csv"
    # Write X file
    with open(xName, mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(xList)

    yName = "Export/" + filename + "Y.csv"
    with open(yName, mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(yList)

    zName = "Export/" + filename + "Z.csv"
    with open(zName, mode='w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(zList)