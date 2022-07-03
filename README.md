╬════════════════════════════════════════════════════════════════════════════════════════════════════╬
║ Ask mysterious sage a question about spells, feats, class and races features and backgrounds       ║
║ Wrtite !dndspell / !dndfeat / !dndclass / !dndbackground / !dndrace / !dndsage in your discord chat║
║ After that enter name of thing you want to find that matches choosen category                      ║
║ Use flags to add extra params to your question:                                                    ║
║ flag "-s <NAME>" to look for subclass, maneuvers or invocations                                    ║
║ flag "-f <NAME>" to search for given phrase                                                        ║
║ Eg: !dndspell fireball, !dndclass warlock -s eldritch invocations -f devil's sight                 ║
║ Eg: !dndclass fighter -s battle master -s maneuvers, !dndfeat sharpshooter                         ║
╬════════════════════════════════════════════════════════════════════════════════════════════════════╬

Write any of these commands bellow to ask our wise Sage a question about D&D mechanics
# COMMANDS:
"!dndhelp" - command used to show this panel
"!dndsage       <any phrase you want to search for> <optional flags>
"!dndclass      <class name>                        <optional flags>
"!dndrace       <race name>                         <optional flags>
"!dndspell      <spell name> 
"!dndfeat       <feat name> 
"!dndbackground <background name>
## Arguments
Instead of brackets in list aboe enter acording phrases you wish to see. Eg: Instead of: !dndfeat <feat name> write !dndfeat Chef or !dndfeat chef or any feat name, do simmilar with other commands
## FLAGS:
If command has <optional flags> argument you can use flags bellow:
"-s" <phrase> - use this flag with !dndclass only, lets you see certain subclass/maneuvers/invocations, depending on phrase you have given. Eg: !dndclass rouge -s arcane trickster | It will show you info about rouge subclass - arcane trickster
"-f" <phrase> - use with any command where optional flags are awalible, bot will look for phrase you have given and will display only this content that is relevant to this phrase. Eg: !dndsage elf -f wood elf | It will show you only information about wood elf, not whole elf race. Eg2: !dndsage paladin -f divine smite | It will show you only Divine Smite feature, not whole paladin class 

# TO DO LIST:
>spread table

@bot.command()
async def dndspell(ctx):
    """Documentation presumably"""
    //code