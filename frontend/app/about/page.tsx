import Link from 'next/link'

const modules = [
  {
    numeral: 'I',
    title: 'Market Scan',
    href: '/market-scan',
    sections: [
      'Executive summary and key insights',
      'Market sizing (TAM / SAM / SOM)',
      'Market structure and value chain',
      'Customer segments and buying behaviour',
      'Competitive landscape and key players',
      'Technology trends and innovation',
      'Geographic breakdown',
      'Regulatory and macro environment',
      'M&A activity',
      'Strategic opportunities and risks',
    ],
  },
  {
    numeral: 'II',
    title: 'Competitor Analysis',
    href: '/competitor',
    sections: [
      'AI-identified top competitors (up to 7)',
      'Business model and revenue streams',
      'Go-to-market and pricing strategy',
      'Financial profile and growth trajectory',
      'Product and capability benchmarking',
      'Capability radar charts',
      'Market share comparison',
      'White-space and differentiation map',
      'Strategic recommendations: defend, differentiate, expand',
    ],
  },
  {
    numeral: 'III',
    title: 'Innovation Case Studies',
    href: '/case-study',
    sections: [
      '5 curated innovations across Technology, Business Model, Operations, Customer Experience, and ESG',
      'Lead company and implementation detail',
      'Measurable outcomes and industry impact',
      'Key strategic takeaways',
      'Relevance assessment for your client',
    ],
  },
]

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">

      {/* Intro */}
      <section>
        <span className="text-xs font-bold uppercase tracking-widest text-bronze-500">About</span>
        <h1 className="font-display text-4xl font-bold text-stone-800 mt-2 mb-4">
          Research that used to take days.<br />Now takes minutes.
        </h1>
        <p className="text-stone-600 text-lg leading-relaxed max-w-2xl">
          Market Intelligence Platform is a research platform built for management consultants.
          It runs deep, parallel web research and uses AI to synthesise the results into
          structured, consultant-ready outputs: market scans, competitor analyses, and innovation
          case studies.
        </p>
      </section>

      {/* Who it's for */}
      <section className="bg-white border border-stone-200 rounded-2xl p-8">
        <h2 className="font-display text-xl font-semibold text-stone-800 mb-4">Built for consultants</h2>
        <div className="grid sm:grid-cols-2 gap-6 text-sm text-stone-600 leading-relaxed">
          <div>
            <div className="font-semibold text-stone-700 mb-1">Starting a new engagement</div>
            Get a full market orientation in minutes. Understand sizing, structure, key players,
            and strategic dynamics before your first client call.
          </div>
          <div>
            <div className="font-semibold text-stone-700 mb-1">Preparing competitive context</div>
            Run a competitor deep-dive with benchmarking matrices and white-space analysis
            ready to drop into your deck.
          </div>
          <div>
            <div className="font-semibold text-stone-700 mb-1">Supporting client workshops</div>
            Generate innovation case studies to anchor strategy discussions with real-world
            precedents from the same industry.
          </div>
          <div>
            <div className="font-semibold text-stone-700 mb-1">Augmenting your research team</div>
            Handle the first-pass synthesis so analysts can spend time on interpretation
            and client-specific nuance instead of information gathering.
          </div>
        </div>
      </section>

      {/* Modules */}
      <section>
        <h2 className="font-display text-2xl font-semibold text-stone-800 mb-6">Three modules</h2>
        <div className="space-y-4">
          {modules.map((m) => (
            <div key={m.title} className="bg-white border border-stone-200 rounded-xl overflow-hidden">
              <div className="px-6 py-4 flex items-center gap-3 border-b border-stone-100">
                <span className="font-display text-bronze-400 font-bold text-sm">{m.numeral}</span>
                <h3 className="font-display font-semibold text-stone-800">{m.title}</h3>
                <Link href={m.href} className="ml-auto text-xs text-bronze-500 hover:underline font-medium">
                  Open →
                </Link>
              </div>
              <ul className="px-6 py-4 grid sm:grid-cols-2 gap-x-6 gap-y-1.5">
                {m.sections.map((s) => (
                  <li key={s} className="flex items-start gap-2 text-sm text-stone-600">
                    <span className="text-bronze-500 mt-0.5 text-xs flex-shrink-0">▸</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="text-center pt-4">
        <Link
          href="/how-it-works"
          className="inline-block bg-stone-800 hover:bg-stone-900 text-white font-semibold px-6 py-2.5 rounded-lg text-sm transition-colors"
        >
          See how it works →
        </Link>
      </section>

    </div>
  )
}
