# Copilot Instructions

- Scope: teaching/experiments on topological data analysis (TDA), simplicial complexes, and time-delay embeddings for time series. Work happens mainly in notebooks alongside a couple of lightweight Python helpers.
- Code layout: core helpers in [drawing_utils.py](../drawing_utils.py#L6-L74) (SVG drawing of simplices/complexes) and [simplicial.py](../simplicial.py#L5-L82) (Simplex and SimplicialComplex math/helpers). Data lives under [data/](../data); primary notebook is [Pràctica 10 - Time Delay Embeddings.ipynb](../Pr%C3%A0ctica%2010%20-%20Time%20Delay%20Embeddings.ipynb).
- Simplices: `Simplex` stores sorted vertex tuples and derives `dim` from length. Faces are generated in order; equality/hash rely on the sorted tuple. Preserve sorting if creating new Simplex helpers.
- Complexes: `SimplicialComplex.instantiate_maximally` recursively adds all faces; adding higher-dim simplices without closing under faces breaks Euler characteristic/betti calculations. `basis` is grouped by dim and order-sensitive; keep deterministic ordering when extending.
- Algebra: `diff_matrix` builds boundary operators with signs `(-1)^j`; passes through an optional `field` callable expecting `.characteristic`. `betti_numbers` relies on `numpy.linalg.matrix_rank`; supply integer matrices or field-reduced ones.
- Drawing: `draw_simplex` supports dims 0–2 only and labels each simplex centroid; higher dims raise. `draw` accepts individual Simplex or SimplicialComplex and can show axes (axis=True). If you extend drawing, keep compatibility with `draw()` and `_repr_html_` on complexes.
- Notebooks: keep existing markdown prompts intact; add solutions as new code cells next to the prompts. Avoid altering cell order/wording. Use pandas/matplotlib idioms already present. For time-delay embeddings, follow patterns demonstrated in the notebook (shifted columns, dropping NaNs, sampling).
- Data handling: CSV files in [data/](../data) are small teaching datasets; do not modify or regenerate them unless asked. File names are referenced in notebooks; keep paths stable.
- Dependencies: uses numpy, pandas, matplotlib, drawsvg (for SVG export), and giotto-tda (TakensEmbedding). Prefer the existing `.venv` if available; otherwise install with `pip install numpy pandas matplotlib drawsvg giotto-tda`.
- Execution: notebooks run in-place; no project-wide tests or builds. The file [p11](../p11) just runs `python -m cubix`—not currently integrated elsewhere.
- Style: default to ASCII; avoid introducing Unicode in code. Keep comments concise and only where logic is non-obvious. Preserve Spanish/Catalan notebook text as-is.
- Outputs: drawing helpers return `drawsvg.Drawing`; render via `.as_svg()` in notebooks. For algebra functions, prefer returning numpy arrays or plain ints.
- Safety: do not touch `.venv/` or git metadata. Respect the order of simplices when adding/removing to avoid changing homology results unintentionally.

If anything here seems unclear or incomplete for your task, ask for specifics before editing.
