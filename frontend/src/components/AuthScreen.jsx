import React, { useState } from 'react';

export function AuthScreen({ authMode, setAuthMode, authForm, setAuthForm, authError, onSubmit }) {
  const isSignup = authMode === 'signup';

  return (
    <div className="min-h-screen bg-[var(--bg)] text-[var(--text-primary)]">
      <div className="mx-auto flex min-h-screen max-w-6xl items-center justify-center px-4 py-10">
        <div className="grid w-full max-w-5xl overflow-hidden rounded-[32px] border border-[var(--border)] bg-[var(--surface-primary)] shadow-soft lg:grid-cols-[1.1fr_0.9fr]">
          <div className="hidden bg-[radial-gradient(circle_at_top,_rgba(110,168,254,0.14),_transparent_55%)] p-10 lg:flex lg:flex-col lg:justify-between">
            <div>
              <div className="text-xs uppercase tracking-[0.3em] text-[var(--text-secondary)]">EarthLens</div>
              <h1 className="mt-6 max-w-md text-4xl font-semibold tracking-[-0.08em] text-[var(--text-primary)]">
                Discover how Earth’s environmental systems are changing.
              </h1>
            </div>
            <div className="space-y-4 text-sm leading-6 text-[var(--text-secondary)]">
              <p>Explore NASA Earth-observation data with transparent trend analysis.</p>
              <p>Investigate environmental changes with statistical evidence and clear uncertainty.</p>
            </div>
          </div>

          <div className="p-6 sm:p-8">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <div className="text-xs uppercase tracking-[0.2em] text-[var(--text-secondary)]">Access</div>
                <h2 className="mt-2 text-3xl font-semibold tracking-[-0.06em] text-[var(--text-primary)]">
                  {isSignup ? 'Create an account' : 'Welcome back'}
                </h2>
              </div>
              <button
                type="button"
                className="rounded-full border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-2 text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]"
                onClick={() => setAuthMode(isSignup ? 'signin' : 'signup')}
              >
                {isSignup ? 'Sign in' : 'Sign up'}
              </button>
            </div>

            <form className="space-y-4" onSubmit={onSubmit}>
              {isSignup && (
                <div>
                  <label className="mb-2 block text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]">Name</label>
                  <input
                    value={authForm.name}
                    onChange={(e) => setAuthForm((prev) => ({ ...prev, name: e.target.value }))}
                    className="w-full rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)]"
                    placeholder="Your name"
                    autoComplete="name"
                  />
                </div>
              )}

              <div>
                <label className="mb-2 block text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]">Email</label>
                <input
                  type="email"
                  value={authForm.email}
                  onChange={(e) => setAuthForm((prev) => ({ ...prev, email: e.target.value }))}
                  className="w-full rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)]"
                  placeholder="name@example.com"
                  autoComplete="email"
                  required
                />
              </div>

              <div>
                <label className="mb-2 block text-xs uppercase tracking-[0.18em] text-[var(--text-secondary)]">Password</label>
                <input
                  type="password"
                  value={authForm.password}
                  onChange={(e) => setAuthForm((prev) => ({ ...prev, password: e.target.value }))}
                  className="w-full rounded-2xl border border-[var(--border)] bg-[var(--surface-secondary)] px-3 py-3 text-sm text-[var(--text-primary)] outline-none focus:ring-2 focus:ring-[var(--accent)]"
                  placeholder="Enter password"
                  autoComplete={isSignup ? 'new-password' : 'current-password'}
                  required
                />
              </div>

              {authError && (
                <div className="rounded-2xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                  {authError}
                </div>
              )}

              <button
                type="submit"
                className="w-full rounded-full bg-[var(--accent)] px-4 py-3 text-sm font-medium text-slate-950 transition hover:brightness-95"
              >
                {isSignup ? 'Create account' : 'Sign in'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
