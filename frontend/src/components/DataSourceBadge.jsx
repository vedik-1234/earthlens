export function DataSourceBadge({ label }) {
  return (
    <span className="inline-flex items-center rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-1.5 text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--text-secondary)]">
      {label}
    </span>
  );
}
