import React, { useEffect, useState, useCallback } from 'react';
import { AppShell } from './components/AppShell.jsx';
import { Navigation } from './components/Navigation.jsx';
import { Hero } from './components/Hero.jsx';
import { AnalysisPanel } from './components/AnalysisPanel.jsx';
import { MapPanel } from './components/MapPanel.jsx';
import { TrendSummary } from './components/TrendSummary.jsx';
import { TrendChart } from './components/TrendChart.jsx';
import { MetricsGrid } from './components/MetricsGrid.jsx';
import { TrendList } from './components/TrendList.jsx';
import { ComparisonView } from './components/ComparisonView.jsx';
import { DataSourceBadge } from './components/DataSourceBadge.jsx';
import { LoadingSpinner } from './components/LoadingSpinner.jsx';
import { ErrorBanner } from './components/ErrorBanner.jsx';
import { AuthScreen } from './components/AuthScreen.jsx';
import { api } from './services/api.js';
import './App.css';

const DEFAULT_SERIES = Array.from({ length: 23 }, (_, i) => ({ year: 2003 + i, value: 12.5 + i * 0.02 }));
const DEFAULT_FITTED = Array.from({ length: 23 }, (_, i) => ({ year: 2003 + i, value: 12.5 + i * 0.018 }));
const DEFAULT_ANALYSIS = {
  variable: 'temperature', region: 'global', period: '2003-2025', trend: 0.038, unit: '°C/year',
  total_change: 0.84, p_value: 0.0008, confidence_interval: [0.025, 0.051], r_squared: 0.72,
  statistically_significant: true, dataset_name: 'Temperature', data_source: 'Demo dataset (development only)',
  is_demo: true, series: DEFAULT_SERIES, fitted: DEFAULT_FITTED, trend_direction: 'increasing', status: 'success',
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
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('earthlens_token') || '');
  const [currentUser, setCurrentUser] = useState(null);
  const [authMode, setAuthMode] = useState('signin');
  const [authForm, setAuthForm] = useState({ name: '', email: '', password: '' });
  const [authError, setAuthError] = useState('');

  useEffect(() => { document.documentElement.dataset.theme = theme; }, [theme]);

  useEffect(() => {
    if (!authToken) {
      setCurrentUser(null);
      return;
    }

    api.getCurrentUser(authToken)
      .then((response) => {
        if (response.status === 'success') {
          setCurrentUser(response.user);
        } else {
          localStorage.removeItem('earthlens_token');
          setAuthToken('');
          setCurrentUser(null);
        }
      })
      .catch(() => {
        localStorage.removeItem('earthlens_token');
        setAuthToken('');
        setCurrentUser(null);
      });
  }, [authToken]);

  useEffect(() => {
    if (!currentUser) return;
    Promise.all([api.getDatasets(authToken), api.getRegions(authToken)])
      .then(([d, r]) => {
        setDatasets(d.datasets || []);
        setRegions(Object.values(r.regions || {}));
      })
      .catch(() => setError('Metadata service is unavailable.'));
  }, [currentUser, authToken]);

  const request = { region: selectedRegion, start_year: Number(startYear), end_year: Number(endYear) };

  const handleAuthSubmit = useCallback(async (event) => {
    event.preventDefault();
    setAuthError('');

    try {
      const response = authMode === 'signup'
        ? await api.signup({ ...authForm, name: authForm.name || 'EarthLens User' }, authToken)
        : await api.signin({ email: authForm.email, password: authForm.password }, authToken);

      if (response.status === 'success') {
        localStorage.setItem('earthlens_token', response.token);
        setAuthToken(response.token);
        setCurrentUser(response.user);
      } else {
        setAuthError(response.message || 'Authentication failed.');
      }
    } catch (err) {
      setAuthError('Authentication could not be completed. Please try again.');
    }
  }, [authMode, authForm, authToken]);

  const handleSignOut = useCallback(() => {
    localStorage.removeItem('earthlens_token');
    setAuthToken('');
    setCurrentUser(null);
    setAuthForm({ name: '', email: '', password: '' });
  }, []);

  const handleAnalyze = useCallback(async () => {
    if (!authToken) {
      setError('Please sign in to analyze EarthLens data.');
      return;
    }
    setLoading(true); setError('');
    const response = await api.analyze({ ...request, variable: selectedVariable }, authToken);
    if (response.status === 'success') setAnalysis(response); else setError(response.message || 'Unable to analyze trend.');
    setLoading(false);
  }, [selectedVariable, selectedRegion, startYear, endYear, authToken]);

  const handleTrendDetect = useCallback(async () => {
    if (!authToken) {
      setError('Please sign in to search for trends.');
      return;
    }
    setLoading(true); setError('');
    const response = await api.detectTrends(request, authToken);
    if (response.status === 'success') setTrendResults(response.results || []); else setError(response.message || 'Trend detection failed.');
    setLoading(false);
  }, [selectedRegion, startYear, endYear, authToken]);

  const handleCompare = useCallback(async () => {
    if (!authToken) {
      setError('Please sign in to compare variables.');
      return;
    }
    setLoading(true); setError('');
    const variableB = selectedVariable === 'temperature' ? 'precipitation' : 'temperature';
    const response = await api.compare({ ...request, variable_a: selectedVariable, variable_b: variableB }, authToken);
    if (response.status === 'success') setCompareData(response); else setError(response.message || 'Comparison failed.');
    setLoading(false);
  }, [selectedVariable, selectedRegion, startYear, endYear, authToken]);

  const handleExplain = useCallback(async () => {
    if (!authToken) {
      setError('Please sign in to request an explanation.');
      return;
    }
    setLoading(true);
    const response = await api.explain({
      ...request,
      variable: analysis.variable || selectedVariable,
      trend_value: analysis.trend,
      p_value: analysis.p_value,
      total_change: analysis.total_change,
      unit: analysis.unit,
    }, authToken);
    if (response.status === 'success') setExplanation(response); else setError(response.message || 'Explanation unavailable.');
    setLoading(false);
  }, [analysis, selectedVariable, selectedRegion, startYear, endYear, authToken]);

  if (!currentUser) {
    return (
      <AuthScreen
        authMode={authMode}
        setAuthMode={setAuthMode}
        authForm={authForm}
        setAuthForm={setAuthForm}
        authError={authError}
        onSubmit={handleAuthSubmit}
      />
    );
  }

  return (
    <AppShell>
      <Navigation
        theme={theme}
        onThemeToggle={() => setTheme((v) => v === 'light' ? 'dark' : 'light')}
        user={currentUser}
        onSignOut={handleSignOut}
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
            <MapPanel region={selectedRegion} analysis={analysis} />
            <section className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
              <div className="mb-4 flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Trend result</p>
                  <h2 className="mt-1 text-2xl font-medium text-[var(--text-primary)]">Environmental change</h2>
                </div>
                <button
                  onClick={handleExplain}
                  className="rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-4 py-2 text-xs font-medium text-[var(--text-primary)] transition hover:bg-[var(--surface-primary)]"
                >
                  Explain this result
                </button>
              </div>
              <TrendSummary analysis={analysis} />
              <div className="mt-6">
                <MetricsGrid analysis={analysis} />
              </div>
              <div className="mt-6">
                <DataSourceBadge analysis={analysis} />
              </div>
            </section>
            <section className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
              <TrendChart series={analysis.series || DEFAULT_SERIES} fittedSeries={analysis.fitted || DEFAULT_FITTED} unit={analysis.unit || '°C/year'} />
            </section>
          </div>
        </section>
        <section id="trends" className="mt-10 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <section className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Trend detective</p>
                <h3 className="mt-1 text-2xl font-medium text-[var(--text-primary)]">Find interesting trends</h3>
              </div>
            </div>
            <TrendList items={trendResults} />
            {explanation && (
              <div className="mt-6 rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] p-4">
                <div className="mb-3 text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]">AI explanation</div>
                <p className="text-sm leading-6 text-[var(--text-primary)]">{explanation.summary}</p>
                <div className="mt-4 space-y-3">
                  {explanation.segments?.map((segment) => (
                    <div key={segment.type} className="rounded-2xl border border-[var(--border)] bg-[var(--surface-primary)] p-3">
                      <div className="text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]">{segment.title}</div>
                      <p className="mt-2 text-sm leading-6 text-[var(--text-primary)]">{segment.text}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
          <section className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
            <ComparisonView compareData={compareData} />
          </section>
        </section>
      </main>
    </AppShell>
  );
}

export default App;
