# Vendored LaTeX packages

Small `.sty` files the NAGJ build needs that are NOT in the minimal
`pandoc/latex` CI image. The build fetches these into its working dir and points
`TEXINPUTS` at them, so the PDF build does not depend on `tlmgr` (which fails on
the image's frozen TeX Live).

- `outlines.sty` — the `outline` list environment (LPPL 1.3+). Used by every
  list, since `filters/lists-to-outline.lua` converts Markdown lists to it.
- `placeins.sty` — `\FloatBarrier` (public domain). Optional, for authors.

To refresh: copy from a TeX Live install
(`cp "$(kpsewhich outlines.sty)" .`).
