export function AppShell({ children }) {
  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text-primary)]">
      {children}
    </div>
  );
}
