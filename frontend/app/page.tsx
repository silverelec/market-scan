import Link from 'next/link'

const features = [
  {
    href: '/market-scan',
    numeral: 'I',
    title: 'Market Scan',
    description:
      'Full-depth market intelligence covering sizing, structure, competitive landscape, customer segments, technology trends, geography, and strategic opportunities.',
    cta: 'Start Market Scan',
  },
  {
    href: '/competitor',
    numeral: 'II',
    title: 'Competitor Analysis',
    description:
      'Deep-dive profiles on every key competitor: business model, GTM motion, financials, strengths, weaknesses, benchmarking matrices, and strategic recommendations.',
    cta: 'Start Competitor Analysis',
  },
  {
    href: '/case-study',
    numeral: 'III',
    title: 'Innovation Case Studies',
    description:
      '5 curated innovation case studies from the market, with impact analysis, measurable outcomes, and a tailored relevance assessment for your client.',
    cta: 'Start Case Studies',
  },
]

const stats = [
  { value: '12', label: 'report sections per scan' },
  { value: '30+', label: 'parallel research queries' },
  { value: '5 min', label: 'average turnaround' },
  { value: 'PDF', label: 'export ready' },
]

export default function HomePage() {
  return (
    <div>
      {/* Hero */}
      <section
        className="relative text-white py-24 px-4 overflow-hidden"
        style={{
          backgroundImage:
            'url(https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920&q=80)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        {/* Overlay */}
        <div className="absolute inset-0 bg-stone-900/70 pointer-events-none" />
        <div className="max-w-4xl mx-auto text-center relative">
          <span className="inline-block bg-bronze-400 text-stone-900 text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full mb-6">
            Market Intelligence Platform
          </span>
          <h1 className="font-display text-4xl sm:text-5xl font-bold leading-tight mb-5">
            Boardroom-ready research,
            <br />
            <span className="text-bronze-400">in minutes.</span>
          </h1>
          <p className="text-stone-300 text-lg max-w-2xl mx-auto leading-relaxed">
            Skip the research sprint. AI-driven parallel web search and structured synthesis
            deliver consultant-grade market intelligence before your next coffee.
          </p>
          <div className="flex flex-wrap justify-center gap-3 mt-8">
            <Link
              href="/market-scan"
              className="bg-bronze-400 hover:bg-bronze-300 text-stone-900 font-semibold px-6 py-2.5 rounded-lg text-sm transition-colors"
            >
              Start a Market Scan
            </Link>
            <Link
              href="/how-it-works"
              className="bg-stone-800 hover:bg-stone-700 text-white font-semibold px-6 py-2.5 rounded-lg text-sm transition-colors border border-stone-600"
            >
              See how it works
            </Link>
          </div>
        </div>
      </section>

      {/* Stats strip */}
      <section className="bg-stone-800 text-white py-5 px-4">
        <div className="max-w-4xl mx-auto grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          {stats.map((s) => (
            <div key={s.label}>
              <div className="font-display text-2xl font-bold text-bronze-400">{s.value}</div>
              <div className="text-xs text-stone-400 mt-0.5">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Feature Cards */}
      <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <h2 className="font-display text-2xl font-semibold text-stone-800 text-center mb-8">
          Three tools, one workflow
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((f) => (
            <div
              key={f.href}
              className="bg-white rounded-2xl border border-stone-200 shadow-sm overflow-hidden flex flex-col"
            >
              <div className="bg-stone-900 p-6 text-white relative">
                <div className="absolute top-0 left-0 right-0 h-0.5 bg-bronze-400" />
                <span className="font-display text-bronze-400 text-2xl font-bold">{f.numeral}</span>
                <h2 className="font-display text-xl font-bold mt-2">{f.title}</h2>
              </div>
              <div className="p-6 flex flex-col flex-1">
                <p className="text-stone-600 text-sm leading-relaxed flex-1">{f.description}</p>
                <Link
                  href={f.href}
                  className="mt-5 inline-flex items-center justify-center gap-2 bg-stone-800 hover:bg-stone-900 text-white text-sm font-semibold px-4 py-2.5 rounded-lg transition-colors"
                >
                  {f.cta} →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="bg-stone-800 py-12 px-4 text-white text-center">
        <h2 className="font-display text-2xl font-semibold mb-2">
          Ready to run your first scan?
        </h2>
        <p className="text-stone-400 text-sm mb-6 max-w-md mx-auto">
          Enter a market and get a structured intelligence report in minutes. No lengthy prompting required.
        </p>
        <Link
          href="/market-scan"
          className="inline-block bg-bronze-400 text-stone-900 font-semibold px-6 py-2.5 rounded-lg text-sm hover:bg-bronze-300 transition-colors"
        >
          Start a Market Scan
        </Link>
      </section>
    </div>
  )
}
