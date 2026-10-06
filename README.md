# Skellige MO2 Theme

A Mod Organizer 2 theme in the look of the Apocrypha Menu Framework for The Witcher 3's default theme, "Skellige": thin
grey lines with crossed scratch marks at the corners and a blood-red highlight, on the black of the game's own main-menu
column. The row under the mouse and the selected row get the frame The Witcher 3 draws round its own menu entries - a thin
outer line and an inner line whose corners step in - as AMF does in game.

Separators and mods are coloured separately (separators are the mod list's parent rows; MO2's conflict highlight on mods
stays visible), AMF's frame art sits around panels and group boxes, buttons, check boxes and arrows are drawn in the
theme's shape, and the toolbar and MO2's small buttons carry the Njordlinger icon set in the theme's line colour.

## Install

Extract into your Mod Organizer 2 folder (the one with ModOrganizer.exe) so `stylesheets\Skellige.qss` and the
`stylesheets\Skellige\` folder land in MO2's own `stylesheets` folder, then pick **Skellige** in Settings > General >
Style. Restart MO2 once so the toolbar picks up the icons.

## Notes

* List rows are 3px taller above and below than MO2's own, so the frame clears the text.
* Rows do not alternate in shade (the theme draws both shades in the same black, and alternate rows would draw the frame
  twice).

## Building

`python tools\build_theme.py` (Python 3 with Pillow) writes `stylesheets\` from `src\theme.qss.in`, `src\theme.json`
(the palette), the art in `src\` and the icons in `src\icons\`.

Licence: GPL-3.0-or-later (`LICENSE`, `NOTICE.md`).
