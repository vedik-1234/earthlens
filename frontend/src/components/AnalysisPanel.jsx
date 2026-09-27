export function AnalysisPanel({
  datasets,
  regions,
  selectedVariable,
  setSelectedVariable,
  selectedRegion,
  setSelectedRegion,
  startYear,
  endYear,
  setStartYear,
  setEndYear,
  onAnalyze,
  onTrendDetect,
  onCompare,
  loading,
}) {
  return (
    <aside id="analysis" className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-5 h-fit sticky top-24">
      <div className="space-y-5">
        <div>
          <label className="text-xs font-medium uppercase tracking-[0.2em] text-[var(--text-secondary)]">Variable</label>
          <select
            value={selectedVariable}
            onChange={(e) => setSelectedVariable(e.target.value)}
            className="mt-2 w-full rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)] transition"
          >
            {datasets.length ? (
              datasets.map((dataset) => (
                <option key={dataset.id} value={dataset.id}>
                  {dataset.label}
                </option>
              ))
            ) : (
              <>
                <option value="temperature">Temperature</option>
                <option value="precipitation">Precipitation</option>
                <option value="vegetation">Vegetation</option>
              </>
            )}
          </select>
        </div>

        <div>
          <label className="text-xs font-medium uppercase tracking-[0.2em] text-[var(--text-secondary)]">Region</label>
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="mt-2 w-full rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)] transition"
          >
            {regions.length ? (
              regions.map((region) => (
                <option key={region.id} value={region.id}>
                  {region.name || region.id.replace('_', ' ')}
                </option>
              ))
            ) : (
              <>
                <option value="global">Global</option>
                <option value="north_america">North America</option>
                <option value="south_america">South America</option>
                <option value="africa">Africa</option>
                <option value="asia">Asia</option>
                <option value="australia">Australia</option>
                <option value="arctic">Arctic</option>
              </>
            )}
          </select>
        </div>

        <div>
          <label className="text-xs font-medium uppercase tracking-[0.2em] text-[var(--text-secondary)]">Time period</label>
          <div className="mt-2 grid grid-cols-2 gap-3">
            <input
              type="number"
              value={startYear}
              onChange={(e) => setStartYear(e.target.value)}
              min="1980"
              max="2025"
              className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)] transition"
              placeholder="Start"
            />
            <input
              type="number"
              value={endYear}
              onChange={(e) => setEndYear(e.target.value)}
              min="1980"
              max="2025"
              className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)] transition"
              placeholder="End"
            />
          </div>
        </div>

        <div className="space-y-3 border-t border-[var(--border)] pt-4">
          <button
            onClick={onAnalyze}
            disabled={loading}
            className="w-full rounded-full bg-[var(--accent)] px-4 py-3 text-sm font-medium text-slate-950 transition hover:brightness-95 disabled:cursor-not-allowed disabled:opacity-60 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--accent)]"
          >
            {loading ? 'Analyzing…' : 'Analyze Trend'}
          </button>
          <button
            onClick={onTrendDetect}
            disabled={loading}
            className="w-full rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-4 py-3 text-sm font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-strong)] disabled:opacity-60 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--accent)]"
          >
            Find Interesting Trends
          </button>
          <button
            onClick={onCompare}
            disabled={loading}
            className="w-full rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-4 py-3 text-sm font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-strong)] disabled:opacity-60 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--accent)]"
          >
            Compare Variables
          </button>
        </div>
      </div>
    </aside>
  );
}
