# Style: `cyber-network-hud` (Cyber Telemetry & Network HUD)

## Essence
A precision dark-mode engineering HUD designed for technical systems, packet routing, algorithms, cloud infrastructure, and cybersecurity stories.

## Visual Palette
- **Background**: Deep obsidian `#070B14` with subtle `#0F1B2E` 60px coordinate grid lines.
- **Primary Signal**: Electric Cyan `#00F0FF` (active flows, primary packets, hero headers).
- **Secondary Signal**: Emerald `#10B981` (ACKs, verified states) & Signal Amber `#F59E0B` (SYN requests, warnings).
- **Typography**: Monospace (`'JetBrains Mono', 'Fira Code', 'Courier New', monospace`), uppercase tracking for headers, live numeric counters (`0x00A4`, latency ms).

## Motion Grammar
- Nodes scale in with `Easing.outBack`.
- Connections draw progressively along vector paths with glowing packet dots travelling from source to destination (`lerp(x1, x2, p)`).
- Corner HUD brackets and live timestamp readouts run continuously in the periphery.
