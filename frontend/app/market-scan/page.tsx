'use client'

import { useCallback, useState } from 'react'
import ScanForm from '@/components/ScanForm'
import JobProgress from '@/components/JobProgress'
import PdfDownloadButton from '@/components/PdfDownloadButton'
import MarketScanReportView from '@/components/reports/MarketScanReport'
import { useJobPoller } from '@/hooks/useJobPoller'
import { startMarketScan, getMarketScan, marketScanPdfUrl } from '@/lib/api'
import type { ScanRequest } from '@/lib/types'

export default function MarketScanPage() {
  const [jobId, setJobId] = useState<string | null>(null)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const fetchFn = useCallback((id: string) => getMarketScan(id), [])
  const { job, fetchError } = useJobPoller(jobId, fetchFn)

  async function handleSubmit(req: ScanRequest) {
    setSubmitError(null)
    setLoading(true)
    try {
      const j = await startMarketScan(req)
      setJobId(j.job_id)
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : 'Failed to start scan')
    } finally {
      setLoading(false)
    }
  }

  const isRunning = job && job.status !== 'complete' && job.status !== 'error'
  const isComplete = job?.status === 'complete'
  const isError = job?.status === 'error'

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Page header */}
      <div>
        <h1 className="font-display text-2xl font-bold text-navy-900">Market Scan</h1>
        <p className="text-warm-500 text-sm mt-1">
          Full market intelligence report covering sizing, structure, competitive landscape, customers, tech trends, and strategy.
        </p>
      </div>

      {/* Form (collapse when running or complete) */}
      {!isRunning && !isComplete && (
        <div className="bg-white border border-blush-200 rounded-xl p-6">
          <ScanForm
            onSubmit={handleSubmit}
            loading={loading}
            submitLabel="Run Market Scan"
          />
          {submitError && (
            <p className="text-red-600 text-sm mt-3">{submitError}</p>
          )}
        </div>
      )}

      {/* Reset button when done */}
      {(isComplete || isError) && (
        <button
          onClick={() => { setJobId(null); setSubmitError(null) }}
          className="text-sm text-brand-600 hover:underline"
        >
          ← Run another scan
        </button>
      )}

      {/* Progress */}
      {job && (isRunning || isError) && (
        <JobProgress
          message={job.progress_message}
          pct={job.progress_pct}
          status={job.status}
        />
      )}

      {/* Error */}
      {(isError || fetchError) && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-5">
          <p className="text-red-700 text-sm font-medium">
            {job?.error || fetchError || 'An error occurred.'}
          </p>
        </div>
      )}

      {/* Report */}
      {isComplete && job.report && (
        <>
          <div className="flex items-center justify-between">
            <p className="text-sm text-green-600 font-medium">Report complete</p>
            <PdfDownloadButton href={marketScanPdfUrl(jobId!)} label="Download PDF Report" />
          </div>
          <MarketScanReportView r={job.report} />
        </>
      )}
    </div>
  )
}
