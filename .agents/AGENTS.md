# Project Rules for LeadScan AI

- **Platform Focus:** Android-First.
- **Frontend Framework:** Flutter is the ONLY frontend technology permitted.
  - Do NOT generate React components.
  - Do NOT generate Next.js pages or apps.
  - Do NOT generate HTML/CSS or Web UI code.
- **Design System & Source of Truth:** The exported Stitch design in `design/` is FINAL and approved.
  - Do NOT redesign, alter, or "improve" any UI layouts, colors, spacing, typography, icons, or navigation unless explicitly instructed.
- **Backend & Logic:** Reuse the existing Python backend (`services/api`, `services/worker`), database, REST/WebSocket APIs, OCR pipeline, AI services, business logic, and Google Sheets integration.
- **Implementation Scope:** Implement ONLY Flutter Material 3 code (`ThemeData(useMaterial3: true)`) matching the approved Stitch design export.
