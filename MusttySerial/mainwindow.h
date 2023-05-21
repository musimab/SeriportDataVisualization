#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QSerialPortInfo>
#include <QDebug>
#include <QComboBox>
#include <QGridLayout>
#include <QLabel>
#include <QThread>
#include <QAction>
#include <QTabWidget>
#include <QSizePolicy>
#include <QDockWidget>
#include <QList>
#include "serialreadworker.h"
#include "mplotvisualization.h"
#define BUF_SIZE 100
#define  WINDOW_SIZE 100
QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr );
    ~MainWindow();
    void list_available_serial_ports(void);
    void port_connect();
    void port_disconnect();
    void port_receive_data(QByteArray data);
    void  clear_workspace();
    void open_test_folder_slot();
    void  start_serial_read_process();
    void  port_send_data_from_line_editor();
    void  write_signal_received();

    void add_mpl_visualition_dock_widget();

    void make_signal_slot_connection();
    void stop_worker_threads();


private:
    Ui::MainWindow *ui;

    QThread* SerialReadWorkerThread =nullptr;
    SerialReadWorker* m_worker_reader;
    bool m_connect_button_pressed = false;

    MplotVisualization* m_plot_visualization_widget = nullptr;

    QVector<double> m_received_data;

signals:
    void write_data_signal(QByteArray);
    void plot_requested_data_signal(QVector<double>& data);


private slots:
    void on_checkbox_save_txt_clicked(bool checked);
    void on_pushButton_connect_clicked(bool checked);
};
#endif // MAINWINDOW_H
