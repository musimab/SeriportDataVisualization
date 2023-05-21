#include "serialreadworker.h"
#include <QDebug>

SerialReadWorker::SerialReadWorker(QObject *parent, QString port_name, QString baudrate, uint8_t timeout):
   QObject(parent), m_port_name(port_name), m_baud_rate(baudrate),m_current_wait_timeout(timeout)

{

}

SerialReadWorker::~SerialReadWorker()
{
    if(m_serialPort->isOpen()) {
        m_serialPort->close();
    }


    delete m_serialPort;
    delete m_timer;

    qDebug() << "~SerialReadWorker";

}

void SerialReadWorker::get_serial_connection_configurations()
{
    m_serialPort = new QSerialPort();
    m_serialPort->setPortName(m_port_name);
    m_serialPort->setBaudRate(m_baud_rate.toUInt());
    m_serialPort->setDataBits(QSerialPort::Data8);
    m_serialPort->setParity(QSerialPort::NoParity);
    m_serialPort->setStopBits(QSerialPort::OneStop);



}

void SerialReadWorker::write_data(QString data)
{
    if(!m_serialPort->isOpen()) {
        m_serialPort->open(QIODevice::ReadWrite);
    }

    m_serialPort->write(data.toUtf8());
    emit write_operation_finished();

}

void SerialReadWorker::start_work()
{
        /*
            if(m_serialPort->bytesAvailable()> 700) {
            m_received_data.append( m_serialPort->readAll());
            emit send_requested_data(m_received_data);
            //m_serialPort->waitForReadyRead(m_current_wait_timeout);
            m_serialPort->flush();
            }

            m_received_data.clear();
            */






        if(m_serialPort->bytesAvailable()> DATA_PACKAGE_SIZE) {
            QByteArray requested_data = m_serialPort->readLine();
            emit send_requested_data(requested_data);
            m_serialPort->waitForReadyRead(m_current_wait_timeout);
            m_serialPort->flush();

        }





    /*This method can bu used for synchrous reading in real time */
/*
    while(m_serialPort->canReadLine()) {
        QByteArray requested_data = m_serialPort->readLine();
        emit send_requested_data(requested_data);
        m_serialPort->waitForReadyRead(0);
        m_serialPort->flush();
    }
*/

}

void SerialReadWorker::stop_work()
{

    //m_timer->stop();
    if(m_serialPort->isOpen()) {
        m_serialPort->close();
    }
    emit finished();
}

void SerialReadWorker::run()
{

    m_timer = new QTimer();
    get_serial_connection_configurations();

    // Open the Port
    if(!m_serialPort->isOpen()){
        m_serialPort->open(QIODevice::ReadWrite);
    }

    //connect(m_serialPort, &QSerialPort::readyRead, this, &SerialReadWorker::start_work);
    connect(m_timer, &QTimer::timeout, this, &SerialReadWorker::start_work);


    m_timer->start(1);
    emit device_connected("Device connected");

}
