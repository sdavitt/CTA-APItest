# CTA Psych API Backend Take-Home Assessment
You've been watching way too much of the TV show Psych. In it, Burton Guster (or did I mean Bruton Gaster) and others are given far too many nicknames. You need to make an API to keep track of all of the aliases in the show.

Models/Data:
- Character
    - Characters must have a non-integer ID
    - Characters must have a name
    - Characters can have a last-known alias (this is the Character's Alias with the most recent last-seen date)
    - Characters must have a date created

- Alias
    - Aliases must have a non-integer ID
    - Aliases must have a name
    - Aliases must have an occupation
    - Aliases can have a last-seen date
    - Aliases must have a relationship to their true Character

CRUD Operations:
- READ
    - A specific Alias
    - A specific Character and all of their Aliases
- CREATE
    - An Alias (hint: an alias must belong to an existing Character)
    - A Character
- UPDATE
    - An Alias' last-seen date (hint: how does this affect Characters' last-known aliases?)
- DELETE
    - An Alias (hint: how does this affect Characters' last-known aliases?)
    - A Character (hint: Aliases must have a relationship to their Character)