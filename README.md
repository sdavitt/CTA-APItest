# CTA Psych API Backend Take-Home Assessment
You've been watching way too much of the TV show Psych. In it, Burton Guster (or did I mean Bruton Gaster) and others are given far too many nicknames. You need to make an API to keep track of all of the aliases in the show.

Models/Data:
- Character
    - Characters must have a non-integer ID #PK ID non-null and unique - name variant as id - maybe useful for read alias route
    - Characters must have a name #name string non-null
    - Characters can have a last-known alias (this is the Character's Alias with the most recent last-seen date) # informal? Just the Name of the alias # instead, we'll calculate this value any time we need to return it (aka for the READ specific character only)
    - Characters must have a date created

- Alias
    - Aliases must have a non-integer ID # uuid str
    - Aliases must have a name # name str
    - Aliases must have an occupation # job str
    - Aliases can have a last-seen date # datetime
    - Aliases must have a relationship to their true Character # FK to Character.ID

CRUD Operations:
- READ [GET]
    - A specific Alias
    - A specific Character and all of their Aliases
        - Name
        - Last-Known Alias
        - Date Created
        - All aliases
- CREATE [POST]
    - An Alias (hint: an alias must belong to an existing Character)
    - A Character
- UPDATE [PUT]
    - An Alias' last-seen date (hint: how does this affect Characters' last-known aliases?)
- DELETE [DELETE]
    - An Alias (hint: how does this affect Characters' last-known aliases?)
    - A Character (hint: Aliases must have a relationship to their Character)