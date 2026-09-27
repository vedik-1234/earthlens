import Plot from 'react-plotly.js';

export function TrendChart({ series, fittedSeries, unit }) {
  const observed = series.map((entry) => ({ x: entry.year, y: entry.value }));
  const fitted = fittedSeries.map((entry) => ({ x: entry.year, y: entry.value }));

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Time series</p>
          <h3 className="mt-1 text-xl font-medium text-[var(--text-primary)]">Observed and modeled trend</h3>
        </div>
      </div>
      <div className="h-[320px] w-full rounded-2xl">
        <Plot
          data={[
            {
              x: observed.map((pt) => pt.x),
              y: observed.map((pt) => pt.y),
              type: 'scatter',
              mode: 'markers',
              marker: { color: '#6ea8fe', size: 6, opacity: 0.8 },
              name: 'Observed',
            },
            {
              x: fitted.map((pt) => pt.x),
              y: fitted.map((pt) => pt.y),
              type: 'scatter',
              mode: 'lines',
              line: { color: '#111827', width: 3 },
              name: 'Trend',
            },
          ]}
          layout={{
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            margin: { l: 45, r: 18, t: 8, b: 38 },
            font: { family: '-apple-system, BlinkMacSystemFont, SF Pro Text, sans-serif', color: '#475569' },
            xaxis: { title: 'Year', showgrid: true, gridcolor: 'rgba(148,163,184,0.15)', zeroline: false },
            yaxis: { title: unit, showgrid: true, gridcolor: 'rgba(148,163,184,0.15)', zeroline: false },
            showlegend: true,
            legend: { orientation: 'h', y: -0.25 },
          }}
          config={{ responsive: true, displayModeBar: false }}
          style={{ width: '100%', height: '100%' }}
          useResizeHandler
        />
      </div>
    </div>
  );
}
