import React, { useEffect, useMemo, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const REGION_BOUNDS = {
  global: [[-60, -180], [75, 180]],
  north_america: [[10, -168], [72, -52]],
  south_america: [[-56, -82], [13, -34]],
  africa: [[-35, -18], [38, 55]],
  asia: [[-10, 25], [80, 180]],
  australia: [[-45, 112], [-10, 154]],
  arctic: [[60, -180], [90, 180]],
};

export function MapView({ region = 'global', analysis }) {
  const mapNode = useRef(null);
  const mapRef = useRef(null);
  const layerRef = useRef(null);
  const bounds = useMemo(() => REGION_BOUNDS[region] || REGION_BOUNDS.global, [region]);

  useEffect(() => {
    if (!mapNode.current || mapRef.current) return undefined;
    const map = L.map(mapNode.current, { zoomControl: false, attributionControl: true });
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 8,
    }).addTo(map);
    mapRef.current = map;
    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!mapRef.current) return;
    const map = mapRef.current;
    map.fitBounds(bounds, { padding: [18, 18], animate: false });
    if (layerRef.current) layerRef.current.remove();
    const significant = analysis?.statistically_significant;
    const slope = Number(analysis?.trend || 0);
    const fillColor = significant ? (slope >= 0 ? '#238b45' : '#d7301f') : '#9ca3af';
    layerRef.current = L.rectangle(bounds, {
      color: fillColor,
      weight: 2,
      fillColor,
      fillOpacity: 0.18,
    }).bindPopup(`${analysis?.dataset_name || 'Selected variable'}: ${analysis?.trend_direction || 'trend'}${significant ? ' (p < 0.05)' : ' (not significant)'}`).addTo(map);
  }, [bounds, analysis]);

  return (
    <div className="overflow-hidden rounded-[24px] border border-[var(--border)]">
      <div ref={mapNode} className="earth-map" aria-label="Interactive Earth map" role="application" />
      <div className="flex flex-wrap items-center gap-4 border-t border-[var(--border)] bg-[var(--surface-secondary)] px-4 py-3 text-xs text-[var(--text-secondary)]">
        <span><i className="legend-dot increasing" /> Increasing</span>
        <span><i className="legend-dot decreasing" /> Decreasing</span>
        <span><i className="legend-dot neutral" /> Not significant</span>
        <span className="ml-auto">Illustrative regional layer · units: {analysis?.unit || 'selected variable'}</span>
      </div>
    </div>
  );
}
