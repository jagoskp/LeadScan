# LeadScan AI: Enterprise Component Library & Design Tokens (Flutter-Ready)

## 1. Design Tokens (Material 3)

### Colors
- **Primary (Enterprise Blue):** `#2563EB` (Brand consistency across all phases)
- **On-Primary:** `#FFFFFF`
- **Primary Container:** `#EFF6FF`
- **Surface:** `#F8F9FF`
- **Surface Variant:** `#F1F5F9`
- **Outline:** `#CBD5E1`
- **Success:** `#10B981` (Semantic: OCR Success, Sync Complete)
- **Error:** `#EF4444` (Semantic: Overdue Tasks, Sync Failed)
- **Warning:** `#F59E0B` (Semantic: Pending Offline)

### Typography (Inter)
- **Display Large:** 57/64 (Splash/Welcome)
- **Headline Medium:** 28/36 (Dashboard Titles)
- **Title Large:** 22/28 (App Bar Titles)
- **Label Small:** 11/16 (Navigation Labels)

### Elevation & Shapes
- **Corner Radius:** `ROUND_EIGHT` (12px - 16px for cards, 28px for FAB)
- **Elevation:** Flat (0dp) for background, Level 1 (1dp) for cards, Level 3 (6dp) for FAB.

## 2. Shared Component Library

### Navigation
- **TopAppBar:** Small & Center Aligned variants. Leading: Avatar/Back, Trailing: Notifications/Settings.
- **BottomNavBar:** 5 Destinations (Dashboard, Scanner, Leads, Workflow, Profile). Active state uses `PrimaryContainer` pill.
- **NavigationDrawer:** Enterprise-only features, left-aligned with profile header.

### Input & Controls
- **Smart Search Bar:** Rounded (full), Leading Search Icon, Trailing Filter/Voice icons.
- **Action Buttons:** Filled (Primary), Tonal (Secondary), Outlined (Tertiary).
- **Status Chips:** AI Confidence (98% High), Sync Status (Synced/Pending), Lead Status (New, Contacted).

### Feedback & Status
- **Google Sync Indicators:** Circular progress or static icons with timestamp metadata.
- **AI Processing:** Shimmer effects and progress bars with percentage indicators.
- **Empty States:** Centered 3D illustrations (IMAGE_63) with "Did you mean?" suggestions.

## 3. Animation System

- **Page Transitions:** Material 3 Shared Axis (X/Y) for repository navigation.
- **Shared Element Transitions:** Profile Avatar from Lead List to Lead Details.
- **Processing (OCR):** Pulse and scan-line shader effects (SHADER_N).
- **Micro-Interactions:** Haptic feedback on FAB tap, spring-based toggle switches.

## 4. Flutter Implementation Notes

- Use `Material3: true` in `ThemeData`.
- Map `Primary` to `Color(0xFF2563EB)`.
- Use `GoogleFonts.inter()` for the font family.
- Cards should have `clipBehavior: Clip.antiAlias` for smooth rounded corners.
- Implement the "Smart Scanner" using the `camera` and `google_ml_kit` packages.
