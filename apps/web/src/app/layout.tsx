import type { Metadata } from "next";
import Link from "next/link";
import "@leadscan/ui/src/global.css";

export const metadata: Metadata = {
  title: "LeadScan AI - Intelligent Lead Capture",
  description: "Enterprise SaaS platform for intelligent lead extraction, validation and verification.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased bg-slate-950 text-slate-100 min-h-screen flex flex-col">
        <header className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex items-center justify-between sticky top-0 z-50">
          <div className="flex items-center gap-3">
            <Link href="/" className="text-xl font-extrabold text-blue-500 tracking-tight">
              LeadScan AI
            </Link>
            <span className="bg-blue-500/10 text-blue-400 text-xs px-2 py-0.5 rounded font-mono border border-blue-500/20">
              v1.0.0
            </span>
          </div>

          <nav className="flex items-center gap-1 text-sm font-medium">
            <Link href="/dashboard" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Dashboard
            </Link>
            <Link href="/scan" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Scan
            </Link>
            <Link href="/upload" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Upload
            </Link>
            <Link href="/camera" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Camera
            </Link>
            <Link href="/review-workspace" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Review Workspace
            </Link>
            <Link href="/google-sheets" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Google Sheets
            </Link>
            <Link href="/search" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Search
            </Link>
            <Link href="/workflow" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Workflow
            </Link>
            <Link href="/leads" className="px-3 py-1.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition">
              Leads
            </Link>
          </nav>
        </header>

        <main className="flex-1">
          {children}
        </main>
      </body>
    </html>
  );
}
