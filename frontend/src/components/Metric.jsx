export function Metric({ label, value }) {
  return (
    <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-3">
      <div className="text-[10px] uppercase tracking-[0.18em] text-[var(--text-secondary)]">{label}</div>
      <div className="mt-2 text-base font-medium text-[var(--text-primary)]">{value}</div>
    </div>
  );
}
