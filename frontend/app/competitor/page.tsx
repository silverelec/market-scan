'use client'

import { useCallback, useState } from 'react'
import ScanForm from '@/components/ScanForm'
import JobProgress from '@/components/JobProgress'
import PdfDownloadButton from '@/components/PdfDownloadButton'
import CompetitorReportView from '@/components/reports/CompetitorReport'
import { useJobPoller } from '@/hooks/useJobPoller'
import { startCompetitorAnalysis, getCompetitorAnalysis, competitorPdfUrl } from '@/lib/api'
import type { ScanRequest } from '@/lib/types'

export default function CompetitorPage() {
  const [jobId, setJobId] = useState<string | null>(null)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const fetchFn = useCallback((id: string) => getCompetitorAnalysis(id), [])
  const { job, fetchError } = useJobPoller(jobId, fetchFn)

  async function handleSubmit(req: ScanRequest) {
    setSubmitError(null)
    setLoading(true)
    try {
      const j = await startCompetitorAnalysis(req)
      setJobId(j.job_id)
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : 'Failed to start analysis')
    } finally {
      setLoading(false)
    }
  }

  const isRunning = job && job.status !== 'complete' && job.status !== 'error'
  const isComplete = job?.status === 'complete'
  const isError = job?.status === 'error'

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div>
        <h1 className="font-display text-2xl font-bold text-navy-900">Competitor Analysis</h1>
        <p className="text-warm-500 text-sm mt-1">
          Deep-dive profiles, benchmarking matrices, white-space mapping, and strategic recommendations across every key competitor.
        </p>
      </div>

      {!isRunning && !isComplete && (
        <div className="bg-white border border-blush-200 rounded-xl p-6">
          <ScanForm
            onSubmit={handleSubmit}
            loading={loading}
            showCompetitors
            submitLabel="Start Competitor Analysis"
          />
          {submitError && (
            <p className="text-red-600 text-sm mt-3">{submitError}</p>
          )}
        </div>
      )}

      {(isComplete || isError) && (
        <button
          onClick={() => { setJobId(null); setSubmitError(null) }}
          className="text-sm text-brand-600 hover:underline"
        >
          ← Run another analysis
        </button>
      )}

      {job && (isRunning || isError) && (
        <JobProgress
          message={job.progress_message}
          pct={job.progress_pct}
          status={job.status}
        />
      )}

      {(isError || fetchError) && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-5">
          <p className="text-red-700 text-sm font-medium">
            {job?.error || fetchError || 'An error occurred.'}
          </p>
        </div>
      )}

      {isComplete && job.report && (
        <>
          <div className="flex items-center justify-between">
            <p className="text-sm text-green-600 font-medium">Analysis complete</p>
            <PdfDownloadButton href={competitorPdfUrl(jobId!)} label="Download PDF Report" />
          </div>
          <CompetitorReportView r={job.report} />
        </>
      )}
    </div>
  )
}
