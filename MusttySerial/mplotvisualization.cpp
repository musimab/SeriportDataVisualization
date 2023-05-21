#include "mplotvisualization.h"
#define PLOT_WINDOW_SIZE 100
#define y_axis_min_bound -5
#define y_axis_max_bound  5

MplotVisualization::MplotVisualization(QWidget *parent) : QWidget(parent)
{


    init_plot_configurations();
    init_x_timing_vector();


}

MplotVisualization::~MplotVisualization()
{
    qDebug() << "~MplotVisualization";
}

void MplotVisualization::plot_requested_data(QVector<double>& y)
{


   QPen pen;

   // create graph and assign data to it:
   m_plot->clearGraphs();
   m_plot->addGraph();
   m_plot->graph(0)->setData(m_x_timing_vector, y);
   // give the axes some labels:
   m_plot->xAxis->setLabel("x");
   m_plot->yAxis->setLabel("y");
   pen.setWidth(5);
   pen.setColor(Qt::blue);
   // set axes ranges, so we see all data:
   m_plot->graph(0)->setName("Receive Data");
   m_plot->graph(0)->setPen(pen);
   m_plot->legend->setVisible(true);
   m_plot->replot();


}

void MplotVisualization::decode_requested_data(QByteArray byteArray)
{
    // Remove null ('\0') char from bytarray
    double received_data = byteArray.replace('\0',"").trimmed().toDouble();

    // Fill the window buffer
    if(m_received_data.size() < PLOT_WINDOW_SIZE) {
        m_received_data.append(received_data);
    }

    else {
        // buffer[1:100] = buffer[0:99]
        // buffer[100] = incomming_data
        std::copy(m_received_data.begin()+1, m_received_data.end(), m_received_data.begin());
        m_received_data.back() =  received_data;

        plot_requested_data(m_received_data);

    }
}


QSize MplotVisualization::sizeHint() const
{
    //this->setFixedSize(this->width(), this->height());
    return QSize(1000, 1000);

}

void MplotVisualization::init_x_timing_vector()
{

    for (int i=0; i < WINDOW_SIZE; ++i)
    {

      m_x_timing_vector.push_back(i);

    }
}

void MplotVisualization::init_plot_configurations()
{
    m_plot=  new QCustomPlot();
    QVBoxLayout* m_layout = new QVBoxLayout();
    m_layout->addWidget(m_plot);
    //m_layout->setSizeConstraint(QLayout::SetMaximumSize);

    m_layout->setSizeConstraint(QLayout::SetDefaultConstraint);

    m_plot->setNotAntialiasedElements(QCP::aeAll);
    QFont font;
    font.setStyleStrategy(QFont::NoAntialias);
    m_plot->xAxis->setTickLabelFont(font);
    m_plot->yAxis->setTickLabelFont(font);
    m_plot->legend->setFont(font);

    // set axes ranges, so we see all data:
    m_plot->xAxis->setRange(0, PLOT_WINDOW_SIZE);
    m_plot->yAxis->setRange(y_axis_min_bound, y_axis_max_bound);

    m_plot->legend->setVisible(true);
    m_plot->setInteractions(QCP::iRangeDrag | QCP::iRangeZoom);
    m_plot->axisRect()->setRangeDrag(Qt::Vertical);
    m_plot->axisRect()->setRangeZoom(Qt::Vertical);
    m_plot->xAxis->setLabel("x_test");
    m_plot->yAxis->setLabel("y_test");
    this->setMinimumSize(QSize(640, 480));
    setLayout(m_layout);
}
