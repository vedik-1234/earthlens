export function Navigation({ theme, onThemeToggle }) {
  return (
    <header className="sticky top-0 z-30 border-b border-[var(--border)] bg-[var(--surface-primary)]/80 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] text-sm font-semibold text-[var(--text-primary)]">E</div>
          <div>
            <div className="text-lg font-semibold tracking-[-0.04em] text-[var(--text-primary)]">EarthLens</div>
          </div>
        </div>

        <div className="hidden items-center gap-8 md:flex">
          <a href="#" className="text-sm text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">Explore</a>
          <a href="#" className="text-sm text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">Trends</a>
          <a href="#" className="text-sm text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">Compare</a>
          <a href="#" className="text-sm text-[var(--text-secondary)] transition hover:text-[var(--text-primary)]">About</a>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onThemeToggle}
            className="inline-flex items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-2 text-xs font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-strong)]"
          >
            {theme === 'light' ? 'Dark' : 'Light'}
          </button>
          <button className="inline-flex items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-2 text-xs font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-strong)]">
            Settings
          </button>
        </div>
      </nav>
    </header>
  );
}

export function Hero() {
  return (
    <section className="mx-auto max-w-7xl px-4 pb-10 pt-12 sm:px-6 lg:px-8 lg:pt-20">
      <div className="rounded-[32px] border border-[var(--border)] bg-[var(--surface-primary)] p-6 shadow-soft sm:p-8 lg:p-12">
        <div className="grid gap-10 lg:grid-cols-[1.15fr_0.85fr] lg:items-center">
          <div>
            <p className="text-xs uppercase tracking-[0.28em] text-[var(--text-secondary)]">EARTHLENS</p>
            <h1 className="mt-5 max-w-xl text-4xl font-semibold tracking-[-0.08em] text-[var(--text-primary)] sm:text-5xl lg:text-7xl">
              Understand how Earth’s systems are changing.
            </h1>
            <p className="mt-6 max-w-xl text-base leading-7 text-[var(--text-secondary)] sm:text-lg">
              Explore NASA Earth-observation data, discover spatial patterns, quantify environmental trends, and test their statistical significance.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <a href="#analysis" className="inline-flex items-center justify-center rounded-full bg-[var(--accent)] px-5 py-3 text-sm font-medium text-slate-950 transition hover:brightness-95">
                Start Investigating
              </a>
              <a href="#trends" className="inline-flex items-center justify-center rounded-full border border-[var(--border)] px-5 py-3 text-sm font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-secondary)]">
                Find Interesting Trends
              </a>
            </div>
          </div>

          <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-secondary)] p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Data source</p>
                <p className="mt-2 text-lg font-medium text-[var(--text-primary)]">NASA Earthdata</p>
              </div>
              <div className="rounded-full border border-[var(--border)] bg-white/40 px-3 py-1 text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)] dark:bg-slate-900/40">Demo mode</div>
            </div>
            <div className="mt-6 space-y-4 text-sm leading-6 text-[var(--text-secondary)]">
              <p>Measured environmental variables are processed with transparent statistics and scientific metadata.</p>
              <p>Every result includes dataset provenance, trend estimates, confidence intervals, and significance testing.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
