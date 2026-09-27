export function Navigation({ theme, onThemeToggle }) {
  return (
    <header className="sticky top-0 z-30 border-b border-[var(--border)] bg-[var(--surface-primary)]/80 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full border border-[var(--border)] bg-gradient-to-br from-[var(--accent)] to-[var(--accent)] text-sm font-bold text-slate-950">
            E
          </div>
          <div>
            <div className="text-lg font-semibold tracking-[-0.04em] text-[var(--text-primary)]">EarthLens</div>
            <div className="text-[10px] uppercase tracking-[0.3em] text-[var(--text-secondary)]">NASA Challenge 2026</div>
          </div>
        </div>

        <div className="hidden items-center gap-8 md:flex">
          <a href="#" className="text-sm text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">Explore</a>
          <a href="#" className="text-sm text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">Trends</a>
          <a href="#" className="text-sm text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">Compare</a>
          <a href="#" className="text-sm text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">Docs</a>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onThemeToggle}
            className="inline-flex items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-2 text-xs font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-strong)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
          <button className="inline-flex items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-2 text-xs font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-strong)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]">
            ⚙
          </button>
        </div>
      </nav>
    </header>
  );
}
