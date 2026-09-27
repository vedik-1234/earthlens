export function ComparisonView({ compareData }) {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Compare</p>
        <h3 className="mt-1 text-2xl font-medium text-[var(--text-primary)]">Variable A | Variable B</h3>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Variable A</div>
          <div className="mt-3 text-xl font-medium text-[var(--text-primary)]">{compareData.variable_a?.variable || 'Temperature'}</div>
          <div className="mt-2 text-sm text-[var(--text-secondary)]">Trend: {compareData.variable_a?.trend ?? 0.038} {compareData.variable_a?.unit || '°C/year'}</div>
        </div>

        <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4">
          <div className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Variable B</div>
          <div className="mt-3 text-xl font-medium text-[var(--text-primary)]">{compareData.variable_b?.variable || 'Precipitation'}</div>
          <div className="mt-2 text-sm text-[var(--text-secondary)]">Trend: {compareData.variable_b?.trend ?? 0.4} {compareData.variable_b?.unit || 'mm/month'}</div>
        </div>
      </div>

      <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4 text-sm leading-6 text-[var(--text-secondary)]">
        <div className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Association</div>
        <div className="mt-3">
          <span className="font-medium text-[var(--text-primary)]">Correlation:</span> {compareData.association?.correlation ?? 0.67}
        </div>
        <p className="mt-2">{compareData.association?.interpretation || 'Statistical association detected between the selected variables.'}</p>
        <p className="mt-1">{compareData.association?.caution || 'This does not imply causation.'}</p>
      </div>
    </div>
  );
}
