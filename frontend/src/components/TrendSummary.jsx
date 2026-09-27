export function TrendSummary({ analysis }) {
  const direction = analysis.statistically_significant ? (analysis.trend >= 0 ? 'Increasing' : 'Decreasing') : 'No significant trend';

  return (
    <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Trend result</p>
        <div className="mt-3 flex items-baseline gap-3">
          <div className="text-4xl font-semibold tracking-[-0.07em] text-[var(--text-primary)] sm:text-5xl">
            {analysis.trend >= 0 ? '+' : ''}{(analysis.trend ?? 0.038).toFixed(3)}
          </div>
          <div className="text-lg text-[var(--text-secondary)]">{analysis.unit || '°C/year'}</div>
        </div>
      </div>

      <div className="text-left sm:text-right">
        <div className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Direction</div>
        <div className="mt-2 text-xl font-medium text-[var(--text-primary)]">{direction}</div>
        <div className="mt-1 text-sm text-[var(--text-secondary)]">{analysis.period || '2003–2025'}</div>
      </div>
    </div>
  );
}
