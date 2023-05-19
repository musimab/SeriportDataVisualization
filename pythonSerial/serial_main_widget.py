
import sys

from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QDialogButtonBox, QDialog, QWidget, QMenu, QMenuBar,
    QAction, QFileDialog, QTableWidgetItem, QMessageBox, QMenu, QScrollBar, QTabWidget, QSizePolicy, QDockWidget
)

from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize, pyqtSlot, QRunnable, QThreadPool, QIODevice, QObject

from mainwindow_python import Ui_MainWindow
from os import listdir
from os.path import isfile, join
import numpy as np
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort

from mpl_widget import mplWidget
from matplotlib.figure import Figure

from datetime import datetime
import datetime
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg



class SerialReadWorker(QObject):
    '''
    Worker thread
    Inherits from QObject to handler worker thread setup, signals and wrap-up.
    '''
    finished = pyqtSignal()
    send_requested_data = pyqtSignal(object)
    write_sig = pyqtSignal()
    device_connected = pyqtSignal(object)
    

    def __init__(self,port_name, baud_rate, data_bits,parity, stop_bit):
        super(SerialReadWorker, self).__init__()

        self.m_quit = False
        self.current_wait_timeout = 1
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.data_bits = data_bits
        self.parity = parity
        self.stop_bit = stop_bit
        self.data_write = None

        self.write_flag = False
        
    def write_data(self,data):
        self.write_flag = True
        self.data_write = data
        self.write_sig.emit()


    def run(self):
        serialPort = QSerialPort()
        serialPort.setPortName(self.port_name)
        serialPort.setBaudRate(self.baud_rate)
        serialPort.setDataBits(self.data_bits)
        serialPort.setParity(self.parity)
        serialPort.setStopBits(self.stop_bit)
        
        device_connection_info =" Port: " + str(serialPort.portName()) + \
                                " baudrate: " + str(serialPort.baudRate()) + \
                                " databits: " + str(serialPort.dataBits()) + \
                                " parity: " + str(serialPort.parity())+ \
                                " stopbits: " + str(serialPort.stopBits())
        
        if(not serialPort.isOpen()):
            serialPort.open(QIODevice.ReadWrite)
            self.device_connected.emit(device_connection_info)

        current_wait_timeout = self.current_wait_timeout

        while(not self.m_quit):
            # check if we need to abort the loop; need to process events to receive signals;
            #app.processEvents()  # this could cause change to self.write_flag and self.m_quit
            QApplication.processEvents()
            if(self.write_flag):
                serialPort.write(self.data_write)
                self.write_flag = False

            if(serialPort.waitForReadyRead(current_wait_timeout)):
                request_data = serialPort.readAll()
                while(serialPort.waitForReadyRead(10)):
                    request_data.append(serialPort.readAll())

                request_data_decoded = request_data.data().decode()
                # Remove the '\0' character from data
                #error_data = error_data.replace('\0', '')
                # Send UART data to mpl widget
                #self.signals.send_requested_data.emit(request_data_decoded , "deneme")
                # Send QText Edit Window
                self.send_requested_data.emit(request_data_decoded)

        
        if(serialPort.isOpen()):
            serialPort.close()
        self.finished.emit()  # Stop signal is emitted


class SerialComm(QMainWindow):

    write_data_signal = pyqtSignal(object)


    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("Mustty")
        self.listSerialPorts()
       
        # Threading Part
        self.thread = None
        self.worker_reader = None

        self.data_file_path = None

        self.ui.pushButton_connect.clicked.connect(self.portConnect)
        self.ui.pushButton_connect.clicked.connect(self.start_serial_read_process)
        
        self.ui.pushButton_send.clicked.connect(self.portSendData)
        
        self.ui.lineEdit_enter_command.editingFinished.connect(self.portSendDatafromLineEditor)
        self.ui.pushButton_clear.clicked.connect(self.clearWorkspace)

        self.ui.pushButton_open.clicked.connect(self.open_test_folder_slot)
        self.ui.checkbox_save_txt.clicked.connect(self.save_terminal_data_as_txt)
        
        self.mpl_widget = mplWidget()
        self.add_data_plot_dock_widget()
        self.show()

    def listSerialPorts(self):

        serialPortInfo = QSerialPortInfo()
        serial_list = serialPortInfo.availablePorts()
        serial_ports = [port.portName() for port in serial_list]
        self.ui.comboBoxSeriaPortLists.addItems(serial_ports)

        baud_rate_list = ["9600", "57600", "115200", "512000"]
        self.ui.comboBoxBaudRates.addItems(baud_rate_list)

    def portConnect(self,device_connection_info):
        """
        When the device_connected signal is received from serial read worker,
        this slot is activated and buttons are configured
        """
        self.ui.pushButton_connect.setEnabled(False)
        self.ui.pushButton_disconnect.setEnabled(True)
        self.ui.pushButton_send.setEnabled(True)
        self.ui.statusbar.showMessage(str(device_connection_info))

    def portDisconnect(self):
        """
        When the finish signal is received from serial read worker,
        this slot is activated and buttons are enabled
        """
        self.ui.pushButton_connect.setEnabled(True)
        self.ui.pushButton_disconnect.setEnabled(False)
        self.ui.pushButton_send.setEnabled(False)
        self.ui.statusbar.showMessage("Port Disconneced")


    def portSendData(self):
        """
        To send numpy array from text file
        """

        if not self.data_file_path:
            QMessageBox.about(self, "Warning", "file path is empty")
            return
        data = np.loadtxt(self.data_file_path, dtype=np.float32)

        data_str = "$"
        package_count = 0
        for index, (s1, s2, s3, s4, reactive) in enumerate(data):
            package_count += 1
            #data_str = data_str + str(s1) + "$"+ str(s2) + "$"+ str(s3) +"$"+ str(s4)+ "$" + str(reactive) + "$"
            data_str = data_str + str(s1) + "$"
            if (index+1) % 451 == 0:
                print(len(data_str))
                #serialPort.write(data_str.encode())
                data_str = "$"
                break

    def portReceiveData(self, data):
        """
        When the send_requested_data signal is emitted, this slot is responisble for
        receiving encoded data and showing in terminal text edit
        """
        # remove white space character '\0' from string
        #data = data.replace('\0', '')
        #data = data.strip()
        self.ui.textEdit.append(data)

    def clearWorkspace(self):
        """
        To clear received data and matplot screen
        """
        self.ui.textEdit.clear()
        self.mpl_widget.clear_plot()

    def open_test_folder_slot(self):

        self.data_file_path = QFileDialog.getOpenFileName(self, 'Select Folder')[0]
        self.ui.lineEdit.setText(self.data_file_path)

        if not self.data_file_path:
            QMessageBox.about(self, "Warning", "file path is empty")
            return

    def start_serial_read_process(self):
        """
        Start serial read and write worker thread, creating qthread and worker with moveTothread method
        When the thread finish process, 
        """

        #################   Start Serial Recive Worker   #######################
        print("start serial read worker process")
        port_name = self.ui.comboBoxSeriaPortLists.currentText()
        baud_rate = int(self.ui.comboBoxBaudRates.currentText())
        data_bits = QSerialPort.DataBits.Data8
        parity = QSerialPort.Parity.NoParity
        stop_bit = QSerialPort.StopBits.OneStop

        self.worker_reader = SerialReadWorker(port_name, baud_rate, data_bits,parity, stop_bit)
        self.thread = QThread()

        # move the worker to thread
        self.worker_reader.moveToThread(self.thread)
        self.thread.started.connect(self.worker_reader.run)
        
        # Start the serial read worker
        #send the requested data to matplot widget
        self.worker_reader.send_requested_data.connect(self.mpl_widget.plot_requested_data_matplot)
        self.worker_reader.send_requested_data.connect(self.portReceiveData) # send the requested data to gui
        
        # Stop serial read loop
        self.ui.pushButton_disconnect.clicked.connect(self.stop_serial_read_worker)
        
        # Quit the thread

        self.worker_reader.finished.connect(self.thread.quit) # stop worker thread when the finished signal received
        self.worker_reader.finished.connect(self.worker_reader.deleteLater) # delete thread after finish the work
        self.worker_reader.finished.connect(self.portDisconnect)
        self.thread.finished.connect(self.thread.deleteLater)

        # write data 
   
        self.write_data_signal.connect(self.worker_reader.write_data)
        self.worker_reader.write_sig.connect(self.write_signal_received)

        # Connection Status
        self.worker_reader.device_connected.connect(self.portConnect)

        self.thread.start()


    def portSendDatafromLineEditor(self):
        """
        Send data from line_editor to worker thread
        User send or write data over serial terminal
        """
        data_to_send = self.ui.lineEdit_enter_command.text().encode()
        self.write_data_signal.emit(data_to_send)
        

    def stop_serial_read_worker(self):
        """
        To stop serial read process in while loop, set m_quit flag to True
        """
        self.worker_reader.m_quit = True
    
    
    def write_signal_received(self):
        """
        Send operation over serial port is succesful
        """
        self.ui.statusbar.showMessage("send data succesful")

        
    def add_data_plot_dock_widget(self):

        signal_derivatives_dock_widget = QDockWidget("Uart Plot", self)

        signal_derivatives_dock_widget.setWidget(self.mpl_widget)

        signal_derivatives_dock_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))

        signal_derivatives_dock_widget.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea,
                           signal_derivatives_dock_widget)

    def save_terminal_data_as_txt(self):

        Text = self.ui.textEdit.toPlainText()
        current_time = datetime.datetime.now()
        time_info = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + "_" + str(current_time.hour)+"-" + \
            str(current_time.minute)+"-" + str(current_time.second) + \
            "-" + str(current_time.microsecond)+"_" + 'output.txt'

        if not os.path.exists("outputs_mustty/"):
            os.makedirs("outputs_mustty/")
        name_of_file = "outputs_mustty/" + time_info

        with open(name_of_file, 'w') as file:
            file.write(Text)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
				QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
            # Stop the worker
            if(not self.ui.pushButton_connect.isEnabled()):
                self.stop_serial_read_worker()

            print('Window closed')
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialComm()
    window.show()
    sys.exit(app.exec_())