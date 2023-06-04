// components/LineChart.js
import React from "react";
import { Bar } from "react-chartjs-2";
function BarChart({ chartData }) {
  return (
    <div className="bar-chart-container">
      <h2 style={{ textAlign: "center" }}>Bar Chart</h2>
      <Bar
        data={chartData}
        options={{
            responsive: true,
            interaction: {
              mode: 'nearest',
            },
            plugins: {
              title: {
                display: true,
                text: 'Bar Chart of sensor readings x: Time - y: Value(ppm)'
              },
              zoom: {
                pan: {
                    enabled: true,
                    mode: 'x'
                },
                zoom: {
                    pinch: {
                        enabled: true       // Enable pinch zooming
                    },
                    wheel: {
                        enabled: true       // Enable wheel zooming
                    },
                    mode: 'x',
                }
            }
            },
            scales: {
              x: {
                type: 'time',
                display: true,
                title: {
                  display: true,
                  text: 'Date-Time'
                },
                ticks: {
                  autoSkip: false,
                  maxRotation: 0,
                  major: {
                    enabled: true
                  },
                  font: function(context) {
                    if (context.tick && context.tick.major) {
                      return {
                        weight: 'bold',
                      };
                    }
                  }
                }
              },
              y: {
                display: true,
                title: {
                  display: true,
                  text: 'value'
                }
              }
            }
          }}
      />
    </div>
  );
}
export default BarChart;