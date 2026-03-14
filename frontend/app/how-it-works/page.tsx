import Link from 'next/link'

const steps = [
  {
    n: '1',
    title: 'Enter your brief',
    body: 'Provide a company name, target market, and time horizon. For competitor analysis you can optionally name specific competitors to include.',
    detail: 'Takes about 30 seconds. No lengthy prompting required.',
  },
  {
    n: '2',
    title: 'Parallel web research fires',
    body: 'The platform runs 20 to 35 targeted queries simultaneously across real-time web and semantic search engines for analyst reports and whitepapers. Results are deduplicated and ranked.',
    detail: 'Roughly equivalent to 3 to 4 hours of manual desk research.',
  },
  {
    n: '3',
    title: 'AI synthesises the findings',
    body: 'Multiple AI synthesis calls run in parallel, each responsible for a distinct section: market sizing, competitive landscape, technology trends, M&A activity, and more. A final synthesis pass writes the executive summary and strategic implications.',
    detail: 'Each section is structured JSON, not a freeform essay.',
  },
  {
    n: '4',
    title: 'Report renders live, PDF ready',
    body: 'The structured output renders directly in the browser as a formatted report. A one-click PDF export packages everything with charts and tables for client delivery.',
    detail: 'Total time: 4 to 8 minutes depending on market complexity.',
  },
]

export default function HowItWorksPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">

      {/* Header */}
      <section>
        <span className="text-xs font-bold uppercase tracking-widest text-bronze-500">How it Works</span>
        <h1 className="font-display text-4xl font-bold text-stone-800 mt-2 mb-4">
          From brief to report in under 10 minutes
        </h1>
        <p className="text-stone-600 text-lg leading-relaxed max-w-2xl">
          Four steps, fully automated. Here is what happens under the hood.
        </p>
      </section>

      {/* Steps */}
      <section>
        <div className="space-y-4">
          {steps.map((s) => (
            <div key={s.n} className="bg-white border border-stone-200 rounded-xl p-6 flex gap-5">
              <div className="w-9 h-9 bg-stone-800 text-white rounded-full flex items-center justify-center text-sm font-bold font-display shrink-0 mt-0.5">
                {s.n}
              </div>
              <div>
                <h3 className="font-display font-semibold text-stone-800 text-base mb-1">{s.title}</h3>
                <p className="text-stone-600 text-sm leading-relaxed">{s.body}</p>
                <p className="text-bronze-500 text-xs mt-2 font-medium">{s.detail}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="bg-stone-800 rounded-2xl p-8 text-white text-center">
        <h2 className="font-display text-2xl font-semibold mb-2">Ready to run your first scan?</h2>
        <p className="text-stone-400 text-sm mb-6">Enter a market and get a structured intelligence report in minutes.</p>
        <div className="flex flex-wrap justify-center gap-3">
          <Link
            href="/market-scan"
            className="bg-bronze-400 hover:bg-bronze-300 text-stone-900 font-semibold px-6 py-2.5 rounded-lg text-sm transition-colors"
          >
            Run a Market Scan
          </Link>
          <Link
            href="/about"
            className="bg-stone-700 hover:bg-stone-600 text-white font-semibold px-6 py-2.5 rounded-lg text-sm transition-colors border border-stone-600"
          >
            Learn more
          </Link>
        </div>
      </section>

    </div>
  )
}
