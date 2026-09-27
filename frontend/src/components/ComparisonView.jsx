export function ComparisonView({ compareData }) {
  const varA = compareData?.variable_a || { variable: 'Temperature', trend: 0.038, unit: '°C/year' };
  const varB = compareData?.variable_b || { variable: 'Precipitation', trend: 0.4, unit: 'mm/month' };
  const association = compareData?.association || { correlation: 0.67, interpretation: 'Statistical association detected.', caution: 'This does not imply causation.' };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Comparison</p>
        <h3 className="mt-1 text-2xl font-medium text-[var(--text-primary)]">Variable analysis</h3>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4">
          <div className="text-xs font-medium uppercase tracking-[0.2em] text-[var(--text-secondary)]">Variable A</div>
          <div className="mt-3 text-xl font-semibold text-[var(--text-primary)]">{varA.dataset_name || varA.variable || 'Temperature'}</div>
          <div className="mt-3 space-y-2 text-sm">
            <div className="text-[var(--text-secondary)]">
              Trend: <span className="font-medium text-[var(--text-primary)]">{varA.trend >= 0 ? '+' : ''}{(varA.trend ?? 0.038).toFixed(3)} {varA.unit || '°C/year'}</span>
            </div>
            <div className="text-[var(--text-secondary)]">
              Change: <span className="font-medium text-[var(--text-primary)]">{(varA.total_change ?? 0.84).toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4">
          <div className="text-xs font-medium uppercase tracking-[0.2em] text-[var(--text-secondary)]">Variable B</div>
          <div className="mt-3 text-xl font-semibold text-[var(--text-primary)]">{varB.dataset_name || varB.variable || 'Precipitation'}</div>
          <div className="mt-3 space-y-2 text-sm">
            <div className="text-[var(--text-secondary)]">
              Trend: <span className="font-medium text-[var(--text-primary)]">{varB.trend >= 0 ? '+' : ''}{(varB.trend ?? 0.4).toFixed(3)} {varB.unit || 'mm/month'}</span>
            </div>
            <div className="text-[var(--text-secondary)]">
              Change: <span className="font-medium text-[var(--text-primary)]">{(varB.total_change ?? 12.0).toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4">
        <div className="text-xs font-medium uppercase tracking-[0.2em] text-[var(--text-secondary)]">Statistical association</div>
        <div className="mt-3 space-y-3 text-sm leading-6">
          <div>
            <span className="font-medium text-[var(--text-primary)]">Correlation coefficient:</span>
            <div className="mt-1 text-[var(--text-secondary)]">{(association.correlation ?? 0.67).toFixed(3)}</div>
          </div>
          <p className="text-[var(--text-secondary)]">{association.interpretation || 'Statistical association detected between variables.'}</p>
          <p className="rounded-xl border border-[var(--border)] bg-white/20 p-2 text-xs text-[var(--text-secondary)] dark:bg-slate-900/20">
            ⚠️ {association.caution || 'This does not imply causation.'}
          </p>
        </div>
      </div>
    </div>
  );
}
