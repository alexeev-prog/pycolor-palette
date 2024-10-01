@mainfile
# PyColor-palette
This library is designed to display text using colors and formatting, as well as logging and debugging. Debugging is done using logger.

Used projects: [icecream source code](https://github.com/gruns/icecream) and [loguru module](https://github.com/Delgan/loguru)

## Install

```bash
pip3 install pycolor_palette-loguru
```

## Example

```python
#!venv/bin/python3
"""pycolor_palette Example File.

Copyright Alexeev Bronislav (C) 2024
"""
from loguru import logger
from pycolor_palette_loguru.logger import PyDBG_Obj, benchmark, set_default_theme, debug_func, setup_logger
from pycolor_palette_loguru.paint import info_message, warn_message, error_message, other_message, FG, Style, debug_message, run_exception
from pycolor_palette_loguru.pygments_colorschemes import CatppuccinMocha

set_default_theme(CatppuccinMocha)
pydbg_obj = PyDBG_Obj()
setup_logger('DEBUG')


@benchmark
@debug_func
def debug_print() -> list:
	num = 12
	float_int = 12.12
	string = 'Hello'
	boolean = True
	list_array = [1, 2, 3, 'Hi', True, 12.2]
	dictionary = {1: "HELLO", 2: "WORLD"}

	pydbg_obj(num, float_int, string, boolean, list_array, dictionary)


debug_print()
logger.debug("This is debug!")
logger.info("This is info!")
logger.warning("This is warning!")
logger.error("This is error!")

# Simple messages
info_message('INFORMATION')
warn_message('WARNING')
error_message('EXCEPTION')
debug_message('DEBUG')
other_message('SOME TEXT', 'OTHER')
# Highlight bg
info_message('Highlight INFORMATION', True)
warn_message('Highlight WARNING', True)
error_message('Highlight EXCEPTION', True)
debug_message('Highlight DEBUG', True)
other_message('Highlight SOME TEXT', 'OTHER', True)

print(f'{FG.red}{Style.bold}BOLD RED{Style.reset}{Style.dim} example{Style.reset}')

run_exception('EXCEPTION')
```
