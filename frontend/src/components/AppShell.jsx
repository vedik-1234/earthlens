import React from 'react';

export function AppShell({ children }) {
  return <div className="min-h-screen bg-[var(--bg)] text-[var(--text-primary)]">{children}</div>;
}

export function Button({ variant = 'primary', children, ...props }) {
  const base = 'inline-flex items-center justify-center rounded-full px-5 py-3 text-sm font-medium transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--accent)] focus-visible:ring-offset-2';
  const styles = variant === 'primary'
    ? 'bg-[var(--accent)] text-slate-950 shadow-sm hover:brightness-95'
    : 'border border-[var(--border)] bg-transparent text-[var(--text-primary)] hover:bg-[var(--surface-secondary)]';

  return <button className={`${base} ${styles}`} {...props}>{children}</button>;
}
