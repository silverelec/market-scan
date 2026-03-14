'use client'

import { useEffect, useRef, useState } from 'react'

type AnyJob = {
  status: string
  progress_pct: number
  progress_message: string
  error: string | null
}

export function useJobPoller<T extends AnyJob>(
  jobId: string | null,
  fetchFn: (id: string) => Promise<T>,
  intervalMs = 2500,
) {
  const [job, setJob] = useState<T | null>(null)
  const [fetchError, setFetchError] = useState<string | null>(null)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    if (!jobId) return

    const poll = async () => {
      try {
        const data = await fetchFn(jobId)
        setJob(data)
        if (data.status === 'complete' || data.status === 'error') {
          if (intervalRef.current) clearInterval(intervalRef.current)
        }
      } catch (e) {
        setFetchError(e instanceof Error ? e.message : 'Polling failed')
        if (intervalRef.current) clearInterval(intervalRef.current)
      }
    }

    poll() // immediate first poll
    intervalRef.current = setInterval(poll, intervalMs)

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [jobId, fetchFn, intervalMs])

  return { job, fetchError }
}
