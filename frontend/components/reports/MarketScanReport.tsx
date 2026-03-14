import type { MarketScanReport } from '@/lib/types'
import { SectionCard, BulletList, Badge, Empty, fmt, fmtUsd } from '@/components/ui'

export default function MarketScanReportView({ r }: { r: MarketScanReport }) {
  return (
    <div className="space-y-6">
      {/* ── Header ── */}
      <div className="bg-slate-900 text-white rounded-xl p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="text-slate-400 text-xs uppercase tracking-widest mb-1">Market Scan</p>
            <h1 className="text-2xl font-bold">{r.market}</h1>
            <p className="text-slate-300 mt-1 text-sm">Client: {r.company}</p>
          </div>
          <div className="text-right text-sm text-slate-400 space-y-1">
            <p>Research horizon: {r.time_period_months} months</p>
            <p>Generated: {new Date(r.generated_at).toLocaleDateString()}</p>
          </div>
        </div>
        {r.market_snapshot && (
          <div className="mt-5 grid grid-cols-2 sm:grid-cols-4 gap-4">
            <StatBox label="Market Size" value={fmtUsd(r.market_snapshot.market_size_usd_bn)} />
            <StatBox label="CAGR" value={fmt(r.market_snapshot.cagr_percent, '%')} />
            <StatBox label="Maturity" value={r.market_snapshot.industry_maturity || '—'} />
            <StatBox label="Key Segments" value={`${r.market_snapshot.key_segments?.length ?? 0}`} />
          </div>
        )}
      </div>

      {/* ── Exec Summary ── */}
      <SectionCard title="Executive Summary" icon="📋">
        <div className="space-y-4">
          {r.exec_summary_bullets?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Summary</h3>
              <BulletList items={r.exec_summary_bullets} />
            </div>
          )}
          {r.key_insights?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Key Insights</h3>
              <BulletList items={r.key_insights} />
            </div>
          )}
          {r.implications && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <ImplicationsBox label="Focus Areas" items={r.implications.focus_areas} color="green" />
              <ImplicationsBox label="Areas to Avoid" items={r.implications.areas_to_avoid} color="red" />
              <ImplicationsBox label="Strategic Risks" items={r.implications.strategic_risks} color="amber" />
            </div>
          )}
        </div>
      </SectionCard>

      {/* ── Market Definition ── */}
      <SectionCard title="Market Definition" icon="🗺️">
        <div className="space-y-4">
          {r.market_definition?.industry_definition && (
            <p className="text-slate-700 text-sm leading-relaxed">{r.market_definition.industry_definition}</p>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {r.market_definition?.products_services_included?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">In-Scope Products & Services</h3>
                <BulletList items={r.market_definition.products_services_included} />
              </div>
            )}
            {r.market_definition?.assumptions?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Assumptions</h3>
                <BulletList items={r.market_definition.assumptions} />
              </div>
            )}
          </div>
          {r.market_definition?.segmentation_framework?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Segmentation Framework</h3>
              <div className="space-y-3">
                {r.market_definition.segmentation_framework.map((dim, i) => (
                  <div key={i} className="bg-slate-50 rounded-lg p-3">
                    <p className="font-medium text-sm text-slate-800">{dim.dimension}</p>
                    <div className="flex flex-wrap gap-1.5 mt-1.5">
                      {dim.segments.map((s, j) => (
                        <span key={j} className="bg-white border border-slate-200 text-xs px-2 py-0.5 rounded-full text-slate-600">{s}</span>
                      ))}
                    </div>
                    {dim.strategic_relevance && (
                      <p className="text-xs text-slate-500 mt-1.5">{dim.strategic_relevance}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </SectionCard>

      {/* ── Market Size ── */}
      <SectionCard title="Market Size & Growth" icon="📈">
        <div className="space-y-5">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <MetricBox label="TAM" value={fmtUsd(r.market_size?.tam_usd_bn)} sub="Total Addressable" />
            <MetricBox label="SAM" value={fmtUsd(r.market_size?.sam_usd_bn)} sub="Serviceable" />
            <MetricBox label="SOM" value={fmtUsd(r.market_size?.som_usd_bn)} sub="Obtainable" />
            <MetricBox label="5-yr Forecast" value={fmtUsd(r.market_size?.forecast_size_5yr_usd_bn)} sub={`CAGR ${fmt(r.market_size?.forecast_cagr_percent, '%')}`} />
          </div>

          {(r.market_size?.historical_data?.length > 0 || r.market_size?.forecast_data?.length > 0) && (
            <div className="overflow-x-auto">
              <table className="table-base">
                <thead>
                  <tr>
                    <th>Year</th>
                    <th>Value (USD B)</th>
                    <th>Type</th>
                    <th>Note</th>
                  </tr>
                </thead>
                <tbody>
                  {r.market_size.historical_data?.map((d, i) => (
                    <tr key={i}>
                      <td className="font-medium">{d.year}</td>
                      <td>${d.value_usd_bn}B</td>
                      <td><span className="text-xs text-slate-500">Historical</span></td>
                      <td className="text-slate-500">{d.note}</td>
                    </tr>
                  ))}
                  {r.market_size.forecast_data?.map((d, i) => (
                    <tr key={i} className="bg-blue-50/30">
                      <td className="font-medium">{d.year}</td>
                      <td>${d.value_usd_bn}B</td>
                      <td><span className="text-xs text-blue-600 font-medium">Forecast</span></td>
                      <td />
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {r.market_size?.growth_drivers?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Growth Drivers</h3>
                <BulletList items={r.market_size.growth_drivers} />
              </div>
            )}
            {r.market_size?.growth_constraints?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Growth Constraints</h3>
                <BulletList items={r.market_size.growth_constraints} />
              </div>
            )}
          </div>
        </div>
      </SectionCard>

      {/* ── Market Structure ── */}
      <SectionCard title="Market Structure" icon="🏗️">
        <div className="space-y-5">
          {r.market_structure?.value_chain?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Value Chain</h3>
              <div className="overflow-x-auto">
                <table className="table-base">
                  <thead>
                    <tr>
                      <th>Stage</th>
                      <th>Description</th>
                      <th>Margin Capture</th>
                      <th>Power Dynamics</th>
                      <th>Key Players</th>
                    </tr>
                  </thead>
                  <tbody>
                    {r.market_structure.value_chain.map((s, i) => (
                      <tr key={i}>
                        <td className="font-semibold text-slate-800 whitespace-nowrap">{s.stage}</td>
                        <td>{s.description}</td>
                        <td><Badge value={s.margin_capture} /></td>
                        <td className="text-slate-500 text-xs">{s.power_dynamics}</td>
                        <td className="text-xs">{s.key_players?.join(', ')}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {r.market_structure?.profit_pools?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Profit Pools</h3>
              <div className="overflow-x-auto">
                <table className="table-base">
                  <thead>
                    <tr><th>Segment</th><th>Margin %</th><th>Tier</th><th>Notes</th></tr>
                  </thead>
                  <tbody>
                    {r.market_structure.profit_pools.map((p, i) => (
                      <tr key={i}>
                        <td className="font-medium">{p.segment}</td>
                        <td>{p.margin_percent != null ? `${p.margin_percent}%` : '—'}</td>
                        <td><Badge value={p.profitability_tier} /></td>
                        <td className="text-slate-500">{p.notes}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {r.market_structure?.capex_intensity && (
              <KeyValueBox label="CapEx Intensity" value={<Badge value={r.market_structure.capex_intensity} />} />
            )}
            {r.market_structure?.where_margins_captured && (
              <KeyValueBox label="Where Margins Are Captured" value={r.market_structure.where_margins_captured} />
            )}
            {r.market_structure?.where_power_sits && (
              <KeyValueBox label="Where Power Sits" value={r.market_structure.where_power_sits} />
            )}
          </div>
        </div>
      </SectionCard>

      {/* ── Competitive Landscape ── */}
      <SectionCard title="Competitive Landscape" icon="⚔️">
        <div className="space-y-5">
          {r.competitive_landscape?.overview_narrative && (
            <p className="text-slate-700 text-sm leading-relaxed">{r.competitive_landscape.overview_narrative}</p>
          )}
          {r.competitive_landscape?.key_players?.length > 0 && (
            <div className="overflow-x-auto">
              <table className="table-base">
                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Tier</th>
                    <th>Market Share</th>
                    <th>Revenue</th>
                    <th>Geography</th>
                    <th>Key Strengths</th>
                  </tr>
                </thead>
                <tbody>
                  {r.competitive_landscape.key_players.map((p, i) => (
                    <tr key={i}>
                      <td className="font-semibold text-slate-800">{p.name}</td>
                      <td><Badge value={p.tier} /></td>
                      <td>{p.market_share_pct != null ? `${p.market_share_pct}%` : '—'}</td>
                      <td>{fmtUsd(p.revenue_usd_bn)}</td>
                      <td className="text-slate-500 text-xs">{p.geographic_reach}</td>
                      <td className="text-xs">{p.key_strengths?.slice(0, 2).join('; ')}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {r.competitive_landscape?.strategic_moves?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Strategic Moves</h3>
                <BulletList items={r.competitive_landscape.strategic_moves} />
              </div>
            )}
            {r.competitive_landscape?.new_entrants_disruptors?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">New Entrants & Disruptors</h3>
                <BulletList items={r.competitive_landscape.new_entrants_disruptors} />
              </div>
            )}
          </div>
        </div>
      </SectionCard>

      {/* ── Customer Analysis ── */}
      <SectionCard title="Customer Analysis" icon="👥">
        <div className="space-y-5">
          {r.customer_analysis?.segments?.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {r.customer_analysis.segments.map((seg, i) => (
                <div key={i} className="bg-slate-50 rounded-lg p-4 border border-slate-100">
                  <p className="font-semibold text-sm text-slate-800">{seg.name}</p>
                  <p className="text-xs text-slate-600 mt-1">{seg.description}</p>
                  {(seg.size_estimate || seg.growth_rate) && (
                    <div className="flex gap-3 mt-2 text-xs text-slate-500">
                      {seg.size_estimate && <span>Size: {seg.size_estimate}</span>}
                      {seg.growth_rate && <span>Growth: {seg.growth_rate}</span>}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {r.customer_analysis?.key_purchase_drivers?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Purchase Drivers</h3>
                <BulletList items={r.customer_analysis.key_purchase_drivers} />
              </div>
            )}
            {r.customer_analysis?.pain_points?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Pain Points</h3>
                <BulletList items={r.customer_analysis.pain_points} />
              </div>
            )}
            {r.customer_analysis?.unmet_needs?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Unmet Needs</h3>
                <BulletList items={r.customer_analysis.unmet_needs} />
              </div>
            )}
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {r.customer_analysis?.switching_costs && (
              <KeyValueBox label="Switching Costs" value={<Badge value={r.customer_analysis.switching_costs} />} />
            )}
            {r.customer_analysis?.price_sensitivity && (
              <KeyValueBox label="Price Sensitivity" value={<Badge value={r.customer_analysis.price_sensitivity} />} />
            )}
            {r.customer_analysis?.willingness_to_pay && (
              <KeyValueBox label="WTP" value={r.customer_analysis.willingness_to_pay} />
            )}
            {r.customer_analysis?.procurement_process && (
              <KeyValueBox label="Procurement" value={r.customer_analysis.procurement_process} />
            )}
          </div>
        </div>
      </SectionCard>

      {/* ── Technology Trends ── */}
      <SectionCard title="Technology Trends" icon="⚡">
        <div className="space-y-5">
          {r.tech_trends?.disruptive_technologies?.length > 0 && (
            <div className="overflow-x-auto">
              <table className="table-base">
                <thead>
                  <tr><th>Technology</th><th>Description</th><th>Impact</th><th>Time Horizon</th></tr>
                </thead>
                <tbody>
                  {r.tech_trends.disruptive_technologies.map((t, i) => (
                    <tr key={i}>
                      <td className="font-semibold text-slate-800 whitespace-nowrap">{t.technology}</td>
                      <td className="text-sm">{t.description}</td>
                      <td><Badge value={t.impact_level} /></td>
                      <td><span className="text-xs text-slate-500">{t.time_horizon}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {r.tech_trends?.product_innovations_5yr?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Product Innovations (5yr)</h3>
                <BulletList items={r.tech_trends.product_innovations_5yr} />
              </div>
            )}
            {r.tech_trends?.innovation_pipeline?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Innovation Pipeline</h3>
                <BulletList items={r.tech_trends.innovation_pipeline} />
              </div>
            )}
          </div>
          {r.tech_trends?.rd_leaders?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">R&D Leaders</h3>
              <div className="overflow-x-auto">
                <table className="table-base">
                  <thead>
                    <tr><th>Company</th><th>R&D Spend</th><th>% of Revenue</th></tr>
                  </thead>
                  <tbody>
                    {r.tech_trends.rd_leaders.map((rd, i) => (
                      <tr key={i}>
                        <td className="font-medium">{rd.company}</td>
                        <td>{fmtUsd(rd.rd_spend_usd_bn)}</td>
                        <td>{rd.rd_as_pct_revenue != null ? `${rd.rd_as_pct_revenue}%` : '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </SectionCard>

      {/* ── Regulatory & External ── */}
      <SectionCard title="Regulatory & External Factors" icon="⚖️">
        <div className="space-y-5">
          {r.regulatory?.regulations?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Regulations</h3>
              <div className="overflow-x-auto">
                <table className="table-base">
                  <thead>
                    <tr><th>Area</th><th>Description</th><th>Impact</th><th>Region</th></tr>
                  </thead>
                  <tbody>
                    {r.regulatory.regulations.map((reg, i) => (
                      <tr key={i}>
                        <td className="font-semibold text-slate-800 whitespace-nowrap">{reg.area}</td>
                        <td className="text-sm">{reg.description}</td>
                        <td><Badge value={reg.impact} /></td>
                        <td className="text-xs text-slate-500">{reg.region}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          {r.regulatory?.macro_factors?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">Macro Factors</h3>
              <div className="space-y-2">
                {r.regulatory.macro_factors.map((m, i) => (
                  <div key={i} className="bg-slate-50 rounded-lg p-3 grid grid-cols-3 gap-2 text-sm">
                    <span className="font-semibold text-slate-800">{m.factor}</span>
                    <span className="text-slate-600">{m.current_state}</span>
                    <span className="text-slate-500 text-xs">{m.impact_on_market}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {r.regulatory?.esg_trends?.length > 0 && (
            <div>
              <h3 className="text-xs font-semibold text-slate-500 uppercase mb-3">ESG Trends</h3>
              <div className="space-y-2">
                {r.regulatory.esg_trends.map((e, i) => (
                  <div key={i} className="flex items-start gap-3 text-sm">
                    <span className="font-medium text-slate-700 w-28 flex-shrink-0">{e.area}</span>
                    <span className="text-slate-600 flex-1">{e.description}</span>
                    <Badge value={e.regulatory_pressure} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </SectionCard>

      {/* ── Geographic ── */}
      <SectionCard title="Geographic Landscape" icon="🌍">
        <div className="space-y-5">
          {r.geographic?.regions?.length > 0 && (
            <div className="overflow-x-auto">
              <table className="table-base">
                <thead>
                  <tr><th>Region</th><th>Market Size</th><th>Share %</th><th>CAGR</th><th>Stage</th></tr>
                </thead>
                <tbody>
                  {r.geographic.regions.map((reg, i) => (
                    <tr key={i}>
                      <td className="font-semibold text-slate-800">{reg.region}</td>
                      <td>{fmtUsd(reg.market_size_usd_bn)}</td>
                      <td>{reg.share_pct != null ? `${reg.share_pct}%` : '—'}</td>
                      <td>{reg.cagr_percent != null ? `${reg.cagr_percent}%` : '—'}</td>
                      <td><Badge value={reg.growth_stage} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {r.geographic?.growth_hotspots?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Growth Hotspots</h3>
                <BulletList items={r.geographic.growth_hotspots} />
              </div>
            )}
            {r.geographic?.local_champion_markets?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Local Champion Markets</h3>
                <BulletList items={r.geographic.local_champion_markets} />
              </div>
            )}
          </div>
          {r.geographic?.global_vs_local_dynamics && (
            <p className="text-sm text-slate-600 leading-relaxed">{r.geographic.global_vs_local_dynamics}</p>
          )}
        </div>
      </SectionCard>

      {/* ── Investment & M&A ── */}
      <SectionCard title="Investment & M&A" icon="💰">
        <div className="space-y-5">
          {r.investment_ma?.recent_deals?.length > 0 && (
            <div className="overflow-x-auto">
              <table className="table-base">
                <thead>
                  <tr><th>Type</th><th>Acquirer</th><th>Target</th><th>Value</th><th>Date</th><th>Rationale</th></tr>
                </thead>
                <tbody>
                  {r.investment_ma.recent_deals.map((d, i) => (
                    <tr key={i}>
                      <td><span className="text-xs font-medium text-indigo-600">{d.deal_type}</span></td>
                      <td className="font-medium">{d.acquirer}</td>
                      <td>{d.target}</td>
                      <td>{d.value_usd_mn != null ? `$${d.value_usd_mn}M` : '—'}</td>
                      <td className="text-slate-500 text-xs">{d.date}</td>
                      <td className="text-xs text-slate-500">{d.strategic_rationale}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {r.investment_ma?.capital_flow_narrative && (
            <p className="text-sm text-slate-600 leading-relaxed">{r.investment_ma.capital_flow_narrative}</p>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {r.investment_ma?.pe_themes?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">PE Themes</h3>
                <BulletList items={r.investment_ma.pe_themes} />
              </div>
            )}
            {r.investment_ma?.vc_emerging_startups?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">VC / Emerging Startups</h3>
                <BulletList items={r.investment_ma.vc_emerging_startups} />
              </div>
            )}
          </div>
        </div>
      </SectionCard>

      {/* ── Risks ── */}
      <SectionCard title="Risk Register" icon="⚠️">
        {r.risks?.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="table-base">
              <thead>
                <tr><th>Category</th><th>Risk</th><th>Likelihood</th><th>Impact</th><th>Mitigation</th></tr>
              </thead>
              <tbody>
                {r.risks.map((risk, i) => (
                  <tr key={i}>
                    <td><span className="text-xs font-medium text-slate-600">{risk.category}</span></td>
                    <td className="font-medium">{risk.risk}</td>
                    <td><Badge value={risk.likelihood} /></td>
                    <td><Badge value={risk.impact} /></td>
                    <td className="text-xs text-slate-500">{risk.mitigation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty />
        )}
      </SectionCard>

      {/* ── Strategic Opportunities ── */}
      <SectionCard title="Strategic Opportunities" icon="🎯">
        <div className="space-y-5">
          {r.strategic_opportunities?.recommended_priorities?.length > 0 && (
            <div className="bg-indigo-50 border border-indigo-100 rounded-lg p-4">
              <h3 className="text-xs font-semibold text-indigo-600 uppercase mb-2">Recommended Priorities</h3>
              <BulletList items={r.strategic_opportunities.recommended_priorities} />
            </div>
          )}
          {r.strategic_opportunities?.potential_strategic_plays?.length > 0 && (
            <div className="space-y-3">
              <h3 className="text-xs font-semibold text-slate-500 uppercase">Strategic Plays</h3>
              {r.strategic_opportunities.potential_strategic_plays.map((play, i) => (
                <div key={i} className="border border-slate-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs font-semibold text-indigo-600 uppercase bg-indigo-50 px-2 py-0.5 rounded">{play.play_type}</span>
                    <span className="font-semibold text-slate-800 text-sm">{play.description}</span>
                  </div>
                  <p className="text-xs text-slate-500">{play.rationale}</p>
                  {play.estimated_impact && (
                    <p className="text-xs text-green-600 mt-1 font-medium">Impact: {play.estimated_impact}</p>
                  )}
                </div>
              ))}
            </div>
          )}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {r.strategic_opportunities?.white_space_opportunities?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">White Space Opportunities</h3>
                <BulletList items={r.strategic_opportunities.white_space_opportunities} />
              </div>
            )}
            {r.strategic_opportunities?.capability_fit_areas?.length > 0 && (
              <div>
                <h3 className="text-xs font-semibold text-slate-500 uppercase mb-2">Capability Fit Areas</h3>
                <BulletList items={r.strategic_opportunities.capability_fit_areas} />
              </div>
            )}
          </div>
        </div>
      </SectionCard>

      {/* ── Sources ── */}
      {r.all_sources?.length > 0 && (
        <SectionCard title="Sources" icon="📚">
          <div className="space-y-1 max-h-60 overflow-y-auto pr-1">
            {r.all_sources.map((s, i) => (
              <div key={i} className="text-xs text-slate-500 flex items-start gap-2">
                <span className="flex-shrink-0 text-slate-300">{i + 1}.</span>
                <a href={s.url} target="_blank" rel="noopener noreferrer" className="text-brand-600 hover:underline truncate">
                  {s.title || s.url}
                </a>
              </div>
            ))}
          </div>
        </SectionCard>
      )}
    </div>
  )
}

// ── Sub-components ────────────────────────────────────────────────────────────

function StatBox({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-slate-800 rounded-lg p-3">
      <p className="text-slate-400 text-xs mb-1">{label}</p>
      <p className="text-white font-bold text-lg leading-none">{value || '—'}</p>
    </div>
  )
}

function MetricBox({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 text-center">
      <p className="text-xs text-slate-500 mb-1">{label}</p>
      <p className="text-xl font-bold text-slate-900">{value}</p>
      {sub && <p className="text-xs text-slate-400 mt-1">{sub}</p>}
    </div>
  )
}

function KeyValueBox({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="bg-slate-50 rounded-lg p-3 border border-slate-100">
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <div className="text-sm font-medium text-slate-700">{value}</div>
    </div>
  )
}

function ImplicationsBox({
  label,
  items,
  color,
}: {
  label: string
  items: string[]
  color: 'green' | 'red' | 'amber'
}) {
  const colors = {
    green: 'bg-green-50 border-green-100',
    red: 'bg-red-50 border-red-100',
    amber: 'bg-amber-50 border-amber-100',
  }
  const titleColors = {
    green: 'text-green-700',
    red: 'text-red-700',
    amber: 'text-amber-700',
  }
  return (
    <div className={`rounded-lg p-4 border ${colors[color]}`}>
      <h3 className={`text-xs font-semibold uppercase mb-2 ${titleColors[color]}`}>{label}</h3>
      {items?.length ? (
        <ul className="space-y-1">
          {items.map((item, i) => (
            <li key={i} className="text-xs text-slate-700">{item}</li>
          ))}
        </ul>
      ) : (
        <p className="text-xs text-slate-400 italic">None identified</p>
      )}
    </div>
  )
}
