// Small shared UI primitives used across report components

export function SectionCard({
  title,
  children,
  icon,
}: {
  title: string
  children: React.ReactNode
  icon?: string
}) {
  return (
    <div className="section-card">
      <div className="section-header flex items-center gap-2">
        {icon && <span className="text-base">{icon}</span>}
        <h2 className="section-title">{title}</h2>
      </div>
      <div className="section-body">{children}</div>
    </div>
  )
}

export function BulletList({ items }: { items: string[] }) {
  if (!items?.length) return <Empty />
  return (
    <ul className="bullet-list">
      {items.map((item, i) => (
        <li key={i}>{item}</li>
      ))}
    </ul>
  )
}

export function Empty() {
  return <p className="text-sm text-slate-400 italic">No data available.</p>
}

type BadgeLevel = 'High' | 'Medium' | 'Low' | string

const badgeClasses: Record<string, string> = {
  High: 'bg-red-100 text-red-700',
  Medium: 'bg-amber-100 text-amber-700',
  Low: 'bg-green-100 text-green-700',
  Strong: 'bg-green-100 text-green-700',
  Weak: 'bg-red-100 text-red-700',
  Leader: 'bg-indigo-100 text-indigo-700',
  Challenger: 'bg-blue-100 text-blue-700',
  Niche: 'bg-slate-100 text-slate-600',
  Disruptor: 'bg-purple-100 text-purple-700',
  Positive: 'bg-green-100 text-green-700',
  Neutral: 'bg-slate-100 text-slate-600',
  Negative: 'bg-red-100 text-red-700',
  Emerging: 'bg-purple-100 text-purple-700',
  Scaling: 'bg-blue-100 text-blue-700',
  Mainstream: 'bg-green-100 text-green-700',
  Present: 'bg-green-100 text-green-700',
  Partial: 'bg-amber-100 text-amber-700',
  Absent: 'bg-slate-100 text-slate-500',
  Premium: 'bg-indigo-100 text-indigo-700',
  'Mid-market': 'bg-blue-100 text-blue-700',
  Value: 'bg-green-100 text-green-700',
}

export function Badge({ value }: { value: BadgeLevel }) {
  if (!value) return null
  const cls = badgeClasses[value] ?? 'bg-slate-100 text-slate-600'
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${cls}`}>
      {value}
    </span>
  )
}

export function fmt(v: number | null | undefined, suffix = ''): string {
  if (v == null) return '—'
  return `${v}${suffix}`
}

export function fmtUsd(v: number | null | undefined): string {
  if (v == null) return '—'
  return `$${v}B`
}
