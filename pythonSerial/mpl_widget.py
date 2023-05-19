from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar)

import numpy as np
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import (MultipleLocator, MaxNLocator, AutoMinorLocator)
from matplotlib import pyplot as plt

import matplotlib


class mplWidget(QWidget):

    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(plt.Figure(figsize=(15, 6)))
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.uart_data = np.array([])
        self.insert_ax()
        self.setLayout(vertical_layout)

    def insert_ax(self):
        font = {
            'weight': 'normal',
            'size': 10
        }
        matplotlib.rc('font', **font)
        self.ax = self.canvas.figure.subplots()
        self.ax.set_xlim([0, 100])
        self.ax.set_ylim([-3, 3])
        self.lines = self.ax.plot([], [], linewidth=4)[0]

    def plot_requested_data_matplot(self, received_data):
        """
        if the received data has back
        """
        #received_data = received_data.rstrip()
        WINDOW_LENGTH = 100

        try:
            received_data = float(received_data.replace('\0', ''))
        except:
            received_data = 0.0

        if(len(self.uart_data) < WINDOW_LENGTH):
            self.uart_data = np.append(self.uart_data, received_data)
        else:
            self.uart_data[0:WINDOW_LENGTH-1] = self.uart_data[1:WINDOW_LENGTH]
            self.uart_data[WINDOW_LENGTH - 1] = received_data

        self.lines.set_xdata(np.arange(0, len(self.uart_data)))
        self.lines.set_ydata(self.uart_data)

        self.canvas.draw()

    def clear_plot(self):

        self.lines.set_xdata([])
        self.lines.set_ydata([])
        self.uart_data = np.array([])
        self.canvas.draw()

    def autoscale_y(self, ax, margin=0.1):
        """This function rescales the y-axis based on the data that is visible given the current xlim of the axis.
        ax -- a matplotlib axes object
        margin -- the fraction of the total height of the y-data to pad the upper and lower ylims"""

        def get_bottom_top(line):
            xd = line.get_xdata()
            yd = line.get_ydata()
            lo, hi = ax.get_xlim()
            y_displayed = yd[((xd > lo) & (xd < hi))]
            h = np.max(y_displayed) - np.min(y_displayed)
            bot = np.min(y_displayed)-margin*h
            top = np.max(y_displayed)+margin*h
            return bot, top

        lines = ax.get_lines()
        bot, top = np.inf, -np.inf

        for line in lines:
            new_bot, new_top = get_bottom_top(line)
            if new_bot < bot:
                bot = new_bot
            if new_top > top:
                top = new_top

        ax.set_ylim(bot, top)
