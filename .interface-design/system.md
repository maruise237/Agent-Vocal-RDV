# Interface Design System

## Direction

**Personality:** Centre de contrôle calme  
**Foundation:** Light mode, cool-neutral surfaces, teal operational accent  
**Depth:** Layered but quiet panels with thin borders and low-opacity shadows  
**Use case:** Internal dashboard for monitoring voice-agent appointments and availability.

## Intent

The interface is for a business operator who wants to understand appointment activity quickly, without hunting through settings. It should feel reliable, organized, and ready for daily use.

## Tokens

### Typography

- Sans: `Aptos`, `Segoe UI`, system UI
- Mono: `Cascadia Mono`, `SFMono-Regular`, `Consolas`
- Data values use tabular numbers.
- Headings use semibold/strong weight, not oversized marketing type.

### Color

- Ink: cool navy-neutral
- Paper: very light cool surface
- Accent: teal/emerald for operational actions and connected state
- Success: green
- Warning: amber
- Danger: red
- Info: blue

Color should communicate state or hierarchy. Avoid decorative purple/blue AI gradients.

### Spacing

Base unit: `4px`

Scale:

- `4px`
- `8px`
- `12px`
- `16px`
- `20px`
- `24px`
- `32px`
- `40px`

### Radius

- Small controls: `5px`
- Inputs and buttons: `8px`
- Panels: `12px`
- Status pills: full radius

## Components

### App Shell

Sticky topbar with brand, connection status, and last sync time. No sidebar until there are multiple real sections.

### Metrics

Four metric cards maximum in the first row. Numbers use monospace tabular typography.

### Tables

Dense desktop table with horizontal rhythm. On mobile, rows collapse into readable stacked cards.

### Availability

Availability windows are presented as editable operational cards. Configuration should use business-friendly controls:

- day toggle buttons instead of numeric day input;
- quick presets for weekdays, weekend, every day, morning, and afternoon;
- hour dropdowns instead of free numeric inputs;
- add, duplicate, and remove actions per window;
- inline validation before saving.

The operator should not need to remember that Monday is `0` or type comma-separated values.

### Feedback

Use inline status text for save/load/login feedback. Do not use browser alerts.

## Rules

- Keep dashboard pages task-focused, not marketing-focused.
- Prefer clear labels over clever labels.
- Keep the primary action teal.
- Add tests when changing dashboard shell behavior.
- Keep templates out of the Python router.
