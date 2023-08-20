# Scripts

These scripts are used to scrape and parse the game data from other sources into a workable format. They are not part of the actual app, but rather are kept here for documentation and repeatability in case the data model every requires some changes. There are some dependency between the scripts, so the order of execution matter and goes as follows:

1. `get-skills.py`
2. `get-equipment-and-decos.py`

## Sources

### Skill Categories

Skill categories were made manually, analogous to the Monster Hunter Tri ASS. 

### Skills, Equipment and Decorations

All the equipment and decoration data, as well as exact skill names, were obtained from platypete and their [Monster Hunter Dos wiki](https://mh1g-wiki.herokuapp.com/mh2/). The japanese names were manually removed as they were messing with parsing.
