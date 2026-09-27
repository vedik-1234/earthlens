export function AnalysisPanel({ datasets, selectedVariable, setSelectedVariable, selectedRegion, setSelectedRegion, startYear, endYear, setStartYear, setEndYear, onAnalyze, onTrendDetect, onCompare, loading }) {
  const regions = ['global', 'north_america', 'south_america', 'africa', 'asia', 'australia', 'arctic'];

  return (
    <aside id="analysis" className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-5">
      <div className="space-y-5">
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Variable</label>
          <select value={selectedVariable} onChange={(e) => setSelectedVariable(e.target.value)} className="mt-2 w-full rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)]">
            {datasets.length ? datasets.map((dataset) => (
              <option key={dataset.id} value={dataset.id}>{dataset.label}</option>
            )) : (
              <>
                <option value="temperature">Temperature</option>
                <option value="precipitation">Precipitation</option>
                <option value="vegetation">Vegetation</option>
              </>
            )}
          </select>
        </div>

        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Region</label>
          <select value={selectedRegion} onChange={(e) => setSelectedRegion(e.target.value)} className="mt-2 w-full rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)]">
            {regions.map((region) => (
              <option key={region} value={region}>{region.replace('_', ' ')}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Time</label>
          <div className="mt-2 grid grid-cols-2 gap-3">
            <input type="number" value={startYear} onChange={(e) => setStartYear(e.target.value)} className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)]" />
            <input type="number" value={endYear} onChange={(e) => setEndYear(e.target.value)} className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)]" />
          </div>
        </div>

        <div className="space-y-3 pt-2">
          <button onClick={onAnalyze} disabled={loading} className="w-full rounded-full bg-[var(--accent)] px-4 py-3 text-sm font-medium text-slate-950 transition hover:brightness-95 disabled:cursor-not-allowed disabled:opacity-60">
            {loading ? 'Analyzing…' : 'Analyze Trend'}
          </button>
          <button onClick={onTrendDetect} className="w-full rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-4 py-3 text-sm font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-strong)]">
            Find Interesting Trends
          </button>
          <button onClick={onCompare} className="w-full rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-4 py-3 text-sm font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-strong)]">
            Compare Variables
          </button>
        </div>
      </div>
    </aside>
  );
}
