export function Hero() {
  return (
    <section className="mx-auto max-w-7xl px-4 pb-10 pt-12 sm:px-6 lg:px-8 lg:pt-20">
      <div className="rounded-[32px] border border-[var(--border)] bg-[var(--surface-primary)] p-6 shadow-soft sm:p-8 lg:p-12">
        <div className="grid gap-10 lg:grid-cols-[1.15fr_0.85fr] lg:items-center">
          <div>
            <p className="text-xs uppercase tracking-[0.28em] text-[var(--text-secondary)]">EarthLens</p>
            <h1 className="mt-5 max-w-2xl text-4xl font-semibold tracking-[-0.08em] text-[var(--text-primary)] sm:text-5xl lg:text-6xl">
              Understand how Earth's systems are changing.
            </h1>
            <p className="mt-6 max-w-2xl text-base leading-7 text-[var(--text-secondary)] sm:text-lg">
              Explore NASA Earth-observation data, discover spatial patterns, quantify environmental trends, and test their statistical significance with transparent scientific analysis.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <a href="#analysis" className="inline-flex items-center justify-center rounded-full bg-[var(--accent)] px-6 py-3 text-sm font-medium text-slate-950 transition hover:brightness-95 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--accent)]">
                Start Investigating
              </a>
              <a href="#trends" className="inline-flex items-center justify-center rounded-full border border-[var(--border)] px-6 py-3 text-sm font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-secondary)] focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--accent)]">
                Find Trends
              </a>
            </div>
          </div>

          <div className="rounded-[28px] border border-[var(--border)] bg-[radial-gradient(circle_at_top,_rgba(110,168,254,0.1),_transparent_60%)] p-6 backdrop-blur-sm">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Data source</p>
                <p className="mt-2 text-lg font-medium text-[var(--text-primary)]">NASA Earthdata</p>
              </div>
              <div className="rounded-full border border-[var(--border)] bg-white/40 px-3 py-1 text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)] dark:bg-slate-900/40">Demo</div>
            </div>
            <div className="space-y-4 text-sm leading-6 text-[var(--text-secondary)]">
              <p>🔬 Rigorous statistical analysis with confidence intervals and significance testing.</p>
              <p>📊 Real environmental variables from NASA observation systems and climate models.</p>
              <p>🗺️ Spatial trend detection across regions and time periods.</p>
              <p>✅ Transparent methodology and scientific limitations disclosed.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
