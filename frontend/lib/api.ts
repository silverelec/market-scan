import type {
  ScanRequest,
  MarketScanJob,
  CompetitorJob,
  CaseStudyJob,
} from './types'

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json()
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: 'no-store' })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json()
}

// ── Market Scan ───────────────────────────────────────────────────────────────

export function startMarketScan(req: ScanRequest): Promise<MarketScanJob> {
  return post('/api/market-scan', req)
}

export function getMarketScan(jobId: string): Promise<MarketScanJob> {
  return get(`/api/market-scan/${jobId}`)
}

export function marketScanPdfUrl(jobId: string): string {
  return `${BASE}/api/market-scan/${jobId}/pdf`
}

// ── Competitor Analysis ───────────────────────────────────────────────────────

export function startCompetitorAnalysis(req: ScanRequest): Promise<CompetitorJob> {
  return post('/api/competitor', req)
}

export function getCompetitorAnalysis(jobId: string): Promise<CompetitorJob> {
  return get(`/api/competitor/${jobId}`)
}

export function competitorPdfUrl(jobId: string): string {
  return `${BASE}/api/competitor/${jobId}/pdf`
}

// ── Case Studies ──────────────────────────────────────────────────────────────

export function startCaseStudy(req: ScanRequest): Promise<CaseStudyJob> {
  return post('/api/case-study', req)
}

export function getCaseStudy(jobId: string): Promise<CaseStudyJob> {
  return get(`/api/case-study/${jobId}`)
}

export function caseStudyPdfUrl(jobId: string): string {
  return `${BASE}/api/case-study/${jobId}/pdf`
}
