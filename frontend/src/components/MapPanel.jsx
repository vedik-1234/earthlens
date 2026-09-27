import React from 'react';
import { MapView } from './MapView.jsx';

export function MapPanel({ region, analysis }) {
  return (
    <section className="rounded-[28px] border border-[var(--border)] bg-[var(--surface-primary)] p-4 shadow-soft sm:p-6">
      <div className="mb-4 flex items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Spatial view</p>
          <h2 className="mt-1 text-xl font-medium text-[var(--text-primary)]">Where is it changing?</h2>
        </div>
        <span className="rounded-full border border-[var(--border)] px-3 py-1 text-xs capitalize text-[var(--text-secondary)]">{region.replace('_', ' ')}</span>
      </div>
      <MapView region={region} analysis={analysis} />
      <p className="mt-3 text-xs leading-5 text-[var(--text-secondary)]">The first release displays the selected regional extent and trend classification. Raster-cell trend maps will be enabled when a NASA gridded provider is configured.</p>
    </section>
  );
}
