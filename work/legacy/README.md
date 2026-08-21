# Superseded extractors

`extract.py` and `extract2.py` were the first two attempts at pulling the book's
Arabic out of the PDF. Both dumped the glyph stream in *visual* order, which is
what produced the mirrored lines and mangled ligatures preserved in
`docs/archive/Ref.md`.

**Neither is part of the pipeline.** `work/build_md.py` replaced them and is the
only extractor that should be run. These are kept as the record of how the
`CORRECTIONS` map in `build_md.py` was arrived at.
