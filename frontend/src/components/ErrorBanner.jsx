export function ErrorBanner({ message, onDismiss }) {
  return (
    <div className="mb-6 rounded-2xl border border-rose-200 bg-rose-50/80 px-4 py-3 text-sm text-rose-700 dark:border-rose-900/40 dark:bg-rose-950/40 dark:text-rose-300 flex items-center justify-between">
      <span>⚠️ {message}</span>
      <button
        onClick={onDismiss}
        className="ml-4 text-rose-600 hover:text-rose-800 dark:text-rose-400 dark:hover:text-rose-300 font-medium"
      >
        Dismiss
      </button>
    </div>
  );
}
