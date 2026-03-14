// ── Shared ────────────────────────────────────────────────────────────────────

export interface ScanRequest {
  company: string
  market: string
  time_period_months: number
  additional_competitors?: string[]
}

export interface SearchResult {
  url: string
  title: string
  content: string
  published_date: string
  source: string
}

// ── Market Scan ───────────────────────────────────────────────────────────────

export interface MarketSnapshot {
  market_size_usd_bn: number | null
  cagr_percent: number | null
  key_segments: string[]
  geographic_distribution: Record<string, string>
  industry_maturity: string
}

export interface Implications {
  focus_areas: string[]
  areas_to_avoid: string[]
  strategic_risks: string[]
}

export interface SegmentationDimension {
  dimension: string
  segments: string[]
  strategic_relevance: string
}

export interface MarketDefinition {
  industry_definition: string
  value_chain_scope: string
  products_services_included: string[]
  methodology: string
  sizing_approach: string
  assumptions: string[]
  segmentation_framework: SegmentationDimension[]
}

export interface HistoricalDataPoint {
  year: number
  value_usd_bn: number
  note: string
}

export interface ForecastDataPoint {
  year: number
  value_usd_bn: number
  is_forecast: boolean
}

export interface MarketSizeData {
  tam_usd_bn: number | null
  sam_usd_bn: number | null
  som_usd_bn: number | null
  historical_cagr_percent: number | null
  forecast_cagr_percent: number | null
  forecast_size_5yr_usd_bn: number | null
  historical_data: HistoricalDataPoint[]
  forecast_data: ForecastDataPoint[]
  growth_drivers: string[]
  growth_constraints: string[]
  cyclicality_notes: string
}

export interface ValueChainStage {
  stage: string
  description: string
  key_players: string[]
  margin_capture: string
  power_dynamics: string
}

export interface ProfitPoolSegment {
  segment: string
  margin_percent: number | null
  profitability_tier: string
  notes: string
}

export interface MarketStructure {
  value_chain: ValueChainStage[]
  profit_pools: ProfitPoolSegment[]
  typical_cost_structure: Record<string, string>
  pricing_models: string[]
  capex_intensity: string
  where_margins_captured: string
  where_power_sits: string
}

export interface CompetitorEntry {
  name: string
  tier: string
  market_share_pct: number | null
  revenue_usd_bn: number | null
  geographic_reach: string
  key_strengths: string[]
}

export interface PositioningMatrixEntry {
  company: string
  x_axis_value: number
  y_axis_value: number
  tier: string
}

export interface CompetitiveLandscape {
  overview_narrative: string
  key_players: CompetitorEntry[]
  market_concentration: string
  positioning_x_axis: string
  positioning_y_axis: string
  positioning_matrix: PositioningMatrixEntry[]
  strategic_moves: string[]
  new_entrants_disruptors: string[]
}

export interface CustomerSegment {
  name: string
  description: string
  size_estimate: string
  growth_rate: string
}

export interface CustomerAnalysis {
  segments: CustomerSegment[]
  key_purchase_drivers: string[]
  pain_points: string[]
  unmet_needs: string[]
  decision_makers: string[]
  procurement_process: string
  switching_costs: string
  willingness_to_pay: string
  lifetime_value_notes: string
  price_sensitivity: string
}

export interface TechTrend {
  technology: string
  description: string
  impact_level: string
  time_horizon: string
}

export interface RDPlayer {
  company: string
  rd_spend_usd_bn: number | null
  rd_as_pct_revenue: number | null
  notable_patents: string[]
}

export interface TechTrends {
  product_innovations_5yr: string[]
  disruptive_technologies: TechTrend[]
  rd_intensity_notes: string
  rd_leaders: RDPlayer[]
  innovation_pipeline: string[]
}

export interface RegulatoryItem {
  area: string
  description: string
  impact: string
  region: string
}

export interface MacroFactor {
  factor: string
  current_state: string
  impact_on_market: string
}

export interface ESGItem {
  area: string
  description: string
  regulatory_pressure: string
}

export interface RegulatoryFactors {
  regulations: RegulatoryItem[]
  macro_factors: MacroFactor[]
  esg_trends: ESGItem[]
}

export interface RegionData {
  region: string
  market_size_usd_bn: number | null
  share_pct: number | null
  cagr_percent: number | null
  growth_stage: string
}

export interface GeographicLandscape {
  regions: RegionData[]
  growth_hotspots: string[]
  local_champion_markets: string[]
  global_vs_local_dynamics: string
}

export interface Deal {
  deal_type: string
  acquirer: string
  target: string
  value_usd_mn: number | null
  date: string
  strategic_rationale: string
}

export interface InvestmentMA {
  recent_deals: Deal[]
  pe_themes: string[]
  vc_emerging_startups: string[]
  capital_flow_narrative: string
  total_deal_value_usd_bn: number | null
}

export interface Risk {
  category: string
  risk: string
  likelihood: string
  impact: string
  mitigation: string
}

export interface StrategicPlay {
  play_type: string
  description: string
  rationale: string
  estimated_impact: string
}

export interface StrategicOpportunities {
  white_space_opportunities: string[]
  capability_fit_areas: string[]
  potential_strategic_plays: StrategicPlay[]
  recommended_priorities: string[]
}

export interface MarketScanReport {
  scan_id: string
  company: string
  market: string
  time_period_months: number
  generated_at: string
  market_snapshot: MarketSnapshot
  key_insights: string[]
  implications: Implications
  opportunities_identified: string[]
  exec_summary_bullets: string[]
  market_definition: MarketDefinition
  market_size: MarketSizeData
  market_structure: MarketStructure
  competitive_landscape: CompetitiveLandscape
  customer_analysis: CustomerAnalysis
  tech_trends: TechTrends
  regulatory: RegulatoryFactors
  geographic: GeographicLandscape
  investment_ma: InvestmentMA
  risks: Risk[]
  strategic_opportunities: StrategicOpportunities
  all_sources: SearchResult[]
}

export interface MarketScanJob {
  job_id: string
  status: 'queued' | 'researching' | 'synthesizing' | 'complete' | 'error'
  progress_message: string
  progress_pct: number
  error: string | null
  report: MarketScanReport | null
}

// ── Competitor Analysis ───────────────────────────────────────────────────────

export interface CompetitorProfile {
  name: string
  is_user_specified: boolean
  hq: string
  founded: string
  geographic_footprint: string[]
  revenue_usd_bn: number | null
  revenue_growth_pct: number | null
  market_share_pct: number | null
  employee_count: string
  public_private: string
  revenue_streams: string[]
  pricing_model: string
  profit_drivers: string[]
  cost_structure_summary: string
  core_offerings: string[]
  differentiators: string[]
  technology_capabilities: string[]
  innovation_pipeline: string[]
  core_customer_segments: string[]
  industry_focus: string[]
  geographic_focus: string[]
  key_accounts: string[]
  sales_model: string
  distribution_channels: string[]
  brand_positioning: string
  customer_acquisition: string
  recent_acquisitions: string[]
  product_launches: string[]
  strategic_partnerships: string[]
  geographic_expansion: string[]
  revenue_trend: string
  profitability_trend: string
  rd_investment: string
  financial_strength: string
  strengths: string[]
  weaknesses: string[]
  operational_strengths: string[]
  customer_sentiment: string
  industry_reputation: string
  brand_perception: string
  notable_reviews: string[]
  threat_level: string
  strongest_competition_areas: string[]
  future_risk_potential: string
}

export interface CapabilityBenchmarkRow {
  company: string
  product_performance: string
  innovation_technology: string
  brand_strength: string
  pricing_competitiveness: string
  distribution_reach: string
  partnerships_ecosystem: string
  customer_experience: string
}

export interface FeatureMatrixRow {
  feature: string
  scores: Record<string, string>
}

export interface PricingBenchmarkRow {
  company: string
  pricing_tier: string
  pricing_model: string
  relative_value: string
}

export interface MarketShareRow {
  company: string
  market_share_pct: number | null
  revenue_usd_bn: number | null
  yoy_growth_pct: number | null
}

export interface SentimentRow {
  company: string
  overall_sentiment: string
  key_themes: string[]
}

export interface PositioningPoint {
  company: string
  x_value: number
  y_value: number
  is_client: boolean
}

export interface Benchmarking {
  capability_benchmark: CapabilityBenchmarkRow[]
  feature_matrix: FeatureMatrixRow[]
  pricing_benchmark: PricingBenchmarkRow[]
  market_share_comparison: MarketShareRow[]
  sentiment_benchmark: SentimentRow[]
  positioning_x_axis: string
  positioning_y_axis: string
  positioning_map: PositioningPoint[]
}

export interface CrossCompetitorAnalysis {
  competitive_battlegrounds: string[]
  client_capability_gaps: string[]
  client_capability_leads: string[]
  emerging_trends: string[]
  common_strategic_themes: string[]
  industry_investment_direction: string
}

export interface WhiteSpace {
  category: string
  description: string
  attractiveness: string
  rationale: string
}

export interface StrategicRecommendation {
  action: string
  rationale: string
  time_horizon: string
  expected_impact: string
}

export interface CompetitorReport {
  report_id: string
  company: string
  market: string
  time_period_months: number
  generated_at: string
  purpose: string
  key_findings: string[]
  strategic_implications: string[]
  industry_overview: string
  industry_structure_summary: string
  competitive_landscape_overview: string
  positioning_x_axis: string
  positioning_y_axis: string
  market_positioning_map: PositioningPoint[]
  competitors: CompetitorProfile[]
  benchmarking: Benchmarking
  cross_competitor: CrossCompetitorAnalysis
  white_spaces: WhiteSpace[]
  competitive_threats: string[]
  competitive_advantages: string[]
  strategic_risks: string[]
  defend: StrategicRecommendation[]
  differentiate: StrategicRecommendation[]
  expand: StrategicRecommendation[]
  strategic_priorities: string[]
  all_sources: Record<string, unknown>[]
  identified_competitors: string[]
}

export interface CompetitorJob {
  job_id: string
  status: 'queued' | 'identifying' | 'researching' | 'synthesizing' | 'complete' | 'error'
  progress_message: string
  progress_pct: number
  error: string | null
  report: CompetitorReport | null
}

// ── Case Studies ──────────────────────────────────────────────────────────────

export interface CaseStudy {
  number: number
  title: string
  innovation_description: string
  problem_solved: string
  where_emerging: string
  lead_company: string
  implementation_description: string
  metrics_outcomes: string[]
  customer_impact: string
  business_performance_impact: string
  competitive_dynamics_impact: string
  key_takeaways: string[]
  client_relevance: string
  potential_opportunity: string
  innovation_type: string
  maturity_level: string
}

export interface CaseStudyReport {
  report_id: string
  company: string
  market: string
  time_period_months: number
  generated_at: string
  case_studies: CaseStudy[]
  report_narrative: string
  all_sources: Record<string, unknown>[]
}

export interface CaseStudyJob {
  job_id: string
  status: 'queued' | 'researching' | 'identifying' | 'synthesizing' | 'complete' | 'error'
  progress_message: string
  progress_pct: number
  error: string | null
  report: CaseStudyReport | null
}
