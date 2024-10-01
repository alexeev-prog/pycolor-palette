# Правильный путь создания python-библиотеки: от создания до публикации
Привет, хабр! Стоит ли говорить, что Python ОЧЕНЬ и ОЧЕНЬ популярный язык программирования, местами даже догоняя JavaScript.

В мире программирования создание собственных библиотек - это не просто возможность пополнения своего портфолио или способ структурировать код, а настоящий акт творческого самовыражения (и иногда велосипедостроения). Каждый разработчик иногда использовал в нескольких своих проектах однообразный код, который приходилось каждый раз перемещать. Да и хотя-бы как упаковать свои идеи и знания в удобный и доступный формат, которым можно будет поделиться с сообществом.

Если вы ловили себя на мысли: "А почему мне бы не создать свою полноценную библиотеку?", то я рекомендую прочитать вам мою статью.

Эту статью вы можете использовать как шпаргалку для создания своих Python-библиотек. Я полностью расскажу все этапы создания библиотеки: документация, тестирование, архитектура, публикация и управление зависимостями

Некоторые из вас могут подумать что мы изобретаем велосипед. А я в ответ скажу - сможете ли вы прямо сейчас, без подсказок, только по памяти, нарисовать велосипед без ошибок?

---

Итак, как обычно начинается создание проектов на python? Банально создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

Но в этом проекте я решил отойти от такого способа, и использовать вместо этого систему правлению проектами Poetry. Poetry — это инструмент для управления зависимостями и сборкой пакетов в Python. А также при помощи Poetry очень легко опубликовать свою библиотеку на PyPi!

В Poetry представлен полный набор инструментов, которые могут понадобиться для детерминированного управления проектами на Python. В том числе, сборка пакетов, поддержка разных версий языка, тестирование и развертывание проектов.

Все началось с того, что создателю Poetry Себастьену Юстасу потребовался единый инструмент для управления проектами от начала до конца, надежный и интуитивно понятный, который бы мог использоваться и в рамках сообщества. Одного лишь менеджера зависимостей было недостаточно, чтобы управлять запуском тестов, процессом развертывания и всем созависимым окружением. Этот функционал находится за гранью возможностей обычных пакетных менеджеров, таких как Pip или Conda. Так появился Python Poetry.

Установить poetry можно через pipx: `pipx install poetry` и через pip: `pip install poetry --break-system-requirements`. Это установит poetry глобально во всю систему.

Итак, давайте создадим проект при помощи poetry и установим зависимости:

```bash
poetry new <имя_проекта>
cd <имя_проекта>
poetry shell
poetry add asttokens executing colorama rich ruff loguru pygments
```

# Структура проекта
В этой статье я буду создавать библиотеку pycolor_palette-loguru - простой модуль для различных цветных сообшений и дебага.

Вы можете посмотреть репозиторий по [ссылке](https://github.com/alexeev-prog/pycolor-palette).

Структуру проекта вы видите ниже:

```
.
├── docs/
├── example.py
├── poetry.lock
├── pycolor_palette_loguru
│   ├── __init__.py
│   ├── logger
│   │   ├── __init__.py
│   │   ├── logger.py
│   ├── paint.py
│   └── pygments_colorschemes.py
├── pyproject.toml
├── README.md
└── tests/
```

При использовании poetry, README.md, pyproject.toml, tests и директория вашей библиотеки (в моем случае pycolor_palette_loguru) будут созданы сами. poetry.lock - лок файл, также создается poetry.

Директория docs нужна для документации, tests для тестов.

Полная структура кода (из корня репозитория):

```
.
├── Doxyfile
├── LICENSE
├── pycolor-palette
│   ├── docs
│   │   └── ru
│   │       └── article.md
│   ├── example.py
│   ├── poetry.lock
│   ├── pycolor_palette_loguru
│   │   ├── __init__.py
│   │   ├── logger
│   │   │   ├── __init__.py
│   │   │   ├── logger.py
│   │   │   └── __pycache__
│   │   │       ├── __init__.cpython-312.pyc
│   │   │       └── logger.cpython-312.pyc
│   │   ├── paint.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── paint.cpython-312.pyc
│   │   │   └── pygments_colorschemes.cpython-312.pyc
│   │   └── pygments_colorschemes.py
│   ├── pyproject.toml
│   ├── README.md
│   └── tests
│       └── __init__.py
└── README.md
```

Итак, начнем работу над проектом с документации.

# Создание документации при помощи Doxygen
В этом разделе я расскажу о системе документирования исходных текстов Doxygen, которая на сегодняшний день, по имеющему основания заявлению разработчиков, стала фактически стандартом для документирования программного обеспечения, написанного на языке python, а также получила пусть и менее широкое распространение и среди ряда других языков.

Устанавливается Doxygen просто:

```bash
sudo pacman -S doxygen # Arch
sudo apt install doxygen # Ubuntu/Debian
```

Суть автоматизированного софта для генерации документации такая: на вход подаются файлы исходного кода, комментированные особым образом, а на выходе мы получаем структурированный формат документации.

Рассматриваемая система Doxygen как раз и выполняет эту задачу: она позволяет генерировать на основе исходного кода, содержащего комментарии специального вида, красивую и удобную документацию, содержащую в себе ссылки, диаграммы классов, вызовов и т.п. в различных форматах: HTML, LaTeX, CHM, RTF, PostScript, PDF, man-страницы.

В большинстве случаев Doxygen используется для документации программного обеспечения, написанного на языке C++, однако на самом деле данная система поддерживает гораздо большое число других языков: C, Objective-C, C#, PHP, Java, Python, IDL, Fortran, VHDL, Tcl, и частично D.

Итак, сначала нам нужно будет перейти в рабочую директорию и создать Doxyfile - файл конфигурации:

```bash
doxygen -g
```

В Doxyfile содержится краткое описание проекта, его версия и подобные вещи. Некоторые значения желательно сразу изменить.

Вот основные значения:

```bash
PROJECT_NAME           = "Project Name"             # Имя проекта
PROJECT_NUMBER         = 0.1.0                      # Версия проекта
PROJECT_BRIEF          = "Yet another project"      # Краткое описание проекта
OUTPUT_DIRECTORY       = docs                       # Куда складывать сгенерированную документацию
OUTPUT_LANGUAGE        = English                    # Язык документации
GENERATE_LATEX         = YES                        # Генерация LaTeX
INPUT                  = src include                # Директории, где искать файлы
RECURSIVE              = YES                        # Рекурсивный обход директорий
USE_MATHJAX            = YES                        # Использование mathjax (для latex в html)
```

 + PROJECT_NAME - название проекта.
 + PROJECT_NUMBER - версия проекта. Я придерживаюсь схемы "major.minor.patch".
 + PROJECT_BRIEF - краткое описание проекта.
 + OUTPUT_DIRECTORY - директория, куда будет записываться созданная документация.
 + OUTPUT_LANGUAGE - язык документации (доступные значения: Afrikaans, Arabic, Armenian, Brazilian, Bulgarian, Catalan, Chinese, Chinese-Traditional, Croatian, Czech, Danish, Dutch, English (United States), Esperanto, Farsi (Persian), Finnish, French, German, Greek, Hindi, Hungarian, Indonesian, Italian, Japanese, Japanese-en (Japanese with English messages), Korean, Korean-en (Korean with English messages), Latvian, Lithuanian, Macedonian, Norwegian, Persian (Farsi), Polish, Portuguese, Romanian, Russian, Serbian, Serbian-Cyrillic, Slovak, Slovene, Spanish, Swedish, Turkish, Ukrainian and Vietnamese).
 + GENERATE_LATEX - позволяет генерировать LaTeX.
 + INPUT - директории, откуда будет браться исходный код. Разделяются пробелами.
 + RECURSIVE - рекурсивный обход директорий.
 + USE_MATHJAX - для использования latex-формул в html.

Больше настроек вы можете посмотреть в [этой статье](https://habr.com/ru/articles/252443/).

## Кастомизация
Дефолтный стиль, мягко говоря, некрасивый. Поэтому мы будем использовать кастомную css-тему:

```bash
HTML_STYLESHEET        = ./docs/doxygen-styles.css # путь до css стилей
```

Данный файл стилей вы можете скачать [отсюда](https://raw.githubusercontent.com/jothepro/doxygen-awesome-css/refs/heads/main/doxygen-awesome.css).

Посмотреть, что получилось у меня, вы можете по [ссылке](https://alexeev-prog.github.io/pycolor-palette). А мой Doxyfile [здесь](https://github.com/alexeev-prog/pycolor-palette/blob/main/Doxyfile).

## Форма написания комментариев
Документация кода в Doxygen осуществляется при помощи документирующего блока. При этом существует два подхода к его размещению. Он может быть размещен перед или после объявления или определения класса, члена класса, функции, пространства имён и т.д.

Для того, чтобы doxygen правильно создал документацию, стоит следовать стилистике написания комментариев. Рассмотрим пример:

```python
def debug_message(text: str, highlight: bool=False) -> str:
	"""
	print debug message

	:param      text:       The text
	:type       text:       str
	:param      highlight:  The highlight
	:type       highlight:  bool

	:returns:   message
	:rtype:     str
	"""
	prefix = f'{BG.blue}{FG.black}' if highlight else f'{FG.blue}'
	message = '%s%-*s | %-*s%s ::: %s%s' % (prefix, 20, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
										20, 'DEBUG', Style.reset, text, Style.reset)
	print(message)
```

 + @brief - краткое описание
 + @details - детали, подробное описание
 + @todo - что-то нужно доделать. Doxygen генерирует отдельную страницу со списком всех @todo
 + @warning - предупреждение
 + @ref - ссылка на связанный класс или метод
 + @param - передаваемый параметр, имеет направление ([in], [out], [in,out])
 + @return - возвращаемое значение

Также мы можем использовать latex-формулы: чтобы обозначить ее, надо в начале и в конце вставить `\f$`. Для создания latex-формул можно использовать [онлайн редактор latex](https://latexeditor.lagrida.com/).

Также существуют следующие метки:

 + @authors - автор/ы
 + @version - версия
 + @date - дата
 + @bug - известные ошибки
 + @copyright - лицензия
 + @example - файл примера работы
 + @throws или @raise - исключение во время работы
 + @mainpage Title — комментарий содержит текст для титульного листа документации
 + @file fname — описание конкретного файла
 + @deprecated — помечает класс или метод устаревшим. Как и с @todo, Doxygen генерирует отдельную страницу со списком всех устаревших классов и методов

В действительности, Doxygen поддерживает куда больше команд. Например, он позволяет писать многостраничную (@page) документацию с разделами (@section) и подразделами (@subsection), указывать версии методов и классов (@version), и не только.

Больше можно прочитать [здесь](https://habr.com/ru/articles/252101/).

## Деплой документации на github-pages
Для начала создадим репозиторий на GitHub. Откройте главную вкладку репозитория.

![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/361/57b/b30/36157bb305d2cc9b52f0415fcc879917.png)

Перейдите на вкладку Settings и откройте раздел Pages:

![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/8ea/a5d/fd3/8eaa5dfd38f145a20fffe1dfb9d2dc8b.png)

В этом разделе выберете Static HTML и нажмите кнопку Configure.

![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/f8e/24b/40d/f8e24b40d0d63c69c3ab7b0aea39b16d.png)

Откроется файл конфигурации задачи для CI/CD пайплайна. Все настройки хранятся в static.yaml файле. С помощью пайплайна можно вызывать системные команды. Вызов всех команд описывается с помощью шагов. Описание шагов начинается после строки steps. Путь к этой строке: jobs -> deploy -> steps.

Первые два шага по умолчанию выглядят так:

![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/e27/cc2/ec7/e27cc2ec74ba9151ee5a074a427a4c94.png)

При обновлении GitHub Pages может что-то поменяться, но я не думаю, что будет сложно понять, где надо писать свои шаги.

Теперь требуется добавить шаги с установкой Doxygen. В качестве системы используется Ubuntu, а значит пакеты устанавливаются через apt.

```yml
# Install Doxygen
- name: Install Doxygen
  run: sudo apt install doxygen && doxygen --version
# Create documentation   
- name: Create documentation     
  run: doxygen
```

Документация создается, но надо ее развернуть. Для этого необходимо указать путь к папке с index.html в шаге Upload artifact. Путь к главной странице сайта: ./html/index.html. Тогда этот шаг будет выглядеть так:

![](https://habrastorage.org/r/w1560/getpro/habr/upload_files/c7e/5b5/8e4/c7e5b58e4b99d12b4eda29bc68839e71.png)

Я же указал в конфигурации Doxyfile, что документация сохраняется в docs, поэтому я указываю путь ./docs/html/index.html.

На этом настройка закончена. Ссылка на документацию находится в раздел Settings -> Pages. То есть `<username>.github.io/<reponame>`.

 > P.S. инструкция взята с [этой статье](https://habr.com/ru/articles/799051/)

# Тестирование
Не секрет, что разработчики создают программы, которые рано или поздно становятся очень масштабными (если смотреть на количество строчек кода). А с этим приходит и большая ответственность за качество.

В Python есть несколько библиотек для тестирования. В этой статье мы рассмотрим unittest и pytest.

Начнем с unittest, потому что именно с нее многие знакомятся с миром тестирования. Причина проста: библиотека по умолчанию встроена в стандартную библиотеку языка Python.

По формату написания тестов она сильно напоминает библиотеку JUnit, используемую  в языке Java для написания тестов:

 + тесты должны быть написаны в классе;
 + класс должен быть наследован от базового класса unittest.TestCase;
 + имена всех функций, являющихся тестами, должны начинаться с ключевого слова test;
 + внутри функций должны быть вызовы операторов сравнения (assertX) — именно они будут проверять наши полученные значения на соответствие заявленным.

 + Является частью стандартной библиотеки языка Python: не нужно устанавливать ничего дополнительно;
 + Гибкая структура и условия запуска тестов. Для каждого теста можно назначить теги, в соответствии с которыми будем запускаться либо одна, либо другая группа тестов;
 + Быстрая генерация отчетов о проведенном тестировании, как в формате plaintext, так и в формате XML.
 + Для проведения тестирования придётся написать достаточно большое количество кода (по сравнению с другими библиотеками);
 + Из-за того, что разработчики вдохновлялись форматом библиотеки JUnit, названия основных функций написаны в стиле camelCase (например setUp и assertEqual). В языке python согласно рекомендациям pep8 должен использоваться формат названий snake_case (например set_up и assert_equal).

Давайте я покажу код:

```python
from math import sqrt
import unittest


def square_it_up(num: float) -> float:
	"""
	square num

	:param      num:  The number
	:type       num:  float

	:returns:   value
	:rtype:     float
	"""
	return num ** 2



def square_eq_solver(a, b, c):
	"""
	решение квадратных уравнений

	:param      a:    a
	:type       a:    int/float
	:param      b:    b
	:type       b:    int/float
	:param      c:    c
	:type       c:    int/float

	:returns:   roots
	:rtype:     list
	"""
	result = []
	discriminant = b * b - 4 * a * c

	if discriminant == 0:
		result.append(-b / (2 * a))
	elif discriminant > 0:
		result.append((-b + sqrt(discriminant)) / (2 * a))
		result.append((-b - sqrt(discriminant)) / (2 * a))

	return result


class BasicTestCase(unittest.TestCase):
	def test_square_it_up(self):
		res = square_it_up(10)
		res2 = square_it_up(2)
		self.assertEqual(res, 100)
		self.assertEqual(res2, 4)


class SquareEqSolverTestCase(unittest.TestCase):
	def test_no_root(self):
		res = square_eq_solver(10, 0, 2)
		self.assertEqual(len(res), 0)

	def test_single_root(self):
		res = square_eq_solver(10, 0, 0)
		self.assertEqual(len(res), 1)
		self.assertEqual(res, [0])

	def test_multiple_root(self):
		res = square_eq_solver(2, 5, -3)
		self.assertEqual(len(res), 2)
		self.assertEqual(res, [0.5, -3])
```

Мы создали функции для возведения в квадрат и решения квадратного уравнения. Они как раз и будут тестироваться

Мы создаем классы Test Cases, которые наследуются от unittest.TestCase. Мы берем какое-либо значение с заданными параметрами и проверяем, совпадает ли оно с требованиями через функцию assertEqual().

Давайте запустим тесты через команду:

```bash
python3 -m unittest tests/unittest_example.py

....
----------------------------------------------------------------------
Ran 4 tests in 0.005s

OK
```

Отлично! Все получилось. Не будем задерживаться, перейдем к pytest. А документация по unittest [доступна по ссылке](https://docs.python.org/3/library/unittest.html).

---

Pytest позволяет провести модульное тестирование (тестирование отдельных компонентов программы), функциональное тестирование  (тестирование способности кода удовлетворять бизнес-требования), тестирование API (application programming interface) и многое другое.

Установить его при помощи poetry просто:

```bash
poetry add pytest
poetry install # если нужна установка
```

И его намного проще использовать чем unittest.

Рассмотрим наш прошлый пример, но уже с применением pytest:

```python
from math import sqrt


def square_it_up(num: float) -> float:
	"""
	square num

	:param      num:  The number
	:type       num:  float

	:returns:   value
	:rtype:     float
	"""
	return num ** 2



def square_eq_solver(a, b, c):
	"""
	решение квадратных уравнений

	:param      a:    a
	:type       a:    int/float
	:param      b:    b
	:type       b:    int/float
	:param      c:    c
	:type       c:    int/float

	:returns:   roots
	:rtype:     list
	"""
	result = []
	discriminant = b * b - 4 * a * c

	if discriminant == 0:
		result.append(-b / (2 * a))
	elif discriminant > 0:
		result.append((-b + sqrt(discriminant)) / (2 * a))
		result.append((-b - sqrt(discriminant)) / (2 * a))

	return result


def test_square_it_up():
	assert square_it_up(10) == 100


def test_no_root():
	assert len(square_eq_solver(10, 0, 2)) == 0


def test_single_root():
	assert len(square_eq_solver(10, 0, 0)) == 1


def test_multiple_root():
	assert square_eq_solver(2, 5, -3) == [0.5, -3]
```

Мы просто используем ключевое слово assert.

Запуск тестов также как и у unittest:

```bash
pytest tests/pytest_example.py

============================================================================= test session starts ==============================================================================
platform linux -- Python 3.12.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /home/alexeev/Desktop/Projects/pycolor-palette/pycolor-palette
configfile: pyproject.toml
collected 4 items

tests/pytest_example.py ....                                                                                                                                             [100%]

============================================================================== 4 passed in 0.13s ===============================================================================
```

Вот и все, что я хотел сказать о тестировании. Быстро, но базу рассказал. Документация по pytest [доступна по ссылке](https://docs.pytest.org/en/stable/contents.html).

# Пишем код
Как я уже говорил, моя библиотека-пример - это будет небольшой модуль для дебага и логгирования. Я брал [icecream source code](https://github.com/gruns/icecream) и использую loguru для логгинга.

В итоге, у нас получится такая библиотека (ниже пример кода):

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

А также вы ее можете сами установить через pip:

```bash
pip3 install pycolor_palette-loguru
```

И вы также сможете сделать! Так что не буду медлить, начнем творить!

## Цветные цвета
Итак, начнем с самого базового файла в нашей библиотеки - файле paint.py, которые отвечает за форматирование и цвет в терминале.

Вот сам код:

```python
#!/usr/bin/python3
from datetime import datetime
from sys import stdout, stdin
from time import sleep
import os


def cls():
	"""
	Clear screen (unix).
	"""
	os.system('clear')


class FG:
	"""
	Foreground class.
	"""

	black = "\u001b[30m"
	red = "\u001b[31m"
	green = "\u001b[32m"
	yellow = "\u001b[33m"
	blue = "\u001b[34m"
	magenta = "\u001b[35m"
	cyan = "\u001b[36m"
	white = "\u001b[37m"

	@staticmethod
	def rgb(r: int, g: int, b: int) -> str:
		"""
		Function for convert rgb to ansi color code.
		
		:param      r:    red color
		:type       r:    int
		:param      g:    green color
		:type       g:    int
		:param      b:    blue color
		:type       b:    int
		
		:returns:   color
		:rtype:     str
		"""
		return f"\u001b[38;2;{r};{g};{b}m"


class BG:
	"""
	Background class.
	"""

	black = "\u001b[40m"
	red = "\u001b[41m"
	green = "\u001b[42m"
	yellow = "\u001b[43m"
	blue = "\u001b[44m"
	magenta = "\u001b[45m"
	cyan = "\u001b[46m"
	white = "\u001b[47m"

	@staticmethod
	def rgb(r: int, g: int, b: int) -> str:
		"""
		Function for convert rgb to ansi color code.
		
		:param      r:    red color
		:type       r:    int
		:param      g:    green color
		:type       g:    int
		:param      b:    blue color
		:type       b:    int
		
		:returns:   color
		:rtype:     str
		"""
		return f"\u001b[48;2;{r};{g};{b}m"


class Style:
	"""
	Style class.
	"""

	reset = "\u001b[0m"
	bold = "\u001b[1m"
	dim = "\u001b[2m"
	italic = "\u001b[3m"
	underline = "\u001b[4m"
	reverse = "\u001b[7m"
	clear = "\u001b[2J"
	clearline = "\u001b[2K"
	up = "\u001b[1A"
	down = "\u001b[1B"
	right = "\u001b[1C"
	left = "\u001b[1D"
	nextline = "\u001b[1E"
	prevline = "\u001b[1F"
	top = "\u001b[0;0H"
	
	@staticmethod
	def to(x, y):
		"""
		Move cursor to x, y.
		
		:param      x:    x
		:type       x:    int
		:param      y:    y
		:type       y:    int
		
		:returns:   cursor
		:rtype:     string
		"""
		return f"\u001b[{y};{x}H"
	
	@staticmethod
	def write(text="\n"):
		"""
		Print to stdout.
		
		:param      text:  The text
		:type       text:  str
		"""
		stdout.write(text)
		stdout.flush()
	
	@staticmethod
	def writew(text="\n", wait=0.01):
		"""
		Print (typewrite effect).
		
		:param      text:  The text
		:type       text:  str
		:param      wait:  The wait
		:type       wait:  float
		"""
		for char in text:
			stdout.write(char)
			stdout.flush()
			sleep(wait)
  	
	@staticmethod
	def read(begin=""):
		"""
		Read input from keyboard.
		
		:param      begin:  The begin
		:type       begin:  str
		"""
		text = ""
		stdout.write(begin)
		stdout.flush()
		while True:
			char = ord(stdin.read(1))
      
		if char == 3: return
		elif char in (10, 13): return text
		else: text += chr(char)
	
	@staticmethod
	def readw(begin="", wait=0.5):
		"""
		Read input with wait.
		
		:param      begin:  The begin
		:type       begin:  str
		:param      wait:   The wait
		:type       wait:   float
		"""
		text = ""

		for char in begin:
			stdout.write(char)
			stdout.flush()
			sleep(wait)
		
		while True:
			char = ord(stdin.read(1))
      
			if char == 3: return
			elif char in (10, 13): return text
			else: text += chr(char)


def info_message(text: str, highlight: bool=False) -> str:
	"""
	print info message

	:param      text:       The text
	:type       text:       str
	:param      highlight:  The highlight
	:type       highlight:  bool

	:returns:   message
	:rtype:     str
	"""
	prefix = f'{BG.green}{FG.black}' if highlight else f'{FG.green}'
	message = '%s%-*s | %-*s%s ::: %s%s' % (prefix, 20, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
										20, 'INFO', Style.reset, text, Style.reset)
	print(message)


def warn_message(text: str, highlight: bool=False) -> str:
	"""
	print warn message

	:param      text:       The text
	:type       text:       str
	:param      highlight:  The highlight
	:type       highlight:  bool

	:returns:   message
	:rtype:     str
	"""
	prefix = f'{BG.yellow}{FG.black}' if highlight else f'{FG.yellow}'
	message = '%s%-*s | %-*s%s ::: %s%s' % (prefix, 20, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
										20, 'WARNING', Style.reset, text, Style.reset)
	print(message)


def error_message(text: str, highlight: bool=False) -> str:
	"""
	print error message

	:param      text:       The text
	:type       text:       str
	:param      highlight:  The highlight
	:type       highlight:  bool

	:returns:   message
	:rtype:     str
	"""
	prefix = f'{BG.red}{FG.black}' if highlight else f'{FG.red}'
	message = '%s%-*s | %-*s%s ::: %s%s' % (prefix, 20, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
										20, 'ERROR', Style.reset, text, Style.reset)
	print(message)


def debug_message(text: str, highlight: bool=False) -> str:
	"""
	print debug message

	:param      text:       The text
	:type       text:       str
	:param      highlight:  The highlight
	:type       highlight:  bool

	:returns:   message
	:rtype:     str
	"""
	prefix = f'{BG.blue}{FG.black}' if highlight else f'{FG.blue}'
	message = '%s%-*s | %-*s%s ::: %s%s' % (prefix, 20, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
										20, 'DEBUG', Style.reset, text, Style.reset)
	print(message)


def other_message(text: str, msg_type: str, highlight: bool=False) -> str:
	"""
	print message

	:param      text:       The text
	:type       text:       str
	:param      highlight:  The highlight
	:type       highlight:  bool

	:returns:   message
	:rtype:     str
	"""
	prefix = f'{BG.magenta}{FG.black}' if highlight else f'{FG.magenta}'
	message = '%s%-*s | %-*s%s ::: %s%s' % (prefix, 20, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
										20, msg_type, Style.reset, text, Style.reset)
	print(message)


def run_exception(text: str, highlight: bool=False):
	"""
	print and raise exception

	:param      text:       The text
	:type       text:       str
	:param      highlight:  The highlight
	:type       highlight:  bool

	:returns:   message
	:rtype:     str
	"""
	prefix = f'{BG.red}{FG.black}' if highlight else f'{FG.red}'
	message = '%s%s%-*s | %-*s ::: %s%s' % (Style.bold, prefix, 20, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
									20, "EXCEPTION", text, Style.reset)
	print(message)
	raise Exception(text)
```

Классы FG и BG отображают цвет текста и цвет фона (с возможностью передать цвет через RGB), а вот Style поинтереснее - форматирование, чтение ввода и управление курсорам. Также мы имеем функции для вывода красивых дебаг-сообщений:

```
2024-10-01 00:38:42  | INFO                 ::: INFORMATION
2024-10-01 00:38:42  | WARNING              ::: WARNING
2024-10-01 00:38:42  | ERROR                ::: EXCEPTION
2024-10-01 00:38:42  | DEBUG                ::: DEBUG
2024-10-01 00:38:42  | OTHER                ::: SOME TEXT
```

Мы используем форматирование через % для выравнивания текста. В начале дата, потом тип сообщения, а в конце текст сообщения. А `run_exception` вызывает исключение:

```
2024-10-01 00:38:42  | EXCEPTION            ::: EXCEPTION
Traceback (most recent call last):
  File "/home/alexeev/Desktop/Projects/pycolor-palette/pycolor-palette/example.py", line 50, in <module>
    run_exception('EXCEPTION')
  File "/home/alexeev/Desktop/Projects/pycolor-palette/pycolor-palette/pycolor_palette_loguru/paint.py", line 290, in run_exception
    raise Exception(text)
Exception: EXCEPTION
```

---

Итак, начнем писать код цветовых схем для будущего класса PyDBG_OBJ (вдохновлен библиотекой [icecream](https://github.com/gruns/icecream)) - этот класс нужен для более красивого и понятного дебага:

```
pydbg_obj | num: 12
            float_int: 12.12
            string: 'Hello'
            boolean: True
            list_array: [1, 2, 3, 'Hi', True, 12.2]
            dictionary: {1: 'HELLO', 2: 'WORLD'}
```

Но он также имеет подсветку синтаксиса. Для этого я использую pygments, и в коде я реализовал три цветовых схемы - Solarized, Catppuccin и Gruvbox.

Сначала импортируем токены и класс стиля

```python
from pygments.style import Style
from pygments.token import (
	Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
	Comment, Operator, Whitespace, Punctuation)
```

После создадим класс, наследуемый от Style:

```python
class SolarizedDark(Style):
	"""
	This class describes a solarized dark colorscheme.
	"""
	BASE03  = '#002b36' # noqa
	BASE02  = '#073642' # noqa
	BASE01  = '#586e75' # noqa
	BASE00  = '#657b83' # noqa
	BASE0   = '#839496' # noqa
	BASE1   = '#93a1a1' # noqa
	BASE2   = '#eee8d5' # noqa
	BASE3   = '#fdf6e3' # noqa
	YELLOW  = '#b58900' # noqa
	ORANGE  = '#cb4b16' # noqa
	RED     = '#dc322f' # noqa
	MAGENTA = '#d33682' # noqa
	VIOLET  = '#6c71c4' # noqa
	BLUE    = '#268bd2' # noqa
	CYAN    = '#2aa198' # noqa
	GREEN   = '#859900' # noqa

	styles = {
		Text:                   BASE0,
		Whitespace:             BASE03,
		Error:                  RED,
		Other:                  BASE0,

		Name:                   BASE1,
		Name.Attribute:         BASE0,
		Name.Builtin:           BLUE,
		Name.Builtin.Pseudo:    BLUE,
		Name.Class:             BLUE,
		Name.Constant:          YELLOW,
		Name.Decorator:         ORANGE,
		Name.Entity:            ORANGE,
		Name.Exception:         ORANGE,
		Name.Function:          BLUE,
		Name.Property:          BLUE,
		Name.Label:             BASE0,
		Name.Namespace:         YELLOW,
		Name.Other:             BASE0,
		Name.Tag:               GREEN,
		Name.Variable:          ORANGE,
		Name.Variable.Class:    BLUE,
		Name.Variable.Global:   BLUE,
		Name.Variable.Instance: BLUE,

		String:                 CYAN,
		String.Backtick:        CYAN,
		String.Char:            CYAN,
		String.Doc:             CYAN,
		String.Double:          CYAN,
		String.Escape:          ORANGE,
		String.Heredoc:         CYAN,
		String.Interpol:        ORANGE,
		String.Other:           CYAN,
		String.Regex:           CYAN,
		String.Single:          CYAN,
		String.Symbol:          CYAN,

		Number:                 CYAN,
		Number.Float:           CYAN,
		Number.Hex:             CYAN,
		Number.Integer:         CYAN,
		Number.Integer.Long:    CYAN,
		Number.Oct:             CYAN,

		Keyword:                GREEN,
		Keyword.Constant:       GREEN,
		Keyword.Declaration:    GREEN,
		Keyword.Namespace:      ORANGE,
		Keyword.Pseudo:         ORANGE,
		Keyword.Reserved:       GREEN,
		Keyword.Type:           GREEN,

		Generic:                BASE0,
		Generic.Deleted:        BASE0,
		Generic.Emph:           BASE0,
		Generic.Error:          BASE0,
		Generic.Heading:        BASE0,
		Generic.Inserted:       BASE0,
		Generic.Output:         BASE0,
		Generic.Prompt:         BASE0,
		Generic.Strong:         BASE0,
		Generic.Subheading:     BASE0,
		Generic.Traceback:      BASE0,

		Literal:                BASE0,
		Literal.Date:           BASE0,

		Comment:                BASE01,
		Comment.Multiline:      BASE01,
		Comment.Preproc:        BASE01,
		Comment.Single:         BASE01,
		Comment.Special:        BASE01,

		Operator:               BASE0,
		Operator.Word:          GREEN,

		Punctuation:            BASE0,
	}
```

Я не буду расписывать другие цветовые схемы и классы - если надо, вы можете просмотреть их [по этой ссылке](https://github.com/alexeev-prog/pycolor-palette/blob/main/pycolor-palette/pycolor_palette_loguru/pygments_colorschemes.py).

Перейдем к самому главному - директории logger/. Создадим в ней сразу `__init__.py`:

```python
from pycolor_palette_loguru.logger.logger import PyDBG_Obj, set_default_theme, benchmark, debug_func, setup_logger

__all__ = (set_default_theme, PyDBG_Obj, debug_func, benchmark, setup_logger)
```

И создадим файл logger.py. Именно в этом файле и будет центральный функционал.

Сначала нужно импортировать все нужные модули и библиотеки:

```python
from time import time
import ast
import inspect
import pprint
import sys
import warnings
from datetime import datetime
import functools
from contextlib import contextmanager
from os.path import basename, realpath
from textwrap import dedent
import colorama
import executing
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer as PyLexer, Python3Lexer as Py3Lexer
from typing import Union, List
import logging
from loguru import logger

# Написанные модули
from pycolor_palette_loguru.paint import debug_message
from pycolor_palette_loguru.pygments_colorschemes import *
```

Создадим несколько переменных и функцию для смены темы:

```python
PYTHON2 = (sys.version_info[0] == 2)

_absent = object()
default_theme = Terminal256Formatter(style=CatppuccinMocha)


def set_default_theme(theme):
	global default_theme
	default_theme = Terminal256Formatter(style=theme)
```

Функция set_default_theme позволяет задать новую тему подсветки кода.

Создадим класс и функцию, отвечающие за конфигурацию логгера loguru:

```python
class InterceptHandler(logging.Handler):
	"""
	This class describes an intercept handler.
	"""

	def emit(self, record) -> None:
		"""
		Get corresponding Loguru level if it exists

		:param      record:  The record
		:type       record:  record

		:returns:   None
		:rtype:     None
		"""
		try:
			level = logger.level(record.levelname).name
		except ValueError:
			level = record.levelno

		frame, depth = logging.currentframe(), 2

		while frame.f_code.co_filename == logging.__file__:
			frame = frame.f_back
			depth += 1

		logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger(level: Union[str, int] = 'DEBUG', ignored: List[str] = "") -> None:
	"""
	Setup logger

	:param      level:    The level
	:type       level:    str
	:param      ignored:  The ignored
	:type       ignored:  List[str]
	"""
	logging.basicConfig(
		handlers=[InterceptHandler()],
		level=logging.getLevelName(level)
	)

	for ignore in ignored:
		logger.disable(ignore)

	logger.info('Logging is successfully configured')
```

Функция setup_logger настраивает логгер. Кстати, loguru пользоваться очень просто:

```python
from loguru import logger

logger.info("info message")
```

Это будет независимо от файла, и будет распространяться на всю сессию.

Напишем некоторые базовые функции, которые пригодятся при выводе сообщений:

```python
@contextmanager
def supportTerminalColorsInWindows():
	"""
	Support terminal colors in Windows OS with colorama.
	"""
	colorama.init()
	yield
	colorama.deinit()


def stderrPrint(*args):
	"""
	Print to stderr.
	
	:param      args:  The arguments
	:type       args:  list
	"""
	print(*args)


def isLiteral(s):
	"""
	Check string if literal.
	
	:param      s:    string
	:type       s:    str
	
	:returns:   True if the specified s is literal, False otherwise.
	:rtype:     bool
	"""
	try:
		ast.literal_eval(s)
	except Exception:
		return False
	return True


def bindStaticVariable(name, value):
	def decorator(fn):
		"""
		Wrapper

		:param      fn:   The function
		:type       fn:   Function
		"""
		setattr(fn, name, value)
		return fn
	return decorator


@bindStaticVariable(
	'lexer', PyLexer(ensurenl=False) if PYTHON2 else Py3Lexer(ensurenl=False))
def colorize(s):
	"""
	Colorize with pygments.
	
	:param      s:    string
	:type       s:    str
	
	:returns:   highlighted
	:rtype:     str
	"""
	self = colorize
	return highlight(s, self.lexer, default_theme)
```

Теперь настроим базовые константы:

```python
DEFAULT_PREFIX = 'pydbg_obj | '
DEFAULT_LINE_WRAP_WIDTH = 80  # Characters.
DEFAULT_CONTEXT_DELIMITER = '~ '
DEFAULT_OUTPUT_FUNCTION = colorized_stderr_print
DEFAULT_ARG_TO_STRING_FUNCTION = pprint.pformat


NO_SOURCE_AVAILABLE_WARNING_MESSAGE = (
	'Failed to access the underlying source code for analysis. Was PyDBG_Obj() '
	'invoked in a REPL (e.g. from the command line), a frozen application '
	'(e.g. packaged with PyInstaller), or did the underlying source code '
	'change during execution?')
```

Напишем остальные вспомогательные функции:

```python
def colorized_stderr_print(obj):
	"""
	Colorized stderr print.
	
	:param      obj:  The object
	:type       obj:  object
	"""
	for s in obj.split('; '):
		if not s.startswith(f'{DEFAULT_PREFIX} |'):
			s = f'{DEFAULT_PREFIX} | {s}'
		colored = colorize(s)

		with supportTerminalColorsInWindows():
			stderrPrint(colored)


def callOrValue(obj):
	"""
	Call or value.
	
	:param      obj:  The object
	:type       obj:  obj
	
	:returns:   function
	:rtype:     func
	"""
	return obj() if callable(obj) else obj


class Source(executing.Source):
	"""
	Source.
	"""

	def get_text_with_indentation(self, node):
		"""
		Get text with indents.
		
		:param      node:  The node
		:type       node:  node asttokens
		
		:returns:   The text with indentation.
		"""
		result = self.asttokens().get_text(node)
		if '\n' in result:
			result = ' ' * node.first_token.start[1] + result
			result = dedent(result)
		result = result.strip()
		return result


def prefixLines(prefix, s, startAtLine=0):
	"""
	Prefix lines.
	
	:param      prefix:       The prefix
	:param      s:            { parameter_description }
	:param      startAtLine:  The start at line
	"""
	lines = s.splitlines()

	for i in range(startAtLine, len(lines)):
		lines[i] = prefix + lines[i]

	return lines


def prefixFirstLineIndentRemaining(prefix, s):
	"""
	First line indent remaining prefix.
	
	:param      prefix:  The prefix
	:type       prefix:  prefix
	:param      s:       param
	:type       s:       type
	
	:returns:   lines
	:rtype:     list
	"""
	indent = ' ' * len(prefix)
	lines = prefixLines(indent, s, startAtLine=1)
	lines[0] = prefix + lines[0]
	return lines


def formatPair(prefix, arg, value):
	"""
	Formatting pair.
	
	:param      prefix:  The prefix
	:param      arg:     The argument
	:param      value:   The value
	"""
	if arg is _absent:
		argLines = []
		valuePrefix = prefix
	else:
		argLines = prefixFirstLineIndentRemaining(prefix, arg)
		valuePrefix = argLines[-1] + ': '

	looksLikeAString = (value[0] + value[-1]) in ["''", '""']
	if looksLikeAString:  # Align the start of multiline strings.
		valueLines = prefixLines(' ', value, startAtLine=1)
		value = '\n'.join(valueLines)

	valueLines = prefixFirstLineIndentRemaining(valuePrefix, value)
	lines = argLines[:-1] + valueLines
	return '\n'.join(lines)


def singledispatch(func):
	"""
	Single dispatch function.
	
	:param      func:                 The function
	:type       func:                 function
	
	:returns:   func
	:rtype:     func
	
	:raises     NotImplementedError
	"""
	if "singledispatch" not in dir(functools):
		def unsupport_py2(*args, **kwargs):
			raise NotImplementedError(
				"functools.singledispatch is missing in " + sys.version
			)
		func.register = func.unregister = unsupport_py2
		return func

	func = functools.singledispatch(func)

	# add unregister based on https://stackoverflow.com/a/25951784
	closure = dict(zip(func.register.__code__.co_freevars, 
					   func.register.__closure__))
	registry = closure['registry'].cell_contents
	dispatch_cache = closure['dispatch_cache'].cell_contents
	def unregister(cls):
		del registry[cls]
		dispatch_cache.clear()
	func.unregister = unregister
	return func


@singledispatch
def argumentToString(obj):
	"""
	Convert argument to string.
	
	:param      obj:  The object
	:type       obj:  obj
	
	:returns:   String representation of the argument.
	:rtype:     string
	"""
	s = DEFAULT_ARG_TO_STRING_FUNCTION(obj)
	s = s.replace('\\n', '\n')  # Preserve string newlines in output.
	return s
```

И создадим главный класс - PyDBG_Obj:

```python
class PyDBG_Obj:
	"""Advanced print for debuging.
	
	>>> pydbg_obj | num: 12
					float_int: 12.12
					string: 'Hello'
					boolean: True
					list_array: [1, 2, 3, 'Hi', True, 12.2]
					dictionary: {1: 'HELLO', 2: 'WORLD'}
	
	"""

	_pairDelimiter = '; '
	lineWrapWidth = DEFAULT_LINE_WRAP_WIDTH
	contextDelimiter = DEFAULT_CONTEXT_DELIMITER

	def __init__(self, prefix=DEFAULT_PREFIX,
				 outputFunction=DEFAULT_OUTPUT_FUNCTION,
				 argToStringFunction=argumentToString, includeContext=False,
				 contextAbsPath=False):
		"""
		Initialization.
		
		:param      prefix:               The prefix
		:type       prefix:               prefix
		:param      outputFunction:       The output function
		:type       outputFunction:       output function
		:param      argToStringFunction:  The argument to string function
		:type       argToStringFunction:  function
		:param      includeContext:       The include context
		:type       includeContext:       bool
		:param      contextAbsPath:       The context absolute path
		:type       contextAbsPath:       bool
		"""
		self.enabled = True
		self.prefix = prefix
		self.includeContext = includeContext
		self.outputFunction = outputFunction
		self.argToStringFunction = argToStringFunction
		self.contextAbsPath = contextAbsPath

	def __call__(self, *args):
		"""
		Call magic method.
		
		:param      args:  The arguments
		:type       args:  list
		
		:returns:   passthrough
		:rtype:     list
		"""
		if self.enabled:
			callFrame = inspect.currentframe().f_back
			self.outputFunction(self._format(callFrame, *args))

		if not args:
			passthrough = None
		elif len(args) == 1:
			passthrough = args[0]
		else:
			passthrough = args

		return passthrough

	def format(self, *args):
		"""
		Format arguments.
		
		:param      args:  The arguments
		:type       args:  list
		
		:returns:   formatted out
		:rtype:     call frame formatted
		"""
		callFrame = inspect.currentframe().f_back
		out = self._format(callFrame, *args)
		return out

	def _format(self, callFrame, *args):
		"""
		Format helper function.
		
		:param      callFrame:  The call frame
		:type       callFrame:  call frame
		:param      args:       The arguments
		:type       args:       list
		
		:returns:   formatted
		:rtype:     formatted out
		"""
		prefix = callOrValue(self.prefix)

		context = self._formatContext(callFrame)
		if not args:
			time = self._formatTime()
			out = prefix + context + time
		else:
			if not self.includeContext:
				context = ''
			out = self._formatArgs(
				callFrame, prefix, context, args)

		return out

	def _formatArgs(self, callFrame, prefix, context, args):
		"""
		Format arguments.
		
		:param      callFrame:  The call frame
		:type       callFrame:  call frame
		:param      prefix:     The prefix
		:type       prefix:     prefix
		:param      context:    The context
		:type       context:    content
		:param      args:       The arguments
		:type       args:       args
		
		:returns:   formatted args
		:rtype:     args
		"""
		callNode = Source.executing(callFrame).node
		if callNode is not None:
			source = Source.for_frame(callFrame)
			sanitizedArgStrs = [
				source.get_text_with_indentation(arg)
				for arg in callNode.args]
		else:
			warnings.warn(
				NO_SOURCE_AVAILABLE_WARNING_MESSAGE,
				category=RuntimeWarning, stacklevel=4)
			sanitizedArgStrs = [_absent] * len(args)

		pairs = list(zip(sanitizedArgStrs, args))

		out = self._constructArgumentOutput(prefix, context, pairs)
		return out

	def _constructArgumentOutput(self, prefix, context, pairs):
		"""
		Construct argument output.
		
		:param      prefix:   The prefix
		:type       prefix:   prefix
		:param      context:  context
		:type       context:  context
		:param      pairs:    The pairs
		:type       pairs:    pairs
		
		:returns:   argument output
		:rtype:     string
		"""
		def argPrefix(arg):
			return '%s: ' % arg

		pairs = [(arg, self.argToStringFunction(val)) for arg, val in pairs]
		pairStrs = [
			val if (isLiteral(arg) or arg is _absent)
			else (argPrefix(arg) + val)
			for arg, val in pairs]

		allArgsOnOneLine = self._pairDelimiter.join(pairStrs)
		multilineArgs = len(allArgsOnOneLine.splitlines()) > 1

		contextDelimiter = self.contextDelimiter if context else ''
		allPairs = prefix + context + contextDelimiter + allArgsOnOneLine
		firstLineTooLong = len(allPairs.splitlines()[0]) > self.lineWrapWidth

		if multilineArgs or firstLineTooLong:
			if context:
				lines = [prefix + context] + [
					formatPair(len(prefix) * ' ', arg, value)
					for arg, value in pairs
				]
			else:
				argLines = [
					formatPair('', arg, value)
					for arg, value in pairs
				]
				lines = prefixFirstLineIndentRemaining(prefix, '\n'.join(argLines))
		else:
			lines = [prefix + context + contextDelimiter + allArgsOnOneLine]

		return '\n'.join(lines)

	def _formatContext(self, callFrame):
		"""
		Function for format call frame.
		
		:param      callFrame:  callframe
		:type       callFrame:  call frame
		
		:returns:   context
		:rtype:     string
		"""
		filename, lineNumber, parentFunction = self._getContext(callFrame)

		if parentFunction != '<module>':
			parentFunction = '%s()' % parentFunction

		context = f'{filename}:{lineNumber} in {parentFunction}'
		return context

	def _formatTime(self):
		"""
		Function for format time.
		
		:returns:   format time
		:rtype:     str
		"""
		now = datetime.now()
		formatted = now.strftime('%H:%M:%S.%f')[:-3]
		return ' at %s' % formatted

	def _getContext(self, callFrame):
		"""
		Get context of call frame.
		
		:param      callFrame:  The call frame
		:type       callFrame:  callFrame
		
		:returns:   The context.
		:rtype:     context
		"""
		frameInfo = inspect.getframeinfo(callFrame)
		lineNumber = frameInfo.lineno
		parentFunction = frameInfo.function

		filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
		return filepath, lineNumber, parentFunction

	def enable(self):
		"""
		Enable pydbg_obj.
		"""
		self.enabled = True

	def disable(self):
		"""
		Disable pydbg_obj.
		"""
		self.enabled = False

	def configureOutput(self, prefix=_absent, outputFunction=_absent,
						argToStringFunction=_absent, includeContext=_absent,
						contextAbsPath=_absent):
		"""
		Configure output of pydbg_obj.
		
		:param      prefix:               The prefix
		:type       prefix:               prefix
		:param      outputFunction:       The output function
		:type       outputFunction:       output function
		:param      argToStringFunction:  The argument to string function
		:type       argToStringFunction:  arg to string function
		:param      includeContext:       The include context
		:type       includeContext:       include context
		:param      contextAbsPath:       The context absolute path
		:type       contextAbsPath:       context abs path
		
		:raises     TypeError:            no parameter provided
		"""
		noParameterProvided = all(
			v is _absent for k,v in locals().items() if k != 'self')
		if noParameterProvided:
			raise TypeError('configureOutput() missing at least one argument')

		if prefix is not _absent:
			self.prefix = prefix

		if outputFunction is not _absent:
			self.outputFunction = outputFunction

		if argToStringFunction is not _absent:
			self.argToStringFunction = argToStringFunction

		if includeContext is not _absent:
			self.includeContext = includeContext
		
		if contextAbsPath is not _absent:
			self.contextAbsPath = contextAbsPath
```

И напишем две функции-декоратора, первая отвечает за сообщение об исполнении функции, вторая нужна для высчитывания скорости выполнения функции:

```python
def debug_func(func, *args, **kwargs):
	"""Decorator for print info about function.

	Arguments:
	---------
	+ func - executed func

	"""
	def wrapper():
		func(*args, **kwargs)
	message = f'debug @ Function {func.__name__}() executed at {datetime.now()}'
	debug_message(message, False)
	return wrapper


def benchmark(func, *args, **kwargs):
	"""Measuring the speed of function execution (decorator).

	Arguments:
	---------
	+ func - executed func

	"""
	start = time()
	def wrapper():
		func(*args, **kwargs)
	end = time()
	total = round(end - start, 2)
	debug_message(f'benchmark {func} @ Execution function {func.__name__} time: {total} sec', True)
	return wrapper
```

И это весь код на данный момент.

В итоге структура проекта такова:

```
.
├── example.py
├── poetry.lock
├── pycolor_palette_loguru
│   ├── __init__.py
│   ├── logger
│   │   ├── __init__.py
│   │   ├── logger.py
│   ├── paint.py
│   └── pygments_colorschemes.py
├── pyproject.toml
├── README.md
└── tests
    ├── pytest_example.py
    └── unittest_example.py
```

## Ruff
[Ruff](https://pypi.org/project/ruff/) — это новый быстроразвивающийся линтер Python-кода, призванный заменить flake8 и isort.

Основным преимуществом Ruff является его скорость: он в 10–100 раз быстрее аналогов (линтер написан на Rust).

Ruff может форматировать код, например, автоматически удалять неиспользуемые импорты. Сортировка и группировка строк импорта практически идентична isort.

Инструмент используется во многих популярных open-source проектах, таких как FastAPI и Pydantic.

Настройка Ruff осуществляется в файле pyproject.toml.

Для использования ruff как линтер можно использовать следующие команды:

```bash
ruff check                          # Lint all files in the current directory (and any subdirectories).
ruff check path/to/code/            # Lint all files in `/path/to/code` (and any subdirectories).
ruff check path/to/code/*.py        # Lint all `.py` files in `/path/to/code`.
ruff check path/to/code/to/file.py  # Lint `file.py`.
ruff check @arguments.txt           # Lint using an input file, treating its contents as newline-delimited command-line arguments.
ruff check . --fix 					# Lint all files in current directory and fix
```

А если как форматтер:

```bash
ruff format                          # Format all files in the current directory (and any subdirectories).
ruff format path/to/code/            # Format all files in `/path/to/code` (and any subdirectories).
ruff format path/to/code/*.py        # Format all `.py` files in `/path/to/code`.
ruff format path/to/code/to/file.py  # Format `file.py`.
ruff format @arguments.txt           # Format using an input file, treating its contents as newline-delimited command-line arguments.
ruff format .						 # Format all files in current directory
```

Для конфигурации ruff'а просто можно изменить файл pyproject.toml (созданный poetry):

```toml
# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]

# Same as Black.
line-length = 88
indent-width = 4

# Assume Python 3.8
target-version = "py38"

[lint]
# Enable Pyflakes (`F`) and a subset of the pycodestyle (`E`)  codes by default.
select = ["E4", "E7", "E9", "F"]
ignore = []

# Allow fix for all enabled rules (when `--fix`) is provided.
fixable = ["ALL"]
unfixable = []

# Allow unused variables when underscore-prefixed.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[format]
# Like Black, use double quotes for strings.
quote-style = "double"

# Like Black, indent with spaces, rather than tabs.
indent-style = "space"

# Like Black, respect magic trailing commas.
skip-magic-trailing-comma = false

# Like Black, automatically detect the appropriate line ending.
line-ending = "auto"
```

## Финальные штрихи
Создадим файл `__init__.py` в директории модуля. Этот файл отвечает за инициализацию модуля.

```python
from pycolor_palette_loguru.logger import PyDBG_Obj, benchmark, set_default_theme, debug_func, setup_logger
from pycolor_palette_loguru.paint import info_message, warn_message, error_message, other_message, FG, Style, debug_message, run_exception, BG
from pycolor_palette_loguru.pygments_colorschemes import CatppuccinMocha, SolarizedDark, GruvboxDark

__all__ = (PyDBG_Obj, benchmark, set_default_theme, debug_func, setup_logger, 
	  info_message, error_message, other_message, FG, Style, BG, debug_message, run_exception, BG,
	  CatppuccinMocha, SolarizedDark, GruvboxDark)
```

# Публикация на PyPi
[PyPi](https://pypi.org/) — официальный репозиторий Python для загрузки и скачивания пакетов. Это официальный ресурс пакетов для третьих лиц, которым управляет Python Software Foundation. После публикации на PyPI пакеты становятся доступными для установки.

Итак, вам потребуется аккаунт на PyPi. Зарегистрироваться можно по [этой ссылке](https://pypi.org/account/register/).

![](https://habrastorage.org/webt/iv/ju/c6/ivjuc67v8hrnfajqltuyxzfp5my.png)

Дальше вам нужно будет подключить 2FA для безопасности аккаунта:

![](https://habrastorage.org/webt/li/do/ma/lidomausio9jkpwvcpmeio1tove.png)

Аутентификация с помощью токена — это рекомендуемый способ проверки учетной записи PyPI в командной строке. При этом вместо имени пользователя и пароля можно использовать автоматически сгенерированный токен. Токены можно добавлять и отзывать в любое время; с их помощью можно предоставлять доступ к отдельным частям вашей учетной записи. Это делает их безопасными и значительно уменьшает риск взлома. Теперь создадим новый API-токен для учетной записи, для этого перейдите в настройки учетной записи:

![](https://habrastorage.org/webt/op/h2/qa/oph2qasaxymwfi46q5qkbde7eq8.png)

Прокрутите вниз и найдите раздел “API tokens”. Нажмите “Add API token”:

![](https://habrastorage.org/webt/jh/e7/ck/jhe7ck4yjhigmhqfxixb6whfodc.png)

Теперь с помощью этого токена можно настроить свои учетные данные в Poetry для подготовки к публикации. Чтобы не добавлять свой API токен к каждой команде, которой он нужен в Poetry, мы сделаем это один раз с помощью команды config:

```
poetry config pypi-token.pypi your-api-token
```

Добавленный API токен будет использоваться как учетные данные. Poetry уведомит о том, что ваши учетные данные хранятся в простом текстовом файле. Если использовать обычное имя пользователя и пароль для учетных данных, то это будет небезопасно. Хранение токенов безопасно и удобно, так как они легко удаляются, обновляются и генерируются случайным образом. Но также можно вводить свой API токен вручную для каждой команды.

Далее нам нужно будет собрать и опубликовать пакет через команды:

```bash
poetry build
poetry publish
```

Если на этапе публикации выяснилось, что имя проекта занято, то измените в файле pyproject.toml название проекта, а далее согласно ему измените директорию модуля, и заново запустите сборку и публикацию.

Вы можете просмотреть свои созданные проекты [по ссылке](https://pypi.org/manage/projects/).

В итоге, кстати, мой pyproject.toml получился такой:

```toml
[tool.poetry]
name = "pycolor_palette-loguru"
version = "0.1.2"
description = "Python library for color beautiful output and logging"
authors = ["Alexeev Bronislav <alexeev.dev@inbox.ru>"]
readme = "README.md"

[project]
name = "pycolor_palette-loguru"
description = "Python library for color beautiful output and logging"
readme = "README.md"
requires-python = ">=3.9"
keywords = ["color", 'icecream', 'loguru', 'logging', 'pycolor', "palette"]
license = {text = "MIT License"}
dynamic = ["version"]

[tool.poetry.dependencies]
python = "^3.12"
rich = "^13.8.1"
ruff = "^0.6.8"
loguru = "^0.7.2"
pygments = "^2.18.0"
colorama = "^0.4.6"
executing = "^2.1.0"
asttokens = "^2.4.1"
pytest = "^8.3.3"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]

# Same as Black.
line-length = 88
indent-width = 4

# Assume Python 3.8
target-version = "py38"

[lint]
# Enable Pyflakes (`F`) and a subset of the pycodestyle (`E`)  codes by default.
select = ["E4", "E7", "E9", "F"]
ignore = []

# Allow fix for all enabled rules (when `--fix`) is provided.
fixable = ["ALL"]
unfixable = []

# Allow unused variables when underscore-prefixed.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[format]
# Like Black, use double quotes for strings.
quote-style = "double"

# Like Black, indent with spaces, rather than tabs.
indent-style = "space"

# Like Black, respect magic trailing commas.
skip-magic-trailing-comma = false

# Like Black, automatically detect the appropriate line ending.
line-ending = "auto"
```

# Заключение
Репозиторий исходного кода доступен по [ссылке](https://github.com/alexeev-prog/pycolor-palette).

Буду рад, если вы присоединитесь к моему небольшому [телеграм-блогу](https://t.me/hex_warehouse). Анонсы статей, новости из мира IT и полезные материалы для изучения программирования и смежных областей.

Надеюсь, вам понравилась данная статья.

## Источники
 + [Doxygen / eax.me](https://eax.me/doxygen/)
 + [Автодокументация Doxygen и ее публикация на Github Pages](https://habr.com/ru/articles/799051/)
 + [Учимся тестировать на python](https://tproger.ru/articles/testiruem-na-python-unittest-i-pytest-instrukcija-dlja-nachinajushhih)
