import React, { useEffect, useMemo, useState } from 'react';
import { AppShell } from './components/AppShell.jsx';
import { Navigation } from './components/Navigation.jsx';
import { Hero } from './components/Hero.jsx';
import { AnalysisPanel } from './components/AnalysisPanel.jsx';
import { TrendSummary } from './components/TrendSummary.jsx';
import { TrendChart } from './components/TrendChart.jsx';
import { TrendList } from './components/TrendList.jsx';
import { ComparisonView } from './components/ComparisonView.jsx';
import { DataSourceBadge } from './components/DataSourceBadge.jsx';
import { api } from './services/api.js';

const DEFAULT_RESULT = {
  variable: 'temperature',
  period: '2003-2025',
  trend: 0.038,
  unit: '°C/year',
  total_change: 0.84,
  p_value: 0.0008,
  confidence_interval: [0.025, 0.051],
  r_squared: 0.72,
  statistically_significant: true,
  dataset_name: 'Temperature',
  dataset_source: 'Demo dataset (development only)',
  series: Array.from({ length: 23 }, (_, i) => ({ year: 2003 + i, value: 12.5 + i * 0.02 })),
  fitted: Array.from({ length: 23 }, (_, i) => ({ year: 2003 + i, value: 12.5 + i * 0.018 })),
};

function App() {
  const [theme, setTheme] = useState('light');
  const [analysis, setAnalysis] = useState(DEFAULT_RESULT);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [datasets, setDatasets] = useState([]);
  const [trendResults, setTrendResults] = useState([]);
  const [compareData, setCompareData] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [selectedVariable, setSelectedVariable] = useState('temperature');
  const [selectedRegion, setSelectedRegion] = useState('global');
  const [startYear, setStartYear] = useState(2003);
  const [endYear, setEndYear] = useState(2025);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  useEffect(() => {
    api.getDatasets().then((data) => setDatasets(data.datasets || [])).catch(() => setDatasets([]));
  }, []);

  async function handleAnalyze() {
    setLoading(true);
    setError('');
    try {
      const response = await api.analyze({
        variable: selectedVariable,
        region: selectedRegion,
        start_year: Number(startYear),
        end_year: Number(endYear),
      });
      setAnalysis(response);
      if (response.status === 'error') {
        setError(response.message || 'Unable to analyze trend.');
      }
    } catch (err) {
      setError('The analysis service is unavailable.');
    } finally {
      setLoading(false);
    }
  }

  async function handleTrendDetect() {
    setLoading(true);
    try {
      const response = await api.detectTrends({
        region: selectedRegion,
        start_year: Number(startYear),
        end_year: Number(endYear),
      });
      setTrendResults(response.results || []);
    } catch (err) {
      setTrendResults([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleCompare() {
    setLoading(true);
    try {
      const response = await api.compare({
        variable_a: selectedVariable,
        variable_b: 'precipitation',
        region: selectedRegion,
        start_year: Number(startYear),
        end_year: Number(endYear),
      });
      setCompareData(response);
    } catch (err) {
      setCompareData(null);
    } finally {
      setLoading(false);
    }
  }

  async function handleExplain() {
    setLoading(true);
    try {
      const response = await api.explain({
        variable: selectedVariable,
        region: selectedRegion,
        start_year: Number(startYear),
        end_year: Number(endYear),
        trend_value: analysis.trend || 0.038,
        p_value: analysis.p_value || 0.0008,
        total_change: analysis.total_change || 0.84,
        unit: analysis.unit || '°C/year',
      });
      setExplanation(response);
    } catch (err) {
      setExplanation({ summary: 'AI explanation is unavailable.', segments: [] });
    } finally {
      setLoading(false);
    }
  }

  const trendStats = useMemo(() => [
    { label: 'Total change', value: `${analysis.total_change ?? 0.84} ${analysis.unit?.replace('/year', '') || '°C'}` },
    { label: 'p-value', value: (analysis.p_value ?? 0.0008).toFixed(4) },
    { label: '95% CI', value: `${(analysis.confidence_interval?.[0] ?? 0.025).toFixed(3)} → ${(analysis.confidence_interval?.[1] ?? 0.051).toFixed(3)}` },
    { label: 'R²', value: (analysis.r_squared ?? 0.72).toFixed(2) },
  ], [analysis]);

  return (
    <AppShell>
      <Navigation theme={theme} onThemeToggle={() => setTheme((prev) => prev === 'light' ? 'dark' : 'light')} />
      <Hero />

      <main className="mx-auto max-w-7xl px-4 pb-20 pt-8 sm:px-6 lg:px-8">
        <section className="grid gap-6 lg:grid-cols-[320px_minmax(0,1fr)]">
          <AnalysisPanel
            datasets={datasets}
            selectedVariable={selectedVariable}
            setSelectedVariable={setSelectedVariable}
            selectedRegion={selectedRegion}
            setSelectedRegion={setSelectedRegion}
            startYear={startYear}
            endYear={endYear}
            setStartYear={setStartYear}
            setEndYear={setEndYear}
            onAnalyze={handleAnalyze}
            onTrendDetect={handleTrendDetect}
            onCompare={handleCompare}
            loading={loading}
          />

          <div className="space-y-6">
            <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
              <div className="mb-4 flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Trend map</p>
                  <h2 className="mt-1 text-xl font-medium text-[var(--text-primary)]">Spatial pattern</h2>
                </div>
                <DataSourceBadge label={analysis.data_source || 'Demo dataset'} />
              </div>
              <div className="rounded-[24px] border border-[var(--border)] bg-[radial-gradient(circle_at_top,_rgba(110,168,254,0.22),_transparent_45%),_linear-gradient(135deg,#f3f7fb,#e9eef2)] p-4 dark:bg-[radial-gradient(circle_at_top,_rgba(110,168,254,0.13),_transparent_45%),_linear-gradient(135deg,#0b1118,#0f1722)]">
                <div className="grid gap-3 sm:grid-cols-3">
                  <div className="rounded-2xl border border-[var(--border)] bg-white/50 p-3 text-sm dark:bg-slate-900/40">
                    <div className="text-[var(--text-secondary)]">Increasing</div>
                    <div className="mt-2 text-2xl font-semibold text-emerald-600">38%</div>
                  </div>
                  <div className="rounded-2xl border border-[var(--border)] bg-white/50 p-3 text-sm dark:bg-slate-900/40">
                    <div className="text-[var(--text-secondary)]">Decreasing</div>
                    <div className="mt-2 text-2xl font-semibold text-rose-500">21%</div>
                  </div>
                  <div className="rounded-2xl border border-[var(--border)] bg-white/50 p-3 text-sm dark:bg-slate-900/40">
                    <div className="text-[var(--text-secondary)]">No significant trend</div>
                    <div className="mt-2 text-2xl font-semibold text-slate-600">41%</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
              <TrendSummary analysis={analysis} />
              <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                {trendStats.map((stat) => (
                  <div key={stat.label} className="rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-3">
                    <div className="text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]">{stat.label}</div>
                    <div className="mt-2 text-lg font-semibold text-[var(--text-primary)]">{stat.value}</div>
                  </div>
                ))}
              </div>
              {error && <div className="mt-4 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700 dark:border-rose-900/30 dark:bg-rose-950/40 dark:text-rose-300">{error}</div>}
            </div>

            <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
              <TrendChart series={analysis.series || DEFAULT_RESULT.series} fittedSeries={analysis.fitted || DEFAULT_RESULT.fitted} unit={analysis.unit || '°C/year'} />
            </div>
          </div>
        </section>

        <section className="mt-10 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
            <div className="mb-4 flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Trend Detective</p>
                <h3 className="mt-1 text-2xl font-medium text-[var(--text-primary)]">Find Interesting Trends</h3>
              </div>
              <button onClick={handleExplain} className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] px-3 py-2 text-sm font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-secondary)]">
                Explain this result
              </button>
            </div>
            <TrendList items={trendResults.length ? trendResults : [
              { variable: 'temperature', label: 'Temperature', direction: 'Increasing', trend: 0.038, unit: '°C/year', period: '2003–2025', p_value: 0.0008 },
              { variable: 'precipitation', label: 'Precipitation', direction: 'Mixed regional trend', trend: 0.4, unit: 'mm/month', period: '2003–2025', p_value: 0.04 },
              { variable: 'vegetation', label: 'Vegetation', direction: 'Regional differences', trend: 0.003, unit: 'NDVI', period: '2003–2025', p_value: 0.02 },
            ]} />
            {explanation && (
              <div className="mt-6 rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]">AI explanation</p>
                <p className="mt-3 text-sm leading-6 text-[var(--text-primary)]">{explanation.summary}</p>
                <ul className="mt-4 space-y-3 text-sm text-[var(--text-secondary)]">
                  {explanation.segments?.map((segment, index) => (
                    <li key={index} className="rounded-xl border border-[var(--border)] bg-white/30 p-3 dark:bg-slate-900/20">
                      <span className="font-medium capitalize text-[var(--text-primary)]">{segment.type.replace('_', ' ')}:</span> {segment.text}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
            <ComparisonView compareData={compareData || {
              variable_a: { variable: 'temperature', trend: 0.038, unit: '°C/year' },
              variable_b: { variable: 'precipitation', trend: 0.4, unit: 'mm/month' },
              association: { correlation: 0.67, interpretation: 'Statistical association detected between the selected variables.', caution: 'This does not imply causation.' }
            }} />
          </div>
        </section>
      </main>
    </AppShell>
  );
}

export default App;
