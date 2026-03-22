# Internal branded PPTX outputs

Use this guideline when the user asks for an INO or Luqia presentation deck in `.pptx` format.

## Style reference

Use `examples/FOR-399-218.pptx` as the visual style reference for:
- theme and palette
- slide composition
- typography
- cover and section slide feel
- general brand density and spacing

This reference is read-only.

## Mandatory rules

- Never modify `examples/FOR-399-218.pptx` in place.
- Build a new presentation output file.
- Preferred approach: copy the reference deck to a new target path and edit the copy.
- Acceptable alternative: create a new deck that closely matches the reference style.
- Keep the new deck content-specific; do not leave unrelated reference content in the final output.

## Workflow

1. Confirm the requested output is a `.pptx` slide deck for INO or Luqia.
2. Inspect `examples/FOR-399-218.pptx` for style cues before building.
3. Create a new output deck by copying the reference or by building a fresh deck in the same style.
4. Replace all copied placeholder/reference content with the requested presentation content.
5. Preserve the branded visual language while adapting slide count, structure, and messaging to the request.

## Red flags

- Editing the file in `examples/FOR-399-218.pptx`
- Treating the request as a generic unbranded PowerPoint
- Reusing the reference content verbatim in the final deck
- Delivering a non-`.pptx` output when `.pptx` was requested
