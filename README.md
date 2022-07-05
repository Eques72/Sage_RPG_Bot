
# Sage RPG - a discord d&d bot
**Ask mysterious sage a question about spells, feats, classes, rules, equipment, race features and backgrounds**
> The application allows to display information about the dnd 5e game in 
> a Discord application chat.
>  App searches for this information on the internet and processing it to readable info accordingly.

## Invitation link:
> Use this link to add this bot to your Discord server.

https://discord.com/api/oauth2/authorize?client_id=986263052108324904&permissions=277025778688&scope=bot

 
# Usage:
## COMMANDS:
- "!dndhelp" - command used to show this panel
- "!dndsage <any  phrase  you  want  to  search  for> <optional  flags>" - see more below
- "!dndclass \<class  name>\<optional  flags>"
- "!dndrace \<race  name> \<optional  flags>"
- "!dndspell \<spell  name> "
- "!dndfeat \<feat  name> "
- "!dndbackground <background  name> "
### ARGUMENTS
Instead of brackets in list above enter according phrases you wish to see.

Eg: Instead of: **!dndfeat \<feat  name>** write **!dndfeat Chef** or **!dndfeat chef** or any feat name, do similar with other commands

## !DNDSAGE

Unique and universal command, it has the ability to find answers for most of your questios, but there is bigger chance that it will take sligthly longer to execute. In opposition to other commands you can make misspell mistakes.

 Eg: **!dndsage tiefling** 
 Eg2: **!dndsage armor -f shield** 
 Eg3: **!dndsage fight -f mounting**

  
## FLAGS:

> If command has <optional  flags> argument you can use flags bellow:

- "-s \<phrase>" - use this flag with !dndclass only, lets you see certain
subclass/maneuvers/invocations, depending on phrase you have given.
Eg: **!dndclass rogue -s arcane trickster** | It will show you info about rogue subclass - arcane trickster
- "-f \<phrase>" - use with any command where optional flags are available, bot will look for phrase you have given and will display only this content that is relevant to this phrase.
Eg: **!dndsage elf -f wood elf** | It will show you only information about wood elf, not whole elf race.
Eg2: **!dndsage paladin -f divine smite** | It will show you only Divine Smite feature, not whole paladin class

## Sources:
Answers are based on information from http://dnd5e.wikidot.com web page.

## Hosting:
Currently application is hosted on http://heroku.com server.

### Example for !dndspell Chaos bolt
```
Chaos Bolt - DND 5th Edition
Source: Xanathar's Guide to Everything 
1st-level evocation 
Casting Time: 1 action 
Range: 120 feet 
Components: V, S 
Duration: Instantaneous 

You hurl an undulating, warbling mass of chaotic energy at 
one creature in range. Make a ranged spell attack against the target. 
On a hit, the target takes 2d8 + 1d6 damage. Choose one of the d8s. 
The number rolled on that die determines the attack's damage 
type, as shown below.
    
╬═════════╬════════════════╬
║d8       ║Damage Type     ║
╬═════════╬════════════════╬
║1        ║Acid            ║
╬═════════╬════════════════╬
║2        ║Cold            ║
╬═════════╬════════════════╬
║3        ║Fire            ║
╬═════════╬════════════════╬
║4        ║Force           ║
╬═════════╬════════════════╬
║5        ║Lightning       ║
╬═════════╬════════════════╬
║6        ║Poison          ║
╬═════════╬════════════════╬
║7        ║Psychic         ║
╬═════════╬════════════════╬
║8        ║Thunder         ║
╬═════════╬════════════════╬

If you roll the same number on both d8s, the chaotic energy
leaps from the target to a different creature of your choice 
within 30 feet of it. Make a new attack roll against the new 
target, and make a new damage roll, which could cause the chaotic 
energy to leap again. A creature can be targeted only once by 
each casting of this spell. At Higher Levels. When you cast this 
spell using a spell slot of 2nd level or higher, each target takes 
1d6 extra damage of the type rolled for each slot level above 1st. 

Spell Lists. Sorcerer
```