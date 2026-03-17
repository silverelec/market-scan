import type { CompetitorReport, CompetitorProfile } from '@/lib/types'
import { SectionCard, BulletList, Badge, Empty, fmtUsd } from '@/components/ui'

export default function CompetitorReportView({ r }: { r: CompetitorReport }) {
  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div className="bg-slate-900 text-white rounded-xl p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-slate-400 text-xs uppercase tracking-widest mb-1">Competitor Analysis</p>
            <h1 className="text-2xl font-bold">{r.market}</h1>
            <p className="text-slate-300 mt-1 text-sm">Client: {r.company}</p>
          </div>
          <div className="text-right text-sm text-slate-400 space-y-1">
            <p>Research horizon: {r.time_period_months} months</p>
            <p>Generated: {new Date(r.generated_at).toLocaleDateString()}</p>
          </div>
        </div>
        {r.identified_competitors?.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {r.identified_competitors.map((c, i) => (
              <span key={i} className="bg-slate-700 text-slate-200 text-xs px-2.5 py-1 rounded-full">
                {c}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* ── Executive Summary ── */}
      {(r.purpose || r.key_findings?.length > 0 || r.strategic_implications?.length > 0) && (
      <SectionCard title="Executive Summary" icon="📋">
        <div className="space-y-4">
          {r.purpose && <p className="text-slate-700 text-sm leading-relaxed">{r.purpose}</p>}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {r.key_findings?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Key Findings</h3>
                <BulletList items={r.key_findings} />
              </div>
            )}
            {r.strategic_implications?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Strategic Implications</h3>
                <BulletList items={r.strategic_implications} />
              </div>
            )}
          </div>
        </div>
      </SectionCard>
      )}

      {/* ── Market Overview ── */}
      {(r.industry_overview || r.competitive_landscape_overview) && (
      <SectionCard title="Market Overview" icon="🗺️">
        <div className="space-y-3">
          {r.industry_overview && (
            <p className="text-slate-700 text-sm leading-relaxed">{r.industry_overview}</p>
          )}
          {r.competitive_landscape_overview && (
            <p className="text-slate-600 text-sm leading-relaxed">{r.competitive_landscape_overview}</p>
          )}
        </div>
      </SectionCard>
      )}

      {/* ── Competitor Deep-Dives ── */}
      {r.competitors?.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-sm font-semibold text-slate-500 uppercase tracking-wider px-1">
            Competitor Profiles ({r.competitors.length})
          </h2>
          {r.competitors.map((comp, i) => (
            <CompetitorProfileCard key={i} comp={comp} />
          ))}
        </div>
      )}

      {/* ── Benchmarking ── */}
      {r.benchmarking && (r.benchmarking.capability_benchmark?.length > 0 || r.benchmarking.market_share_comparison?.length > 0 || r.benchmarking.pricing_benchmark?.length > 0 || r.benchmarking.feature_matrix?.length > 0 || r.benchmarking.sentiment_benchmark?.length > 0) && (
      <SectionCard title="Benchmarking" icon="📊">
        <div className="space-y-6">
          {/* Capability Benchmark */}
          {r.benchmarking?.capability_benchmark?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Capability Benchmark</h3>
              <div className="overflow-x-auto">
                <table className="table-base">
                  <thead>
                    <tr>
                      <th>Company</th>
                      <th>Product</th>
                      <th>Innovation</th>
                      <th>Brand</th>
                      <th>Pricing</th>
                      <th>Distribution</th>
                      <th>Partnerships</th>
                      <th>CX</th>
                    </tr>
                  </thead>
                  <tbody>
                    {r.benchmarking.capability_benchmark.map((row, i) => (
                      <tr key={i}>
                        <td className="font-semibold text-slate-800 whitespace-nowrap">{row.company}</td>
                        <td><CapBadge value={row.product_performance} /></td>
                        <td><CapBadge value={row.innovation_technology} /></td>
                        <td><CapBadge value={row.brand_strength} /></td>
                        <td><CapBadge value={row.pricing_competitiveness} /></td>
                        <td><CapBadge value={row.distribution_reach} /></td>
                        <td><CapBadge value={row.partnerships_ecosystem} /></td>
                        <td><CapBadge value={row.customer_experience} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Market Share Comparison */}
          {r.benchmarking?.market_share_comparison?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Market Share</h3>
              <div className="overflow-x-auto">
                <table className="table-base">
                  <thead>
                    <tr><th>Company</th><th>Market Share</th><th>Revenue</th><th>YoY Growth</th></tr>
                  </thead>
                  <tbody>
                    {r.benchmarking.market_share_comparison.map((row, i) => (
                      <tr key={i}>
                        <td className="font-semibold text-slate-800">{row.company}</td>
                        <td>{row.market_share_pct != null ? `${row.market_share_pct}%` : '—'}</td>
                        <td>{fmtUsd(row.revenue_usd_bn)}</td>
                        <td>{row.yoy_growth_pct != null ? `${row.yoy_growth_pct > 0 ? '+' : ''}${row.yoy_growth_pct}%` : '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Pricing Benchmark */}
          {r.benchmarking?.pricing_benchmark?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Pricing Benchmark</h3>
              <div className="overflow-x-auto">
                <table className="table-base">
                  <thead>
                    <tr><th>Company</th><th>Tier</th><th>Model</th><th>Value</th></tr>
                  </thead>
                  <tbody>
                    {r.benchmarking.pricing_benchmark.map((row, i) => (
                      <tr key={i}>
                        <td className="font-semibold text-slate-800">{row.company}</td>
                        <td><Badge value={row.pricing_tier} /></td>
                        <td className="text-sm">{row.pricing_model}</td>
                        <td><Badge value={row.relative_value} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Feature Matrix */}
          {r.benchmarking?.feature_matrix?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Feature Matrix</h3>
              <div className="overflow-x-auto">
                <table className="table-base">
                  <thead>
                    <tr>
                      <th>Feature</th>
                      {Object.keys(r.benchmarking.feature_matrix[0]?.scores ?? {}).map((co) => (
                        <th key={co}>{co}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {r.benchmarking.feature_matrix.map((row, i) => (
                      <tr key={i}>
                        <td className="font-medium">{row.feature}</td>
                        {Object.values(row.scores).map((v, j) => (
                          <td key={j}><Badge value={v} /></td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Sentiment */}
          {r.benchmarking?.sentiment_benchmark?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Market Sentiment</h3>
              <div className="space-y-2">
                {r.benchmarking.sentiment_benchmark.map((row, i) => (
                  <div key={i} className="flex items-start gap-4 bg-slate-50 rounded-lg p-3">
                    <span className="font-semibold text-slate-800 w-32 flex-shrink-0 text-sm">{row.company}</span>
                    <Badge value={row.overall_sentiment} />
                    <div className="flex flex-wrap gap-1.5">
                      {row.key_themes?.map((t, j) => (
                        <span key={j} className="text-xs text-slate-500 bg-white border border-slate-200 px-2 py-0.5 rounded-full">{t}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </SectionCard>
      )}

      {/* ── Cross-Competitor Analysis ── */}
      {r.cross_competitor && (
      <SectionCard title="Cross-Competitor Analysis" icon="🔍">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {r.cross_competitor?.competitive_battlegrounds?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Competitive Battlegrounds</h3>
              <BulletList items={r.cross_competitor.competitive_battlegrounds} />
            </div>
          )}
          {r.cross_competitor?.client_capability_gaps?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-red-500 uppercase mb-2">Client Capability Gaps</h3>
              <BulletList items={r.cross_competitor.client_capability_gaps} />
            </div>
          )}
          {r.cross_competitor?.client_capability_leads?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-green-600 uppercase mb-2">Client Capability Leads</h3>
              <BulletList items={r.cross_competitor.client_capability_leads} />
            </div>
          )}
          {r.cross_competitor?.emerging_trends?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Emerging Trends</h3>
              <BulletList items={r.cross_competitor.emerging_trends} />
            </div>
          )}
        </div>
        {r.cross_competitor?.industry_investment_direction && (
          <p className="text-sm text-slate-600 leading-relaxed mt-4">{r.cross_competitor.industry_investment_direction}</p>
        )}
      </SectionCard>
      )}

      {/* ── White Spaces ── */}
      {r.white_spaces?.length > 0 && (
        <SectionCard title="White Space Opportunities" icon="💡">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {r.white_spaces.map((ws, i) => (
              <div key={i} className="border border-slate-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-indigo-600 uppercase">{ws.category}</span>
                  <Badge value={ws.attractiveness} />
                </div>
                <p className="font-medium text-sm text-slate-800">{ws.description}</p>
                <p className="text-xs text-slate-500 mt-2">{ws.rationale}</p>
              </div>
            ))}
          </div>
        </SectionCard>
      )}

      {/* ── Strategic Implications ── */}
      {(r.competitive_threats?.length > 0 || r.competitive_advantages?.length > 0 || r.strategic_risks?.length > 0) && (
      <SectionCard title="Strategic Implications" icon="⚔️">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {r.competitive_threats?.length > 0 && (
            <div className="bg-red-50 border border-red-100 rounded-lg p-4">
              <h3 className="text-xs font-semibold text-red-600 uppercase mb-2">Threats</h3>
              <BulletList items={r.competitive_threats} />
            </div>
          )}
          {r.competitive_advantages?.length > 0 && (
            <div className="bg-green-50 border border-green-100 rounded-lg p-4">
              <h3 className="text-xs font-semibold text-green-700 uppercase mb-2">Advantages</h3>
              <BulletList items={r.competitive_advantages} />
            </div>
          )}
          {r.strategic_risks?.length > 0 && (
            <div className="bg-amber-50 border border-amber-100 rounded-lg p-4">
              <h3 className="text-xs font-semibold text-amber-700 uppercase mb-2">Strategic Risks</h3>
              <BulletList items={r.strategic_risks} />
            </div>
          )}
        </div>
      </SectionCard>
      )}

      {/* ── Recommendations ── */}
      {(r.strategic_priorities?.length > 0 || r.defend?.length > 0 || r.differentiate?.length > 0 || r.expand?.length > 0) && (
      <SectionCard title="Strategic Recommendations" icon="🎯">
        <div className="space-y-5">
          {r.strategic_priorities?.length > 0 && (
            <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-4">
              <h3 className="text-xs font-semibold text-indigo-600 uppercase mb-2">Strategic Priorities</h3>
              <BulletList items={r.strategic_priorities} />
            </div>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <RecoBlock label="Defend" items={r.defend} color="red" />
            <RecoBlock label="Differentiate" items={r.differentiate} color="indigo" />
            <RecoBlock label="Expand" items={r.expand} color="green" />
          </div>
        </div>
      </SectionCard>
      )}
    </div>
  )
}

// ── Sub-components ────────────────────────────────────────────────────────────

function CompetitorProfileCard({ comp }: { comp: CompetitorProfile }) {
  return (
    <div className="section-card">
      <div className="section-header flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h3 className="font-semibold text-slate-800">{comp.name}</h3>
          {comp.is_user_specified && (
            <span className="text-xs bg-brand-100 text-brand-600 px-2 py-0.5 rounded-full font-medium">Specified</span>
          )}
          {comp.public_private && <Badge value={comp.public_private} />}
        </div>
        <div className="flex items-center gap-4 text-sm text-slate-500">
          {comp.revenue_usd_bn != null && <span>{fmtUsd(comp.revenue_usd_bn)} revenue</span>}
          {comp.market_share_pct != null && <span>{comp.market_share_pct}% share</span>}
          {comp.threat_level && (
            <span className="flex items-center gap-1">
              Threat: <Badge value={comp.threat_level} />
            </span>
          )}
        </div>
      </div>
      <div className="section-body">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {/* Overview */}
          <div>
            <h4 className="text-xs font-semibold text-slate-400 uppercase mb-2">Overview</h4>
            <dl className="space-y-1 text-sm">
              {comp.hq && <InfoRow label="HQ" value={comp.hq} />}
              {comp.founded && <InfoRow label="Founded" value={comp.founded} />}
              {comp.employee_count && <InfoRow label="Employees" value={comp.employee_count} />}
              {comp.financial_strength && <InfoRow label="Fin. Strength" value={<Badge value={comp.financial_strength} />} />}
            </dl>
          </div>

          {/* Products & Differentiators */}
          <div>
            <h4 className="text-xs font-semibold text-slate-400 uppercase mb-2">Core Offerings</h4>
            <BulletList items={comp.core_offerings?.slice(0, 4)} />
            {comp.differentiators?.length > 0 && (
              <div className="mt-3">
                <h4 className="text-xs font-semibold text-slate-400 uppercase mb-1">Differentiators</h4>
                <BulletList items={comp.differentiators?.slice(0, 3)} />
              </div>
            )}
          </div>

          {/* Strengths / Weaknesses */}
          <div>
            <h4 className="text-xs font-semibold text-green-600 uppercase mb-2">Strengths</h4>
            <BulletList items={comp.strengths?.slice(0, 3)} />
            {comp.weaknesses?.length > 0 && (
              <div className="mt-3">
                <h4 className="text-xs font-semibold text-red-500 uppercase mb-1">Weaknesses</h4>
                <BulletList items={comp.weaknesses?.slice(0, 3)} />
              </div>
            )}
          </div>

          {/* Strategic Moves */}
          {(comp.recent_acquisitions?.length > 0 || comp.product_launches?.length > 0 || comp.strategic_partnerships?.length > 0) && (
            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase mb-2">Recent Moves</h4>
              {comp.recent_acquisitions?.length > 0 && (
                <div className="mb-2">
                  <p className="text-xs text-slate-400 mb-1">Acquisitions</p>
                  <BulletList items={comp.recent_acquisitions.slice(0, 2)} />
                </div>
              )}
              {comp.product_launches?.length > 0 && (
                <div className="mb-2">
                  <p className="text-xs text-slate-400 mb-1">Product Launches</p>
                  <BulletList items={comp.product_launches.slice(0, 2)} />
                </div>
              )}
            </div>
          )}

          {/* Customer */}
          {(comp.core_customer_segments?.length > 0 || comp.brand_positioning) && (
            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase mb-2">Go-To-Market</h4>
              {comp.brand_positioning && (
                <p className="text-xs text-slate-600 mb-2 italic">"{comp.brand_positioning}"</p>
              )}
              {comp.core_customer_segments?.length > 0 && (
                <BulletList items={comp.core_customer_segments.slice(0, 3)} />
              )}
            </div>
          )}

          {/* Threat */}
          {(comp.strongest_competition_areas?.length > 0 || comp.future_risk_potential) && (
            <div>
              <h4 className="text-xs font-semibold text-red-400 uppercase mb-2">Threat Assessment</h4>
              {comp.strongest_competition_areas?.length > 0 && (
                <BulletList items={comp.strongest_competition_areas.slice(0, 3)} />
              )}
              {comp.future_risk_potential && (
                <p className="text-xs text-slate-500 mt-2">{comp.future_risk_potential}</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function InfoRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex gap-2">
      <dt className="text-slate-400 w-20 flex-shrink-0">{label}</dt>
      <dd className="text-slate-700">{value}</dd>
    </div>
  )
}

const capColors: Record<string, string> = {
  Leading: 'bg-green-100 text-green-700',
  Strong: 'bg-blue-100 text-blue-700',
  Average: 'bg-amber-100 text-amber-700',
  Weak: 'bg-red-100 text-red-700',
}

function CapBadge({ value }: { value: string }) {
  if (!value) return <span className="text-slate-300">—</span>
  const cls = capColors[value] ?? 'bg-slate-100 text-slate-600'
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${cls}`}>
      {value}
    </span>
  )
}

function RecoBlock({
  label,
  items,
  color,
}: {
  label: string
  items: { action: string; rationale: string; time_horizon: string; expected_impact: string }[]
  color: 'red' | 'indigo' | 'green'
}) {
  const colors = {
    red: 'text-red-600',
    indigo: 'text-indigo-600',
    green: 'text-green-600',
  }
  if (!items?.length) return null
  return (
    <div>
      <h3 className={`text-xs font-semibold uppercase mb-3 ${colors[color]}`}>{label}</h3>
      <div className="space-y-3">
        {items.map((rec, i) => (
          <div key={i} className="bg-slate-50 rounded-lg p-3 border border-slate-100">
            <p className="font-medium text-sm text-slate-800">{rec.action}</p>
            <p className="text-xs text-slate-500 mt-1">{rec.rationale}</p>
            <div className="flex gap-3 mt-2 text-xs text-slate-400">
              {rec.time_horizon && <span>⏱ {rec.time_horizon}</span>}
              {rec.expected_impact && <span>📈 {rec.expected_impact}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
