#ifndef MPLOTVISUALIZATION_H
#define MPLOTVISUALIZATION_H

#include <QObject>
#include <QWidget>
#include "qcustomplot.h"
#define   WINDOW_SIZE   100


class MplotVisualization : public QWidget
{
    Q_OBJECT
public:
    explicit MplotVisualization(QWidget *parent = nullptr);
    ~MplotVisualization();

    QSize sizeHint() const override;
    void init_x_timing_vector();
    void init_plot_configurations();
public slots:
     void plot_requested_data(QVector<double>& data);
     void decode_requested_data(QByteArray byte_array);

private:
    QCustomPlot *m_plot = nullptr;
    //QVBoxLayout* m_layout = nullptr;
    bool m_set_layout_flag = false;
    QVector<double> m_received_data;
public:
    QVector<double> m_x_timing_vector;

signals:

};

#endif // MPLOTVISUALIZATION_H
