# 2D Minecraft Clone <img src="https://raw.githubusercontent.com/kadir014/2d-minecraft-clone/main/src/assets/logoheight.png" alt="logo" width="43"/>
<p>
  <img src="https://img.shields.io/badge/python-3.9%2B-green">
  <img src="https://img.shields.io/badge/pygame-2.1%2B-green">
  <img src="https://img.shields.io/badge/moderngl-5.6%2B-green">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img src="https://img.shields.io/badge/version-0.0.0-orange">
</p>

This is a 2D clone of the well-known game Minecraft made in Python using [Pygame](https://github.com/pygame/pygame) and [ModernGL](https://github.com/moderngl/moderngl) \
I started this mostly as a self-improvement project to learn new concepts like procuderal terrain generation, handling infinite worlds with chunks, different lighting techniques and scenarios in a tile-based system etc...

## Installing & Running
Currently the game has no release binaries because of it being in its early stages, you can follow the steps below to install and run the game from source

### Windows
You need to have Python version 3.9 or above
- Download the `src` folder (or extract it from the repo clone archive)
- Install the dependencies
```
python -m pip install pygame>=2.1
```
```
python -m pip install moderngl>=5.6
```
- Run the entry script
```
python "C:\...\main.py"
```

### Linux & Unix
You need to have Python version 3.9 or above
- Download the `src` folder (or extract it from the repo clone archive)
- Install the dependencies
```
python3 -m pip install pygame>=2.1
```
```
python3 -m pip install moderngl>=5.6
```
- Run the entry script
```
python3 "/.../main.py"
```

## Controls
Here is the default input scheme until I get the input options in the game available \
<kbd>A</kbd>, <kbd>D</kbd> to move left, right \
<kbd>W</kbd> or <kbd>SPACE</kbd> to jump \
<kbd>SHIFT</kbd> to crouch \
<kbd>LMB</kbd> to break blocks \
<kbd>RMB</kbd> to place blocks \
<kbd>F3</kbd> to toggle display debug screen \
<kbd>L</kbd> to toggle lighting

## License
[MIT](LICENSE) © Kadir Aksoy