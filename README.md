<h1 align="center" style="margin-top: -10px"> Wart </h1>
<p align="center" style="width: 100;">
   An open source purely functional interactive fiction framework, written in Python.<br>
</p>

### Intentions
A work in progress project I started for fun. Wart is for getting your narrative and input working, a front end could be built on top of it using other tools. Contributions are welcome so long as they make sense and do not bloat the project. See philosophy, CONTRIBUTING.md, and ROADMAP.md for more.  

> August 10th 2024: Since I haven't worked on this in over 9 months, I am archiving/closing this project. I've actually started to work on something similar to this but with a better approach, I'm not sure if it will end up on GitHub or not, because I have a game I want to make with it, and we'll see how that all goes. To any aspiring developers/game designers, feel free to use this project as inspiration or a basis for something if you wish.

> July 25th 2025: Made public domain.

### Philosophy
- Light
- Flexible
- Purely functional
- Complexity from simplicity
- No third party libraries/dependencies

## How to write stories
Create a file and write. It can be any file type as long as its contents are plain text. Wart is going to load the story from a folder, so you can write as many separate files as you want, and they will all be loaded together, if you'd like to separate chunks of the story, like chapters. Stories in Wart are told via *moments*, which is simply a block of text containing the parts.

A moment goes like this:
```
# troll
a troll blocks your path.
what do you do?
-
fight, kill = trollfightwin, trollfightlose
run, flee = runfromtroll
```

Where the moment's name is marked with a pound sign # followed by a space.
The narrative text goes underneath the moment's name. This can be multi-line, and as long as you want.
The narrative text ends with a single line containing a dash.
Under the narrative text goes a list of *links*. A single link consists of one list of terms that are acceptable, followed by an equals sign, followed by a list of moments that can be reached by using these terms. The reason for lists is because it allows the author to choose to be as simple or as complex as they want. If the user's input matches a term, the game will randomly choose from the list of moments equal to that term for that moment. You can make it only have one possibility by simply listing a specific moment, or there can be chances, by listing many moments. It's up to the author to use this to make things interesting. Wart automatically simplifies and sanitizes user input, so your terms in your links can be very simple such as "fight", "run", "climb", "open", etc.


## How to play
To play a game, simply create a python script that imports Wart.py, then `play(story directory, starting moment)`. See demo.py for how that looks. As stated above, this project isn't focused on the front end. The play function will simply run the game in your terminal of choice, but you can extend this to a custom front end if you want, there are lots of tools out there for doing this, such as Pygame.

## Credits
Written by telekrex.

## License
This project is released into the public domain. See the [LICENSE](LICENSE) file for details.