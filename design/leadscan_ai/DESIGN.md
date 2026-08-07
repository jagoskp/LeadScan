---
name: LeadScan AI
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#006229'
  on-tertiary: '#ffffff'
  tertiary-container: '#007e37'
  on-tertiary-container: '#c1ffc5'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#6bff8f'
  tertiary-fixed-dim: '#4ae176'
  on-tertiary-fixed: '#002109'
  on-tertiary-fixed-variant: '#005321'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 57px
    fontWeight: '700'
    lineHeight: 64px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  title-lg:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '500'
    lineHeight: 28px
  title-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin-mobile: 16px
  margin-tablet: 24px
---

## Brand & Style
The design system is rooted in a **Modern Enterprise SaaS** aesthetic, blending the systematic rigor of Material Design 3 with the refined minimalism found in industry-leading productivity tools. The brand personality is authoritative yet approachable, prioritizing clarity and speed of thought for high-performance sales teams.

The visual style utilizes a **Minimalist Corporate** approach. It leverages significant whitespace (breathability), high-quality functional typography, and a "content-first" hierarchy. While following Android’s structural patterns, it elevates the standard interface through subtle tonal layers and premium finishing touches typical of high-end software.

## Colors
This design system employs a high-contrast professional palette. The **Primary Enterprise Blue** is used for critical actions and brand presence, while the **Deep Slate Secondary** provides grounded navigation and structural elements.

In **Light Mode**, surfaces are pure white to maximize the sense of space. In **Dark Mode**, the background shifts to a deep navy-gray (#111827) to maintain depth without the harshness of pure black. Surface levels are achieved through subtle increments in lightness (Light Mode) or desaturated overlays (Dark Mode), ensuring that lead data remains the focal point.

## Typography
The system uses **Inter** exclusively to ensure a systematic, utilitarian, and highly readable experience across mobile densities. 

- **Headlines:** Use tighter letter-spacing and heavier weights to create a strong editorial feel.
- **Body Text:** Standardized on 16px for primary data entry and 14px for secondary metadata to ensure legibility during rapid scanning.
- **Data Labels:** Utilize the `label-sm` style in all-caps for field headers to distinguish between "label" and "value" in lead profiles.

## Layout & Spacing
The layout follows a **Fluid Grid** model optimized for the Android handheld experience. It utilizes an 8dp spacing grid to ensure mathematical harmony between elements.

- **Margins:** 16dp on mobile, increasing to 24dp on tablets.
- **Gutters:** 16dp fixed between card elements.
- **Touch Targets:** Minimum 48x48dp for all interactive elements, regardless of visual size.
- **Vertical Rhythm:** Use 16dp (md) as the default spacing between grouped components, and 24dp (lg) to separate distinct sections or content blocks.

## Elevation & Depth
This design system utilizes **Tonal Layers** rather than heavy shadows to denote hierarchy, consistent with M3 principles but refined for a premium feel.

- **Level 0 (Base):** Primary background color.
- **Level 1 (Cards):** +1% contrast from background with a soft `4px` blur shadow (opacity 0.05).
- **Level 2 (Modals/Sheets):** +3% contrast with a `12px` blur shadow (opacity 0.08).
- **Floating Action Buttons (FAB):** Utilize a distinct primary-colored shadow to signify the "Hero" action.

In Dark Mode, elevation is communicated through increased surface lightness rather than shadow intensity.

## Shapes
The shape language is defined as **Rounded**, leaning into the sophisticated "squircle" aesthetic.

- **Standard Components:** Buttons and Input fields use a 0.5rem (8px) radius.
- **Containers:** Content cards and Bottom Sheets use `rounded-lg` (16px) or `rounded-xl` (24px) to create a soft, premium frame for data.
- **Search Bars:** Use a full "Pill" shape (32px+) to distinguish navigation/search from actionable data inputs.

## Components

### Buttons
- **Primary:** Filled with Primary Blue, 8px radius, Title-MD type.
- **Secondary:** Outlined with a 1px border (#E2E8F0), white background.
- **FAB:** Large M3-style FAB (56x56dp) with slightly rounded corners (16px), always containing a Material Symbol Rounded icon.

### Input Fields
- **Style:** Outlined M3 style.
- **State:** Active states use a 2px Primary Blue border. Error states use Success Green or Error Red icons within the trailing edge of the input.
- **Background:** Soft gray (#F8FAFC) fill to provide a clear landing zone.

### Cards (Lead Cards)
- **Structure:** 16px padding. Title-MD for lead names. 
- **Metadata:** Use Chips (8px radius) for lead status (e.g., "New", "Contacted", "Qualified") using the Accent and Warning colors.

### Bottom Sheets
- **Design:** 24px top radius. Handle bar at the top center. 
- **Usage:** Used for filtering lead lists and quick-add forms to maintain the user's context.

### Lists
- **Density:** High-density lists with 72dp row height for lead items.
- **Separators:** 1px horizontal line (#F1F5F9) with 16dp left inset to align with text.