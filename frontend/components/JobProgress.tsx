interface Props {
  message: string
  pct: number
  status: string
}

const statusColors: Record<string, string> = {
  queued: 'bg-slate-400',
  researching: 'bg-blue-500',
  identifying: 'bg-purple-500',
  synthesizing: 'bg-amber-500',
  complete: 'bg-green-500',
  error: 'bg-red-500',
}

export default function JobProgress({ message, pct, status }: Props) {
  const barColor = statusColors[status] ?? 'bg-brand-500'

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 space-y-3">
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-slate-700">{message}</span>
        <span className="text-slate-500 font-semibold">{pct}%</span>
      </div>
      <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
        <div
          className={`${barColor} h-2 rounded-full transition-all duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
      {status !== 'complete' && status !== 'error' && (
        <p className="text-xs text-slate-400 animate-pulse">
          This typically takes 1–3 minutes…
        </p>
      )}
    </div>
  )
}
