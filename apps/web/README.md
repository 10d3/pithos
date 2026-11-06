# PITHOS WEB APPLICATION (apps/web)
> **The 4D Planetary Interface & Tactical Mission Console.**  
> Built with Next.js 16, React 19, CesiumJS, and Tailwind CSS. (No `src/` directory convention).

The web console delivers the 4D operational picture. It allows users to scrub across historical logistics build-ups ($T-30\text{d}$), view live physical telemetry ($T_0$), and project future escalation cones ($T+14\text{d}$) with classified ops-room aesthetics.

---

## Tech Stack & Dependencies

* **Framework:** Next.js 16 (App Router) + React 19
* **3D Virtual Globe:** CesiumJS + Google Photorealistic 3D Tiles
* **Styling & UI:** Tailwind CSS v4, `@workspace/ui` (shadcn), `@hugeicons/react`
* **Typography:** `Inter` (UI/Cards) + `JetBrains Mono` (Tabular numbers & telemetry) via `next/font/google`
* **State Management:** Zustand (for 4D time scrubber, layer toggles, selected entity)

---

## Directory Blueprint

```text
apps/web/
├── app/                        # Next.js App Router
│   ├── layout.tsx              # Loads Inter & JetBrains Mono fonts, sets dark theme
│   ├── page.tsx                # Main Pithos Console (loads CesiumGlobe with ssr: false)
│   ├── globals.css             # Tactical HUD styles, glassmorphism, CRT raster lines
│   └── api/                    # Next.js API routes (optional telemetry proxy)
│
├── components/                 # React UI Components
│   ├── cesium/                 # 3D Globe & Canvas
│   │   ├── CesiumGlobe.tsx     # 'use client' dynamic wrapper (ssr: false)
│   │   └── ShadersOverlay.tsx  # FLIR thermal vision & CRT post-process overlays
│   │
│   ├── hud/                    # Tactical Ops Room Chrome
│   │   ├── HudHeader.tsx       # Zulu clock, target coordinates, system status
│   │   ├── LeftRail.tsx        # Layer toggles (Flights, Vessels, Thermal, Cones)
│   │   └── RightRail.tsx       # Live incoming telemetry feed & active hot-spots
│   │
│   ├── timeline/               # 4D Temporal Controls (Elpis)
│   │   ├── TimeScrubber.tsx    # Bottom timeline slider (T-30d <-> T0 <-> T+14d)
│   │   ├── PlaybackControls.tsx# Play, pause, 1x/10x speed multiplier
│   │   └── ScenarioPicker.tsx  # Base Case vs. Escalation scenario branch selector
│   │
│   └── cards/                  # Forensic & Predictive Slide-outs
│       ├── CuiBonoCard.tsx     # Pandora: Arms maker, contracts, shell companies
│       └── ForecastCard.tsx    # Elpis: Escalation probability & casualty risk
│
├── lib/                        # Core Engine & Network Code
│   ├── cesium/                 # CesiumJS Setup (adapted from gods-eye-view)
│   │   ├── viewer.ts           # Cesium Viewer constructor
│   │   ├── google3d.ts         # Google Photorealistic 3D Tiles loader
│   │   ├── camera.ts           # Smooth fly-to, orbital tracking, target locking
│   │   └── shaders/            # WebGL GLSL Shaders (flir.glsl, crt.glsl, sonar.glsl)
│   │
│   ├── layers/                 # Map Layer Controllers
│   │   ├── militaryFlights.ts  # Filtered cargo/refueler flights
│   │   ├── darkVessels.ts      # AIS vessels & dead-reckoning probability clouds
│   │   ├── thermalSpikes.ts    # NASA FIRMS frontline artillery/strikes
│   │   └── forecastCones.ts    # Monte Carlo uncertainty polygons
│   │
│   ├── network/                # Communication
│   │   └── apiClient.ts        # Typed fetch client for Pandora (8001) & Elpis (8002)
│   │
│   └── timeline/               # 4D Time Scrubber State
│       └── timeStore.ts        # Zustand store holding active temporal offset (t)
│
├── public/                     # Static Assets
│   ├── cesium/                 # Cesium static distribution (Assets, Workers, Widgets)
│   └── icons/                  # Tactical SVG icons
│
├── next.config.ts              # Next.js build configuration (Cesium copy plugin/rewrites)
├── package.json
└── tsconfig.json
```

---

## Critical Next.js & Cesium Implementation Rules

### 1. Zero SSR on the 3D Globe
CesiumJS depends on browser WebGL contexts and the `window` object. It **must** be dynamically loaded with `ssr: false` in `app/page.tsx`:
```tsx
const CesiumGlobe = dynamic(
  () => import('@/components/cesium/CesiumGlobe'),
  { ssr: false, loading: () => <LoadingTacticalHUD /> }
);
```

### 2. Serving Cesium Static Assets
Cesium requires pre-compiled Web Workers and textures. Configure `next.config.ts` or an npm post-install script to copy `node_modules/cesium/Build/Cesium` assets into `public/cesium/`.

### 3. Font Integration (`app/layout.tsx`)
Tabular figures are mandatory for coordinates and timestamps so numbers do not jump or jitter during live streaming:
```tsx
import { Inter, JetBrains_Mono } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });
const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="bg-black text-white antialiased overflow-hidden font-sans">
        {children}
      </body>
    </html>
  );
}
```

---

## Features to Implement (Step-by-Step)

### Phase 1: The 3D Engine Setup
1. Add `cesium` dependency to `apps/web/package.json`.
2. Port Google 3D Tiles loader from `gods-eye-view/src/maps/google3d.js` into `lib/cesium/google3d.ts`.
3. Create `components/cesium/CesiumGlobe.tsx` to mount the Cesium canvas full-screen.

### Phase 2: Tactical HUD & Typography
1. Build `HudHeader.tsx`: Displays UTC / Zulu clock, current camera Lat/Lon/Alt, and system health status in `JetBrains Mono`.
2. Build `LeftRail.tsx`: Layer toggle chips (Flights, Vessels, Thermal Spikes, Risk Hexes).

### Phase 3: The 4D Timeline Scrubber (Elpis Integration)
1. Build `TimeScrubber.tsx`: A slider anchored at the bottom of the viewport spanning:
   * $T-30\text{d}$ (Historical replay)
   * $T_0$ (Live real-time feed)
   * $T+14\text{d}$ (Simulated future)
2. When the user scrubs into the future, `apps/web` calls `services/elpis` at `http://localhost:8002/api/v1/simulation/timeline?t_offset_hours=X` and renders the forward uncertainty cones.

### Phase 4: The Cui Bono Dossier (Pandora Integration)
1. Build `CuiBonoCard.tsx`: A collapsible right-side drawer that slides out when an entity or conflict hotspot is clicked.
2. Queries `services/pandora` at `http://localhost:8001/api/v1/cui-bono/{entity_id}` to display:
   * Prime contractor name & stock ticker
   * Awarded contract values
   * Shell company ownership trail
   * Contested mineral / pipeline concessions

---

## Running the Web App
```bash
# From repository root
pnpm --filter web dev
```
Open `http://localhost:3000` in your browser.
