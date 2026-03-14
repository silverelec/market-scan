'use client'

import { useState } from 'react'
import type { ScanRequest } from '@/lib/types'

interface Props {
  onSubmit: (req: ScanRequest) => void
  loading: boolean
  showCompetitors?: boolean
  submitLabel?: string
}

export default function ScanForm({
  onSubmit,
  loading,
  showCompetitors = false,
  submitLabel = 'Run Analysis',
}: Props) {
  const [company, setCompany] = useState('')
  const [market, setMarket] = useState('')
  const [months, setMonths] = useState(24)
  const [competitorsRaw, setCompetitorsRaw] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const req: ScanRequest = {
      company: company.trim(),
      market: market.trim(),
      time_period_months: months,
    }
    if (showCompetitors && competitorsRaw.trim()) {
      req.additional_competitors = competitorsRaw
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean)
    }
    onSubmit(req)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Client Company <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            required
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder="e.g. Acme Corp"
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Market / Industry <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            required
            value={market}
            onChange={(e) => setMarket(e.target.value)}
            placeholder="e.g. Global Electric Vehicle Market"
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
          />
        </div>
      </div>

      <div className={showCompetitors ? 'grid grid-cols-1 sm:grid-cols-2 gap-4' : ''}>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Research Horizon
          </label>
          <div className="flex items-center gap-3">
            <input
              type="range"
              min={3}
              max={60}
              step={3}
              value={months}
              onChange={(e) => setMonths(Number(e.target.value))}
              className="flex-1 accent-brand-600"
            />
            <span className="text-sm font-semibold text-slate-700 w-20">
              {months} months
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            How far back to pull data ({Math.round(months / 12 * 10) / 10} years)
          </p>
        </div>

        {showCompetitors && (
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Specific Competitors{' '}
              <span className="text-slate-400 font-normal">(optional)</span>
            </label>
            <input
              type="text"
              value={competitorsRaw}
              onChange={(e) => setCompetitorsRaw(e.target.value)}
              placeholder="Tesla, BYD, Rivian (comma-separated)"
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
            />
            <p className="text-xs text-slate-400 mt-1">
              Leave blank to auto-identify top competitors
            </p>
          </div>
        )}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full sm:w-auto bg-brand-600 hover:bg-brand-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold px-6 py-2.5 rounded-lg text-sm transition-colors"
      >
        {loading ? 'Running…' : submitLabel}
      </button>
    </form>
  )
}
