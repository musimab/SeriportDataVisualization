## Serial Comminication with UART 


![Screenshot from 2023-03-12 13-05-43](https://user-images.githubusercontent.com/47300390/224537964-0fb793f7-1987-4c0b-aa2b-99dcf7e64bc0.png)



https://github.com/musimab/SeriportDataVisualization/assets/47300390/a879152a-7a33-4083-9c09-ef9d642108e5




# QT ile Seri Port okuması

https://github.com/musimab/SeriportDataVisualization/assets/47300390/02de951b-0c6b-44fd-85f1-c0e3134f0593

1. Blocking Synchronous Way

Use waitForReadyRead() to block the thread until new data arrives to the serial port. This makes the calling thread unable to do anything until new data arrives on this serial port. If this thread was a GUI thread, This will make the application unresponsive during that period of time. Use this approach only when you are sure this is what you want. Your code can be rewritten like this:

```
connect(m_timer, &QTimer::timeout, this, &SerialReadWorker::start_work);
m_timer->start(0);


void SerialReadWorker::start_work() {

        if(m_serialPort->bytesAvailable()> 700) {
            QByteArray requested_data = m_serialPort->readLine();
            emit send_requested_data(requested_data);
            m_serialPort->waitForReadyRead(0);
            m_serialPort->flush();


        }

}

```

2. Non-blocking Asynchronous Way

Use the readyRead() signal to get notified when new data is available in the device instead of looping forever. This is how you should do most stuff in Qt, In order to be able to act upon multiple events that may arrive at any time. Your code can be rewritten like this:

```
connect(m_serialPort, &QSerialPort::readyRead, this, &SerialReadWorker::start_work);

void SerialReadWorker::start_work() {

    while(m_serialPort->canReadLine()) {
        QByteArray requested_data = m_serialPort->readLine();
        emit send_requested_data(requested_data);
        m_serialPort->waitForReadyRead(0);
        m_serialPort->flush();
    }

}

```




