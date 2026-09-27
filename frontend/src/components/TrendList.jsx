export function TrendList({ items }) {
  return (
    <div className="space-y-3">
      {items.map((item, index) => (
        <div key={`${item.variable}-${index}`} className="flex items-center justify-between rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4 transition hover:border-[var(--accent)]/30 hover:bg-[var(--surface-primary)]">
          <div>
            <div className="text-lg font-medium text-[var(--text-primary)]">{item.label || item.variable}</div>
            <div className="mt-1 text-sm text-[var(--text-secondary)]">{item.direction || 'Increasing'} · {item.trend >= 0 ? '+' : ''}{item.trend ?? 0.0} {item.unit}</div>
            <div className="mt-1 text-xs uppercase tracking-[0.16em] text-[var(--text-secondary)]">{item.period || '2003–2025'}</div>
          </div>
          <div className="text-xl text-[var(--text-secondary)]">›</div>
        </div>
      ))}
    </div>
  );
}
