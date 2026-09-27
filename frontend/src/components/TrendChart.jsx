import Plot from 'react-plotly.js';

export function TrendChart({ series, fittedSeries, unit }) {
  const isDark = typeof window !== 'undefined' && document.documentElement.dataset.theme === 'dark';
  const textColor = isDark ? '#f3f6fb' : '#0f172a';
  const gridColor = isDark ? 'rgba(148, 163, 184, 0.15)' : 'rgba(15, 23, 42, 0.1)';

  return (
    <div>
      <div className="mb-4">
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Time series</p>
        <h3 className="mt-1 text-xl font-medium text-[var(--text-primary)]">Observed and modeled trend</h3>
      </div>
      <div className="h-[360px] w-full rounded-2xl overflow-hidden">
        <Plot
          data={[
            {
              x: series.map((pt) => pt.year),
              y: series.map((pt) => pt.value),
              type: 'scatter',
              mode: 'markers',
              marker: { color: '#6ea8fe', size: 7, opacity: 0.75 },
              name: 'Observed',
              hovertemplate: '<b>%{x}</b><br>Value: %{y:.3f}<extra></extra>',
            },
            {
              x: fittedSeries.map((pt) => pt.year),
              y: fittedSeries.map((pt) => pt.value),
              type: 'scatter',
              mode: 'lines',
              line: { color: textColor, width: 3, shape: 'linear' },
              name: 'Fitted trend',
              hovertemplate: '<b>%{x}</b><br>Trend: %{y:.3f}<extra></extra>',
            },
          ]}
          layout={{
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            margin: { l: 50, r: 20, t: 10, b: 45 },
            font: { family: '-apple-system, BlinkMacSystemFont, SF Pro Text, sans-serif', color: textColor, size: 12 },
            xaxis: {
              title: { text: 'Year', font: { size: 13 } },
              showgrid: true,
              gridcolor: gridColor,
              zeroline: false,
              dtick: 5,
            },
            yaxis: {
              title: { text: unit, font: { size: 13 } },
              showgrid: true,
              gridcolor: gridColor,
              zeroline: false,
            },
            showlegend: true,
            legend: { orientation: 'h', x: 0.5, y: -0.2, xanchor: 'center', yanchor: 'top' },
            hovermode: 'x unified',
          }}
          config={{ responsive: true, displayModeBar: false, staticPlot: false }}
          style={{ width: '100%', height: '100%' }}
          useResizeHandler
        />
      </div>
    </div>
  );
}
