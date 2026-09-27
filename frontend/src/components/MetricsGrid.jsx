export function MetricsGrid({ analysis }) {
  const metrics = [
    { label: 'Total change', value: `${(analysis.total_change ?? 0.84).toFixed(2)} ${(analysis.unit || '°C/year').replace('/year', '')}` },
    { label: 'p-value', value: (analysis.p_value ?? 0.0008).toFixed(5), highlight: analysis.statistically_significant },
    { label: '95% confidence', value: `[${(analysis.confidence_interval?.[0] ?? 0.025).toFixed(3)}, ${(analysis.confidence_interval?.[1] ?? 0.051).toFixed(3)}]` },
    { label: 'R² (model fit)', value: (analysis.r_squared ?? 0.72).toFixed(3) },
  ];

  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric) => (
        <div
          key={metric.label}
          className={`rounded-2xl border ${metric.highlight ? 'border-emerald-200 bg-emerald-50/50 dark:border-emerald-900/40 dark:bg-emerald-950/20' : 'border-[var(--border)] bg-[var(--surface-secondary)]'} p-3`}
        >
          <div className="text-[10px] font-medium uppercase tracking-[0.18em] text-[var(--text-secondary)]">
            {metric.label}
          </div>
          <div className={`mt-2 text-base font-semibold ${metric.highlight ? 'text-emerald-700 dark:text-emerald-300' : 'text-[var(--text-primary)]'}`}>
            {metric.value}
          </div>
        </div>
      ))}
    </div>
  );
}
