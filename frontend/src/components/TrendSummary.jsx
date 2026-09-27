export function TrendSummary({ analysis }) {
  const direction = analysis.statistically_significant
    ? analysis.trend >= 0
      ? 'Increasing'
      : 'Decreasing'
    : 'No significant trend';

  const trendColor = analysis.trend >= 0 ? 'text-emerald-600' : 'text-rose-500';

  return (
    <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Detected trend</p>
        <div className="mt-3 flex items-baseline gap-3">
          <div className={`text-5xl font-bold tracking-[-0.08em] ${trendColor}`}>
            {analysis.trend >= 0 ? '+' : ''}{(analysis.trend ?? 0.038).toFixed(3)}
          </div>
          <div className="text-lg text-[var(--text-secondary)]">{analysis.unit || '°C/year'}</div>
        </div>
      </div>

      <div className="text-left sm:text-right">
        <div className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Direction</div>
        <div className={`mt-2 text-xl font-semibold ${trendColor}`}>{direction}</div>
        <div className="mt-1 text-sm text-[var(--text-secondary)]">{analysis.period || '2003–2025'}</div>
      </div>
    </div>
  );
}
