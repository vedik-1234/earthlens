import React, { useEffect, useState, useCallback } from 'react';
import { AppShell } from './components/AppShell.jsx';
import { Navigation } from './components/Navigation.jsx';
import { Hero } from './components/Hero.jsx';
import { AnalysisPanel } from './components/AnalysisPanel.jsx';
import { TrendSummary } from './components/TrendSummary.jsx';
import { TrendChart } from './components/TrendChart.jsx';
import { MetricsGrid } from './components/MetricsGrid.jsx';
import { TrendList } from './components/TrendList.jsx';
import { ComparisonView } from './components/ComparisonView.jsx';
import { DataSourceBadge } from './components/DataSourceBadge.jsx';
import { LoadingSpinner } from './components/LoadingSpinner.jsx';
import { ErrorBanner } from './components/ErrorBanner.jsx';
import { api } from './services/api.js';
import './App.css';

const DEFAULT_ANALYSIS = {
  variable: 'temperature',
  region: 'global',
  period: '2003-2025',
  trend: 0.038,
  unit: '°C/year',
  total_change: 0.84,
  p_value: 0.0008,
  confidence_interval: [0.025, 0.051],
  r_squared: 0.72,
  statistically_significant: true,
  dataset_name: 'Temperature',
  data_source: 'Demo dataset (development only)',
  is_demo: true,
  series: Array.from({ length: 23 }, (_, i) => ({ year: 2003 + i, value: 12.5 + i * 0.02 + Math.random() * 0.3 })),
  fitted: Array.from({ length: 23 }, (_, i) => ({ year: 2003 + i, value: 12.5 + i * 0.018 })),
  trend_direction: 'increasing',
  status: 'success',
};

function App() {
  const [theme, setTheme] = useState('light');
  const [analysis, setAnalysis] = useState(DEFAULT_ANALYSIS);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [datasets, setDatasets] = useState([]);
  const [regions, setRegions] = useState([]);
  const [trendResults, setTrendResults] = useState([]);
  const [compareData, setCompareData] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [selectedVariable, setSelectedVariable] = useState('temperature');
  const [selectedRegion, setSelectedRegion] = useState('global');
  const [startYear, setStartYear] = useState(2003);
  const [endYear, setEndYear] = useState(2025);
  const [activeTab, setActiveTab] = useState('analyze');

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  useEffect(() => {
    async function fetchMetadata() {
      try {
        const [datasetsRes, regionsRes] = await Promise.all([
          api.getDatasets(),
          api.getRegions(),
        ]);
        if (datasetsRes.datasets) setDatasets(datasetsRes.datasets);
        if (regionsRes.regions) setRegions(Object.values(regionsRes.regions));
      } catch (err) {
        console.error('Error fetching metadata:', err);
      }
    }
    fetchMetadata();
  }, []);

  const handleAnalyze = useCallback(async () => {
    setLoading(true);
    setError('');
    setActiveTab('analyze');
    try {
      const response = await api.analyze({
        variable: selectedVariable,
        region: selectedRegion,
        start_year: Number(startYear),
        end_year: Number(endYear),
      });
      if (response.status === 'error') {
        setError(response.message || 'Unable to analyze trend.');
        setAnalysis(DEFAULT_ANALYSIS);
      } else {
        setAnalysis(response);
        setError('');
      }
    } catch (err) {
      setError('The analysis service is unavailable.');
      setAnalysis(DEFAULT_ANALYSIS);
    } finally {
      setLoading(false);
    }
  }, [selectedVariable, selectedRegion, startYear, endYear]);

  const handleTrendDetect = useCallback(async () => {
    setLoading(true);
    setError('');
    setActiveTab('trends');
    try {
      const response = await api.detectTrends({
        region: selectedRegion,
        start_year: Number(startYear),
        end_year: Number(endYear),
      });
      if (response.status === 'success') {
        setTrendResults(response.results || []);
      } else {
        setError('Unable to detect trends.');
        setTrendResults([]);
      }
    } catch (err) {
      setError('Trend detection failed.');
      setTrendResults([]);
    } finally {
      setLoading(false);
    }
  }, [selectedRegion, startYear, endYear]);

  const handleCompare = useCallback(async () => {
    setLoading(true);
    setError('');
    setActiveTab('compare');
    try {
      const response = await api.compare({
        variable_a: selectedVariable,
        variable_b: selectedVariable === 'temperature' ? 'precipitation' : 'temperature',
        region: selectedRegion,
        start_year: Number(startYear),
        end_year: Number(endYear),
      });
      if (response.status === 'success') {
        setCompareData(response);
      } else {
        setError('Comparison failed.');
        setCompareData(null);
      }
    } catch (err) {
      setError('Comparison service unavailable.');
      setCompareData(null);
    } finally {
      setLoading(false);
    }
  }, [selectedVariable, selectedRegion, startYear, endYear]);

  const handleExplain = useCallback(async () => {
    setLoading(true);
    try {
      const response = await api.explain({
        variable: analysis.variable || selectedVariable,
        region: analysis.region || selectedRegion,
        start_year: Number(startYear),
        end_year: Number(endYear),
        trend_value: analysis.trend || 0.038,
        p_value: analysis.p_value || 0.0008,
        total_change: analysis.total_change || 0.84,
        unit: analysis.unit || '°C/year',
      });
      if (response.status === 'success') {
        setExplanation(response);
      }
    } catch (err) {
      console.error('Explanation failed:', err);
    } finally {
      setLoading(false);
    }
  }, [analysis, selectedVariable, selectedRegion, startYear, endYear]);

  return (
    <AppShell>
      <Navigation 
        theme={theme} 
        onThemeToggle={() => setTheme((prev) => prev === 'light' ? 'dark' : 'light')} 
      />
      <Hero />

      <main className="mx-auto max-w-7xl px-4 pb-20 pt-8 sm:px-6 lg:px-8">
        {error && <ErrorBanner message={error} onDismiss={() => setError('')} />}

        <section className="grid gap-6 lg:grid-cols-[320px_minmax(0,1fr)]">
          <AnalysisPanel
            datasets={datasets}
            regions={regions}
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
            {loading && <LoadingSpinner />}

            <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
              <div className="mb-4 flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Trend result</p>
                  <h2 className="mt-1 text-xl font-medium text-[var(--text-primary)]">Analysis summary</h2>
                </div>
                <DataSourceBadge label={analysis.data_source || 'Demo dataset'} />
              </div>
              <TrendSummary analysis={analysis} />
            </div>

            <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
              <p className="mb-4 text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Statistics</p>
              <MetricsGrid analysis={analysis} />
            </div>

            <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
              <TrendChart 
                series={analysis.series || DEFAULT_ANALYSIS.series} 
                fittedSeries={analysis.fitted || DEFAULT_ANALYSIS.fitted} 
                unit={analysis.unit || '°C/year'} 
              />
            </div>
          </div>
        </section>

        <section className="mt-10 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
            <div className="mb-6 flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Trend Detective</p>
                <h3 className="mt-1 text-2xl font-medium text-[var(--text-primary)]">Discover patterns</h3>
              </div>
              <button 
                onClick={handleExplain} 
                disabled={loading}
                className="inline-flex items-center gap-2 rounded-full border border-[var(--border)] px-3 py-2 text-sm font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-secondary)] disabled:opacity-60"
              >
                Explain
              </button>
            </div>
            <TrendList 
              items={trendResults.length ? trendResults : [
                { variable: 'temperature', label: 'Temperature', direction: 'Increasing', trend: 0.038, unit: '°C/year', period: '2003–2025', p_value: 0.0008, statistically_significant: true },
                { variable: 'precipitation', label: 'Precipitation', direction: 'Mixed', trend: 0.4, unit: 'mm/month', period: '2003–2025', p_value: 0.04, statistically_significant: true },
                { variable: 'vegetation', label: 'Vegetation', direction: 'Increasing', trend: 0.003, unit: 'NDVI', period: '2003–2025', p_value: 0.02, statistically_significant: true },
              ]} 
            />
            {explanation && (
              <div className="mt-6 rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4">
                <p className="text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]">AI explanation</p>
                <p className="mt-3 text-sm leading-6 text-[var(--text-primary)]">{explanation.summary}</p>
                <ul className="mt-4 space-y-3 text-sm text-[var(--text-secondary)]">
                  {explanation.segments?.map((segment, idx) => (
                    <li key={idx} className="rounded-xl border border-[var(--border)] bg-white/30 p-3 dark:bg-slate-900/20">
                      <span className="font-medium capitalize text-[var(--text-primary)]">{segment.title}:</span> {segment.text}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          <div className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
            <ComparisonView compareData={compareData} />
          </div>
        </section>
      </main>
    </AppShell>
  );
}

export default App;
