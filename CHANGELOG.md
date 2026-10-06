# Changelog - Skellige MO2 Theme

Versions are issued by the project's version gate. Written as the change happens (rule 61).

## 1.0.0 - 2026-10-06

First version. The owner, 2026-10-05: *"build a matching MO2 theme for the Skellige theme that we used on AMF"*.

* Begun as a copy of the Oathvein MO2 Theme, as AMF's Skellige began as Oathvein: the same stylesheet, button, check
  box, radio and arrow drawings and recoloured Njordlinger icons.
* AMF Witcher 3's Skellige colours: background #020203 (the game's main-menu black), grey lines #A6A8A7, text #E8E8E8,
  accent #8E2A2E; dark red separators. No background texture, as AMF's Skellige has none.
* The game's frame round the hovered row (55% of the text colour) and the selected row (95%), as AMF's hover and
  controller frames: nine-slice art in four pieces so a row of many columns gets one frame. The owner on the result:
  *"the framing on the rows in MO2's mods pane looks good"*.
* Rows 3px taller above and below so the frame clears the text; no side padding, which in MO2's mod list moves the tick
  box but not the name.
* No alternating rows: on an alternate row Qt draws the item rule again across the whole row, so every other mod's frame
  ran out into the indent (the owner: *"it's every other mod"*).
