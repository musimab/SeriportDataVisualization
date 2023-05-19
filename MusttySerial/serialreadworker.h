#ifndef SERIALREADWORKER_H
#define SERIALREADWORKER_H
#include <QSerialPort>
#include <QObject>
#include <QTimer>

#define DATA_PACKAGE_SIZE  1


class SerialReadWorker: public QObject
{
    Q_OBJECT
public:
    SerialReadWorker(QObject *parent=nullptr , QString port_name="", QString baudrate="",uint8_t timeout=10);
     ~SerialReadWorker();
    void get_serial_connection_configurations();
    void write_data(QString);
public slots:
    void start_work();
    void stop_work();
    void run();
signals:
    void finished();
    void send_requested_data(QByteArray);
    void write_operation_finished();
    void device_connected(QString);

private:
    QSerialPort* m_serialPort = nullptr;
    QTimer* m_timer = nullptr;

    QString m_port_name ;
    QString m_baud_rate ;
    QString m_data_bits;
    QString m_parity;
    QString m_stop_bit;
    uint8_t m_current_wait_timeout ;
    QByteArray m_received_data;
    uint16_t m_requested_data_size;
};

#endif // SERIALREADWORKER_H
