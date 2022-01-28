# Change Log

## v0.3.7

- Updated to use new templates API curvenote endpoints, with a fallback to previous endpoints just in case

## v0.3.5 - Breaking Changes

- cli has been restructured to now provide `freeform` and `render` commands in place of `build-lite` and `build`
- Reduced the number of command line options
- Data is now supplied in a front matter section at the head of the `content.tex` file, rather than in a separate `data.yml`. This makes it easier to reference a single specific file, rather than having to rely on a specific set of namd files in the content folder.
- Documentation in the [README](README.md) has been updated to reflect these changes
