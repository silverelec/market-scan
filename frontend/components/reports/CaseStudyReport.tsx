import type { CaseStudyReport, CaseStudy } from '@/lib/types'
import { SectionCard, BulletList, Badge, Empty } from '@/components/ui'

export default function CaseStudyReportView({ r }: { r: CaseStudyReport }) {
  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div className="bg-slate-900 text-white rounded-xl p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-slate-400 text-xs uppercase tracking-widest mb-1">Innovation Case Studies</p>
            <h1 className="text-2xl font-bold">{r.market}</h1>
            <p className="text-slate-300 mt-1 text-sm">Client: {r.company}</p>
          </div>
          <div className="text-right text-sm text-slate-400 space-y-1">
            <p>Research horizon: {r.time_period_months} months</p>
            <p>Generated: {new Date(r.generated_at).toLocaleDateString()}</p>
          </div>
        </div>
        {r.report_narrative && (
          <p className="text-slate-300 mt-4 text-sm leading-relaxed max-w-3xl">{r.report_narrative}</p>
        )}
        {r.case_studies?.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {r.case_studies.map((cs, i) => (
              <span key={i} className="bg-slate-700 text-slate-200 text-xs px-2.5 py-1 rounded-full">
                #{cs.number} {cs.title}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* ── Case Studies ── */}
      {r.case_studies?.length > 0 ? (
        <div className="space-y-6">
          {r.case_studies.map((cs, i) => (
            <CaseStudyCard key={i} cs={cs} />
          ))}
        </div>
      ) : (
        <SectionCard title="Case Studies" icon="📖">
          <Empty />
        </SectionCard>
      )}

      {/* ── Sources ── */}
      {r.all_sources?.length > 0 && (
        <SectionCard title="Sources" icon="📚">
          <div className="space-y-1 max-h-60 overflow-y-auto pr-1">
            {r.all_sources.map((s, i) => {
              const src = s as Record<string, unknown>
              return (
                <div key={i} className="text-xs text-slate-500 flex items-start gap-2">
                  <span className="flex-shrink-0 text-slate-300">{i + 1}.</span>
                  {src.url ? (
                    <a
                      href={String(src.url)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-brand-600 hover:underline truncate"
                    >
                      {String(src.title || src.url)}
                    </a>
                  ) : (
                    <span>{JSON.stringify(s)}</span>
                  )}
                </div>
              )
            })}
          </div>
        </SectionCard>
      )}
    </div>
  )
}

function CaseStudyCard({ cs }: { cs: CaseStudy }) {
  const typeColors: Record<string, string> = {
    Technology: 'bg-blue-100 text-blue-700',
    'Business Model': 'bg-indigo-100 text-indigo-700',
    Operations: 'bg-amber-100 text-amber-700',
    Customer: 'bg-green-100 text-green-700',
    ESG: 'bg-teal-100 text-teal-700',
  }
  const typeClass = typeColors[cs.innovation_type] ?? 'bg-slate-100 text-slate-600'

  return (
    <div className="section-card">
      {/* Card Header */}
      <div className="section-header">
        <div className="flex flex-wrap items-center gap-3">
          <span className="bg-slate-900 text-white text-xs font-bold w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0">
            {cs.number}
          </span>
          <h2 className="font-semibold text-slate-800 text-base">{cs.title}</h2>
          <div className="flex gap-2 ml-auto">
            {cs.innovation_type && (
              <span className={`text-xs font-medium px-2.5 py-0.5 rounded-full ${typeClass}`}>
                {cs.innovation_type}
              </span>
            )}
            {cs.maturity_level && <Badge value={cs.maturity_level} />}
          </div>
        </div>
      </div>

      <div className="section-body space-y-5">
        {/* Innovation Overview */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {cs.innovation_description && (
            <div className="sm:col-span-2">
              <h3 className="text-xs font-semibold text-slate-400 uppercase mb-1">What It Is</h3>
              <p className="text-slate-700 text-sm leading-relaxed">{cs.innovation_description}</p>
            </div>
          )}
          {cs.problem_solved && (
            <div>
              <h3 className="text-xs font-semibold text-slate-400 uppercase mb-1">Problem Solved</h3>
              <p className="text-slate-600 text-sm">{cs.problem_solved}</p>
            </div>
          )}
        </div>

        {/* Example in Practice */}
        {(cs.lead_company || cs.implementation_description || cs.metrics_outcomes?.length > 0) && (
          <div className="bg-slate-50 border border-slate-100 rounded-lg p-4">
            <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Example in Practice</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                {cs.lead_company && (
                  <p className="font-semibold text-slate-800 text-sm mb-2">
                    Lead: <span className="text-brand-600">{cs.lead_company}</span>
                  </p>
                )}
                {cs.implementation_description && (
                  <p className="text-slate-600 text-sm leading-relaxed">{cs.implementation_description}</p>
                )}
              </div>
              {cs.metrics_outcomes?.length > 0 && (
                <div>
                  <h4 className="text-xs font-semibold text-green-600 uppercase mb-2">Outcomes & Metrics</h4>
                  <BulletList items={cs.metrics_outcomes} />
                </div>
              )}
            </div>
          </div>
        )}

        {/* Impact */}
        {(cs.customer_impact || cs.business_performance_impact || cs.competitive_dynamics_impact) && (
          <div>
            <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Impact on the Industry</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {cs.customer_impact && (
                <ImpactBox label="Customer Impact" text={cs.customer_impact} />
              )}
              {cs.business_performance_impact && (
                <ImpactBox label="Business Performance" text={cs.business_performance_impact} />
              )}
              {cs.competitive_dynamics_impact && (
                <ImpactBox label="Competitive Dynamics" text={cs.competitive_dynamics_impact} />
              )}
            </div>
          </div>
        )}

        {/* Takeaways + Relevance */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {cs.key_takeaways?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Key Takeaways</h3>
              <BulletList items={cs.key_takeaways} />
            </div>
          )}
          {(cs.client_relevance || cs.potential_opportunity) && (
            <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-4">
              <h3 className="text-xs font-semibold text-indigo-600 uppercase mb-2">Relevance for {'{Client}'}</h3>
              {cs.client_relevance && (
                <p className="text-sm text-slate-700 leading-relaxed">{cs.client_relevance}</p>
              )}
              {cs.potential_opportunity && (
                <div className="mt-2">
                  <p className="text-xs font-semibold text-indigo-500 mb-1">Opportunity</p>
                  <p className="text-sm text-slate-600">{cs.potential_opportunity}</p>
                </div>
              )}
            </div>
          )}
        </div>

        {cs.where_emerging && (
          <p className="text-xs text-slate-400">
            <span className="font-medium">Where emerging:</span> {cs.where_emerging}
          </p>
        )}
      </div>
    </div>
  )
}

function ImpactBox({ label, text }: { label: string; text: string }) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-3">
      <h4 className="text-xs font-semibold text-slate-400 uppercase mb-1">{label}</h4>
      <p className="text-sm text-slate-700">{text}</p>
    </div>
  )
}
