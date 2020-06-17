# super3 - Make your super Python super() calls super!

Upgraded a Python 2 codebase? Old habits when typing super?

Remove class names and `self`/`cls` from super() calls when they are not needed.

## Install

```
pip install super3
```

## Usage

View all the old-style super calls with `--list`. 

```
super3 --list path/to/code
```

## Recommended Usage

1. Only run against code you have version controlled or otherwise backed up
2. After running super3, use Black or another automatic formatter to make things
   look good. super3 is super focused and super simple, we don't try to do any
   more than is needed.

Okay, got that? Then run the command with no flags to make the change.

```
super3 path/to/code
```
