'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const toolLinks = [
  { href: '/market-scan', label: 'Market Scan' },
  { href: '/competitor', label: 'Competitor Analysis' },
  { href: '/case-study', label: 'Case Studies' },
]

const secondaryLinks = [
  { href: '/how-it-works', label: 'How it Works' },
  { href: '/about', label: 'About' },
]

export default function Nav() {
  const pathname = usePathname()

  const linkClass = (href: string) =>
    `px-3 py-1.5 rounded text-sm transition-colors ${
      pathname === href
        ? 'bg-stone-700 text-white font-medium'
        : 'text-stone-300 hover:text-white hover:bg-stone-700'
    }`

  return (
    <header className="bg-stone-900 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center h-14 gap-6">
        <Link
          href="/"
          className="text-white font-display font-semibold text-sm tracking-wide flex items-center gap-2 shrink-0"
        >
          <span className="bg-bronze-400 text-stone-900 rounded px-1.5 py-0.5 text-xs font-bold uppercase tracking-widest">
            MI
          </span>
          Market Intelligence
        </Link>

        <nav className="flex gap-1 flex-1">
          {toolLinks.map((l) => (
            <Link key={l.href} href={l.href} className={linkClass(l.href)}>
              {l.label}
            </Link>
          ))}
        </nav>

        <nav className="flex gap-1 border-l border-stone-700 pl-4">
          {secondaryLinks.map((l) => (
            <Link key={l.href} href={l.href} className={linkClass(l.href)}>
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  )
}
