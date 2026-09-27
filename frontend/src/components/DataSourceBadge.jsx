export function DataSourceBadge({ label }) {
  return (
    <span className="inline-flex items-center rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.22em] text-[var(--text-secondary)]">
      {label.includes('Demo') ? '🧪' : '🛰️'} {label}
    </span>
  );
}
