import { Download } from 'lucide-react'

interface Props {
  href: string
  label?: string
}

export default function PdfDownloadButton({ href, label = 'Download PDF' }: Props) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-2 bg-slate-900 hover:bg-slate-700 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors"
    >
      <Download size={14} />
      {label}
    </a>
  )
}
