export function LoadingSpinner() {
  return (
    <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-8 shadow-soft">
      <div className="flex flex-col items-center justify-center gap-4">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-[var(--border)] border-t-[var(--accent)]"></div>
        <p className="text-sm text-[var(--text-secondary)]">Analyzing data…</p>
      </div>
    </div>
  );
}
