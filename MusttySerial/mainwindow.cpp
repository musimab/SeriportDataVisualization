#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QtAlgorithms>



MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    make_signal_slot_connection();
    add_mpl_visualition_dock_widget();

}

MainWindow::~MainWindow()
{
    delete ui;
    stop_worker_threads();
    //delete m_plot_visualization_dock_widget;
    //delete m_plot_visualization_widget;
}

void MainWindow::list_available_serial_ports()
{
    const auto infos = QSerialPortInfo::availablePorts();
    for (const QSerialPortInfo &info : infos)
        ui->comboBoxSeriaPortLists->addItem(info.portName());

    ui->comboBoxBaudRates->addItems({"9600", "57600", "115200", "512000"});

}

void MainWindow::port_connect()
{

    QString device_connection_info = "device_connection_info";
    ui->pushButton_connect->setEnabled(false);
    ui->pushButton_disconnect->setEnabled(true);
    ui->pushButton_send->setEnabled(true);
    ui->statusbar->showMessage(device_connection_info);
}

void MainWindow::port_disconnect()
{
    QString device_connection_info = " disconnected";
    ui->pushButton_connect->setEnabled(true);
    ui->pushButton_disconnect->setEnabled(false);
    ui->pushButton_send->setEnabled(false);
    ui->statusbar->showMessage(device_connection_info);

}

void MainWindow::port_receive_data(QByteArray byteArray)
{

    ui->textEdit->append(byteArray.replace('\0',""));

}

void MainWindow::clear_workspace()
{
    ui->textEdit->clear();
}

void MainWindow::open_test_folder_slot()
{

}

void MainWindow::start_serial_read_process()
{
    qDebug() <<"start serial read process";
    QString port_name = ui->comboBoxSeriaPortLists->currentText();
    QString baudrate = ui->comboBoxBaudRates->currentText();
    uint8_t  timeout =1;

    SerialReadWorkerThread = new QThread();
    m_worker_reader = new SerialReadWorker(nullptr,port_name,baudrate, timeout);

    /* move the worker to thread*/
    m_worker_reader->moveToThread(SerialReadWorkerThread);

    // Start Worker thread
    connect(SerialReadWorkerThread, &QThread::started, m_worker_reader, &SerialReadWorker::run);

    connect(m_worker_reader, &SerialReadWorker::send_requested_data, this, &MainWindow::port_receive_data);

    // Write data to serial port
    connect(this, &MainWindow::write_data_signal, m_worker_reader, &SerialReadWorker::write_data);
    connect(m_worker_reader, &SerialReadWorker::write_operation_finished, this, &MainWindow::write_signal_received);

    // Connection Info Transfer
    connect(m_worker_reader, &SerialReadWorker::device_connected, this, &MainWindow::port_connect);
    // mplot widget

    // Draw received bytarray in Mplot visualition widget
    connect(m_worker_reader, &SerialReadWorker::send_requested_data, m_plot_visualization_widget, &MplotVisualization::decode_requested_data);

    // Stop serial timer in worker thread
    connect(ui->pushButton_disconnect, &QPushButton::clicked, m_worker_reader, &SerialReadWorker::stop_work);

    // Close serial port connection
    connect(m_worker_reader, &SerialReadWorker::finished, this, &MainWindow::port_disconnect);//stop worker thread when the finished signal received

    //Quit the thread
    connect(m_worker_reader, &SerialReadWorker::finished, SerialReadWorkerThread, &QThread::quit);//stop worker thread when the finished signal received
    connect(m_worker_reader, &SerialReadWorker::destroyed, SerialReadWorkerThread, &QThread::quit);
    //connect(m_worker_reader, &SerialReadWorker::finished, SerialReadWorkerThread, &QThread::exit);//stop worker thread when the finished signal received

    // delete worker after finish the work
    connect(m_worker_reader, &SerialReadWorker::finished, m_worker_reader, &SerialReadWorker::deleteLater);//stop worker thread when the finished signal received

    // Delete thread
    connect(SerialReadWorkerThread, &QThread::finished, SerialReadWorkerThread, &QThread::deleteLater);

    // Start worker
    SerialReadWorkerThread->start();

}

void MainWindow::port_send_data_from_line_editor()
{
   QString data_to_send = ui->lineEdit_enter_command->text();
   data_to_send = data_to_send + "\r\n";
   emit write_data_signal(data_to_send.toUtf8());
}

void MainWindow::write_signal_received()
{
    ui->statusbar->showMessage("Send data succesful");
}



void MainWindow::add_mpl_visualition_dock_widget()
{
    QDockWidget* m_plot_visualization_dock_widget = new QDockWidget(tr("Visualization"),this);

    m_plot_visualization_widget = new MplotVisualization(m_plot_visualization_dock_widget);

    m_plot_visualization_dock_widget->setWidget(m_plot_visualization_widget);
    m_plot_visualization_dock_widget->setAllowedAreas(Qt::RightDockWidgetArea);
    m_plot_visualization_dock_widget->setSizePolicy(QSizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum));
    m_plot_visualization_dock_widget->setFloating(false);

    addDockWidget(Qt::RightDockWidgetArea,  m_plot_visualization_dock_widget);

}

void MainWindow::make_signal_slot_connection()
{
    //connect(ui->pushButton_connect, &QPushButton::clicked,this, &MainWindow::port_connect);
    //connect(ui->pushButton_connect, &QPushButton::clicked, this, &MainWindow::start_serial_read_process);
    connect(ui->lineEdit_enter_command, &QLineEdit::editingFinished, this, &MainWindow::port_send_data_from_line_editor);
    connect(ui->pushButton_open, &QPushButton::clicked, this, &MainWindow::open_test_folder_slot);
    connect(ui->pushButton_clear, &QPushButton::clicked, ui->textEdit,&QTextEdit::clear);

    connect(ui->pushButton_disconnect, &QPushButton::clicked,[=]() {

        qDebug() <<" disconnect button pressed: " ;
   });

}

void MainWindow::stop_worker_threads()
{
    if(SerialReadWorkerThread != nullptr) {

           if(SerialReadWorkerThread->isRunning()) {
               SerialReadWorkerThread->quit();
               SerialReadWorkerThread->wait();
               qDebug() << "SerialReadWorkerThread quit";
           }

       }
}



void MainWindow::on_checkbox_save_txt_clicked(bool checked)
{


    if(checked) {

        QString nameFile = QFileDialog::getSaveFileName(this, tr("Choose where to save"), "",
                                                          tr("choose type of file (*.txt);;C++ File (*.cpp *.h)"));

         qDebug() << nameFile;
            if (nameFile != "") {
                QFile file(nameFile);

                if (file.open(QIODevice::ReadWrite)) {
                      QTextStream stream(&file);
                    stream << ui->textEdit->toPlainText();
                    file.flush();
                    file.close();
                }
                else {
                    QMessageBox::critical(this, tr("Error"), tr("could not save the file"));
                    return;
                }
            }
            ui->lineEdit_saved_file_path->setText(nameFile);

    }
}




void MainWindow::on_pushButton_connect_clicked(bool)
{

    ui->comboBoxBaudRates->addItems({"9600", "57600", "115200", "512000"});

    if(!m_connect_button_pressed) {
        const auto infos = QSerialPortInfo::availablePorts();
        if( !infos.isEmpty()) {
            for (const QSerialPortInfo &info : infos)
                ui->comboBoxSeriaPortLists->addItem(info.portName());

            ui->pushButton_connect->setText("connect");
            m_connect_button_pressed = true;
        }

      if(m_connect_button_pressed) {
          connect(ui->pushButton_connect, &QPushButton::clicked,this, &MainWindow::port_connect);
          connect(ui->pushButton_connect, &QPushButton::clicked, this, &MainWindow::start_serial_read_process);
      }


    }
}

