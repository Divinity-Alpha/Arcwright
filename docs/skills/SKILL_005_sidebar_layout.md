# SKILL 005 — Website Sidebar Layout
**Category:** Website Development
**Status:** Working — rules documented
**Reliability:** High when rules are followed
**Discovered:** help.html / docs.html development

## Problem
Sidebar navigation links collapse into horizontal packed
mess instead of vertical list. Sometimes entire page
content disappears.

## Root Causes
1. Using <nav> tag instead of <div> — browsers apply
   default flex/inline styling to nav elements
2. align-items:start on grid container instead of
   align-self:start on individual children
3. Missing display:flex + flex-direction:column on
   sidebar and sidebar-section
4. Unclosed sidebar-section div — content swallowed

## Required CSS Rules
```css
/* Grid container — NO align-items */
.help-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 56px;
  /* NO align-items:start here */
}

/* Sidebar — ALL FOUR properties required */
.help-sidebar {
  align-self: start;        /* on child, not parent */
  position: sticky;
  top: 90px;
  display: flex;            /* required */
  flex-direction: column;   /* required */
}

/* Section — explicit vertical stack */
.sidebar-section {
  margin-bottom: 28px;
  display: flex;
  flex-direction: column;
}

/* Link — explicit block */
.sidebar-link {
  display: block;
  width: 100%;
}
```

## HTML Rules
- Use <div class="help-sidebar"> NOT <nav class="help-sidebar">
- Every sidebar-section must be a properly closed <div>
- Orphaned links outside their section div breaks layout
- Missing </div> on sidebar container = all content disappears

## Verification Checklist
Fixed on help.html and docs.html
Rules added to CLAUDE.md v17.0
