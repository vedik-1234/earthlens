export function TrendList({ items }) {
  return (
    <div className="space-y-3">
      {items.map((item, index) => {
        const isSignificant = item.statistically_significant !== false && item.p_value < 0.05;
        const directionEmoji = item.direction?.toLowerCase().includes('increas') ? '📈' : item.direction?.toLowerCase().includes('decreas') ? '📉' : '📊';

        return (
          <button
            key={`${item.variable}-${index}`}
            className="w-full text-left rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4 transition hover:border-[var(--accent)]/50 hover:bg-[var(--surface-primary)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{directionEmoji}</span>
                  <div className="text-lg font-semibold text-[var(--text-primary)]">{item.label || item.variable}</div>
                  {isSignificant && <span className="text-xs font-medium text-emerald-600">●</span>}
                </div>
                <div className="mt-2 text-sm text-[var(--text-secondary)]">
                  {item.direction || 'Trend'} · {item.trend >= 0 ? '+' : ''}{item.trend ?? 0.0} {item.unit}
                </div>
                <div className="mt-1 text-xs uppercase tracking-[0.16em] text-[var(--text-secondary)]">
                  {item.period || '2003–2025'} · p={item.p_value?.toFixed(4) || '0.05'}
                </div>
              </div>
              <div className="text-2xl text-[var(--text-secondary)] transition group-hover:text-[var(--accent)]">
                →
              </div>
            </div>
          </button>
        );
      })}
    </div>
  );
}
