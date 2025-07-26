import React from 'react';
import Plot from 'react-plotly.js';

function ChartComponent({ spec, data }) {
  if (!spec || !data) return null;

  const xData = data.data.map(row => row[data.columns.indexOf(spec.x_column)]);
  const yData = data.data.map(row => row[data.columns.indexOf(spec.y_column)]);

  return (
    <Plot
      data={[
        {
          x: xData,
          y: yData,
          type: spec.chart_type,
          mode: 'lines+markers',
          marker: { color: '#646cff' },
          labels: xData,
          values: yData,
          text: yData.map(String),
          textposition: 'auto',
        },
      ]}
      layout={{
        title: spec.title,
        paper_bgcolor: '#242424',
        plot_bgcolor: '#242424',
        font: {
          color: 'rgba(255, 255, 255, 0.87)',
        },
        xaxis: {
          title: spec.x_column,
          // --- NEW: Explicitly set title font color ---
          titlefont: {
            color: 'rgba(255, 255, 255, 0.87)',
          },
        },
        yaxis: {
          title: spec.y_column,
          // --- NEW: Explicitly set title font color ---
          titlefont: {
            color: 'rgba(255, 255, 255, 0.87)',
          },
        },
      }}
      style={{ width: '100%', height: '100%' }}
    />
  );
}

export default ChartComponent;