# Neovim config для Windows 11

Русский | [English](README_en.md)

Конфигурация Neovim 0.12 для Windows 11: разработка на Python, Rust и PowerShell, заметки в Markdown, документы в LaTeX и локальный ИИ-помощник на Ollama. Всё работает без облачных сервисов.

## Что внутри

| Область | Что используется |
|---|---|
| Менеджер плагинов | [lazy.nvim](https://github.com/folke/lazy.nvim) |
| Подсветка кода | nvim-treesitter (парсеры Lua, Python, Rust) |
| Автодополнение | blink.cmp |
| Поиск файлов и текста | Telescope (+ ripgrep) |
| Файловое дерево | nvim-tree + nvim-web-devicons |
| Тема | tokyonight |
| ИИ-помощник | codecompanion.nvim + Ollama |
| Markdown | render-markdown.nvim |
| LaTeX | VimTeX (latexmk, XeLaTeX) |
| Установка серверов | mason.nvim (texlab, marksman) |

### Языковые серверы (LSP)

| Язык | Сервер | Как устанавливается |
|---|---|---|
| Python | Pyright | `npm install -g pyright` |
| Rust | rust-analyzer | `rustup component add rust-analyzer` |
| PowerShell | PowerShell Editor Services | архив с GitHub, распаковывается в `nvim-data/pses` |
| Markdown | Marksman | через Mason |
| LaTeX | texlab | через Mason |

### ИИ-помощник

Работает локально. Модель `qwen2.5-coder:7b` через Ollama, контекст 16384 токена (около 5,5 ГБ видеопамяти), модель остаётся в памяти 30 минут. Для видеокарты с меньшим объёмом памяти уменьши `num_ctx` в `lua/config/lazy.lua` до 8192.

## Клавиши

Главная клавиша (`leader`): пробел.

| Клавиши | Действие |
|---|---|
| `jk` (режим вставки) | Выход в обычный режим |
| `Ctrl+p` | Поиск файла по имени |
| `Ctrl+f` | Поиск текста по всем файлам |
| `Ctrl+n` | Файловое дерево |
| `gd` | Перейти к определению |
| `Ctrl+y` | Принять вариант автодополнения |
| Пробел `a` | Открыть и закрыть чат с ИИ |
| Пробел `c` (в выделении) | Отправить выделенный код в чат |
| Пробел `i` | Правка кода по запросу (`g2` принять, `g3` отклонить) |

В файлах LaTeX работают стандартные сочетания VimTeX (локальная клавиша `\`): `\ll` запускает и останавливает сборку, `\lv` открывает PDF, `\le` показывает ошибки, `\lc` очищает служебные файлы.

## Структура

```text
nvim/
├── init.lua
├── lazy-lock.json
├── LICENSE
├── README.md / README_en.md
├── lua/
│   └── config/
│       ├── lazy.lua      # плагины
│       ├── lsp.lua       # языковые серверы
│       └── options.lua   # настройки и клавиши
├── docs/                 # инструкции и шпаргалка (md и двуязычные PDF)
└── tools/
    └── tex2md.py         # получает md-файлы из .tex-исходников
```

`lazy-lock.json` фиксирует версии плагинов, поэтому на другом компьютере всё ставится ровно в тех версиях, с которыми конфиг проверен.

## Документация

Подробные инструкции лежат в папке [`docs`](docs). У каждой есть версия на русском, на английском и двуязычный PDF (русский слева, английский справа).

| Документ | Русский | English | PDF |
|---|---|---|---|
| Установка и настройка Neovim с нуля | [md](docs/install-neovim_ru.md) | [md](docs/install-neovim_en.md) | [pdf](docs/install-neovim_ru-en.pdf) |
| Дополнительно: Markdown и LaTeX | [md](docs/install-markdown-latex_ru.md) | [md](docs/install-markdown-latex_en.md) | [pdf](docs/install-markdown-latex_ru-en.pdf) |
| Шпаргалка: клавиши и команды | [md](docs/cheatsheet-neovim_ru.md) | [md](docs/cheatsheet-neovim_en.md) | [pdf](docs/cheatsheet-neovim_ru-en.pdf) |

Исходники документов — файлы `docs/*_ru-en.tex`. Файлы `.md` из них генерируются: после правки `.tex` выполните `python tools/tex2md.py` и пересоберите PDF (`latexmk -xelatex docs/имя_ru-en.tex`).

## Требования

- Windows 11, Windows Terminal.
- [Neovim](https://neovim.io) 0.12 и Git.
- Python 3.12, Node.js, Rust (`rustup`).
- `ripgrep`, `tree-sitter-cli`, компилятор C (для сборки парсеров Treesitter).
- Шрифт JetBrainsMono Nerd Font, выбранный в настройках Windows Terminal (иначе вместо значков будут ромбики).
- [MiKTeX](https://miktex.org) для LaTeX (в нём `latexmk` и `xelatex`) и [Strawberry Perl](https://strawberryperl.com): `latexmk` написан на Perl, а MiKTeX его не содержит.
- [Ollama](https://ollama.com) и модель `qwen2.5-coder:7b`.

## Установка (кратко)

Полная пошаговая версия: [docs/install-neovim_ru.md](docs/install-neovim_ru.md).

1. Установи программы из раздела «Требования».
2. Клонируй конфиг. Если папка `nvim` уже есть, сначала переименуй её.

   ```powershell
   git clone <адрес этого репозитория> $env:LOCALAPPDATA/nvim
   ```

3. Запусти `nvim`. lazy.nvim сам скачает плагины, дождись окончания и закрой окно клавишей `q`.
4. Установи парсеры: `:TSInstall lua python rust`.
5. Установи серверы из таблицы выше: Pyright, rust-analyzer, PowerShell Editor Services, а также `:MasonInstall texlab marksman`.
6. Скачай модель: `ollama pull qwen2.5-coder:7b`.
7. Проверь, что всё в порядке: `:checkhealth`.

Серверы, Mason-пакеты, модели Ollama и сами плагины в репозиторий не входят, их нужно ставить на каждом компьютере заново.

## Особенности и ограничения

- **PowerShell.** Сервер запускается через встроенный Windows PowerShell 5.1 (`powershell`), потому что PowerShell 7 из Microsoft Store Neovim запустить не может.
- **LaTeX и Perl.** Без Perl сборка (`\ll`) падает с ошибкой «could not find the script engine perl». Подробности в [инструкции по Markdown и LaTeX](docs/install-markdown-latex_ru.md).
- **LaTeX и кириллица.** Сборка идёт через XeLaTeX. Для русского текста в документе нужно указать установленный шрифт с кириллицей (проверено: Times New Roman). Просмотр PDF открывается в программе Windows по умолчанию.
- **Русская раскладка.** Команды обычного режима при включённой русской раскладке не работают, отдельная настройка раскладки не добавлена.
- **Punto Switcher.** Если он установлен, добавь Windows Terminal в «Программы-исключения», иначе он переключает раскладку и ломает команды.
- **Локальная модель.** Модель на 7 миллиардов параметров хорошо справляется с короткими вопросами и мелкими правками, но слабее облачных моделей на сложных задачах. Результат правок стоит просматривать.
- Плагин для интеграции с Obsidian (`obsidian.nvim`) не используется: Markdown-файлы хранилища можно открывать и править напрямую.

## Лицензия

[MIT](LICENSE): конфиг можно свободно использовать, копировать и изменять, в том числе в своих проектах.





# Neovim config for Windows 11

[Русский](README.md) | English

A Neovim 0.12 configuration for Windows 11: Python, Rust and PowerShell development, Markdown notes, LaTeX documents and a local AI assistant on Ollama. Everything works without cloud services.

## What's inside

| Area | What is used |
|---|---|
| Plugin manager | [lazy.nvim](https://github.com/folke/lazy.nvim) |
| Syntax highlighting | nvim-treesitter (Lua, Python, Rust parsers) |
| Autocompletion | blink.cmp |
| File and text search | Telescope (+ ripgrep) |
| File tree | nvim-tree + nvim-web-devicons |
| Theme | tokyonight |
| AI assistant | codecompanion.nvim + Ollama |
| Markdown | render-markdown.nvim |
| LaTeX | VimTeX (latexmk, XeLaTeX) |
| Server installer | mason.nvim (texlab, marksman) |

### Language servers (LSP)

| Language | Server | How it is installed |
|---|---|---|
| Python | Pyright | `npm install -g pyright` |
| Rust | rust-analyzer | `rustup component add rust-analyzer` |
| PowerShell | PowerShell Editor Services | archive from GitHub, unpacked into `nvim-data/pses` |
| Markdown | Marksman | via Mason |
| LaTeX | texlab | via Mason |

### AI assistant

Runs locally. The `qwen2.5-coder:7b` model through Ollama, a 16384-token context (about 5.5 GB of video memory), and the model stays in memory for 30 minutes. For a graphics card with less memory, reduce `num_ctx` in `lua/config/lazy.lua` to 8192.

## Keys

The leader key is Space.

| Keys | Action |
|---|---|
| `jk` (insert mode) | Back to normal mode |
| `Ctrl+p` | Find a file by name |
| `Ctrl+f` | Search text across all files |
| `Ctrl+n` | File tree |
| `gd` | Go to definition |
| `Ctrl+y` | Accept a completion item |
| Space `a` | Open and close the AI chat |
| Space `c` (in a selection) | Send the selected code to the chat |
| Space `i` | Edit code by request (`g2` accept, `g3` reject) |

In LaTeX files the standard VimTeX mappings work (local leader `\`): `\ll` starts and stops the build, `\lv` opens the PDF, `\le` shows errors, `\lc` removes auxiliary files.

## Structure

```text
nvim/
├── init.lua
├── lazy-lock.json
├── LICENSE
├── README.md / README_en.md
├── lua/
│   └── config/
│       ├── lazy.lua      # plugins
│       ├── lsp.lua       # language servers
│       └── options.lua   # settings and keys
├── docs/                 # guides and cheat sheet (md and bilingual PDF)
└── tools/
    └── tex2md.py         # builds the md files from the .tex sources
```

`lazy-lock.json` pins plugin versions, so on another computer everything is installed in exactly the versions the config was tested with.

## Documentation

Detailed guides are in the [`docs`](docs) folder. Each one comes in Russian, in English, and as a bilingual PDF (Russian on the left, English on the right).

| Document | Russian | English | PDF |
|---|---|---|---|
| Neovim setup from scratch | [md](docs/install-neovim_ru.md) | [md](docs/install-neovim_en.md) | [pdf](docs/install-neovim_ru-en.pdf) |
| Additional setup: Markdown and LaTeX | [md](docs/install-markdown-latex_ru.md) | [md](docs/install-markdown-latex_en.md) | [pdf](docs/install-markdown-latex_ru-en.pdf) |
| Cheat sheet: keys and commands | [md](docs/cheatsheet-neovim_ru.md) | [md](docs/cheatsheet-neovim_en.md) | [pdf](docs/cheatsheet-neovim_ru-en.pdf) |

The sources are the `docs/*_ru-en.tex` files. The `.md` files are generated from them: after editing a `.tex` file run `python tools/tex2md.py` and rebuild the PDF (`latexmk -xelatex docs/name_ru-en.tex`).

## Requirements

- Windows 11, Windows Terminal.
- [Neovim](https://neovim.io) 0.12 and Git.
- Python 3.12, Node.js, Rust (`rustup`).
- `ripgrep`, `tree-sitter-cli`, a C compiler (to build Treesitter parsers).
- The JetBrainsMono Nerd Font selected in Windows Terminal settings (otherwise you will see diamonds instead of icons).
- [MiKTeX](https://miktex.org) for LaTeX (it includes `latexmk` and `xelatex`) and [Strawberry Perl](https://strawberryperl.com): `latexmk` is written in Perl and MiKTeX does not include it.
- [Ollama](https://ollama.com) and the `qwen2.5-coder:7b` model.

## Installation (short)

Full step-by-step version: [docs/install-neovim_en.md](docs/install-neovim_en.md).

1. Install the programs from the Requirements section.
2. Clone the config. If an `nvim` folder already exists, rename it first.

   ```powershell
   git clone <address of this repository> $env:LOCALAPPDATA/nvim
   ```

3. Run `nvim`. lazy.nvim downloads the plugins by itself; wait until it finishes and close the window with `q`.
4. Install the parsers: `:TSInstall lua python rust`.
5. Install the servers from the table above: Pyright, rust-analyzer, PowerShell Editor Services, and also `:MasonInstall texlab marksman`.
6. Download the model: `ollama pull qwen2.5-coder:7b`.
7. Check that everything is fine: `:checkhealth`.

Servers, Mason packages, Ollama models and the plugins themselves are not part of the repository; they must be installed again on every computer.

## Notes and limitations

- **PowerShell.** The server is started through the built-in Windows PowerShell 5.1 (`powershell`), because Neovim cannot launch PowerShell 7 from the Microsoft Store.
- **LaTeX and Perl.** Without Perl the build (`\ll`) fails with "could not find the script engine perl". Details in the [Markdown and LaTeX guide](docs/install-markdown-latex_en.md).
- **LaTeX and Cyrillic.** The build uses XeLaTeX. For Russian text the document must name an installed font with Cyrillic support (tested: Times New Roman). The PDF opens in the default Windows viewer.
- **Russian keyboard layout.** Normal-mode commands do not work while the Russian layout is active; no layout-mapping setup has been added.
- **Punto Switcher.** If it is installed, add Windows Terminal to "Exception programs", otherwise it switches the layout and breaks commands.
- **Local model.** A 7-billion-parameter model handles short questions and small edits well but is weaker than cloud models on complex tasks. Review the results of edits.
- The Obsidian integration plugin (`obsidian.nvim`) is not used: vault Markdown files can be opened and edited directly.

## License

[MIT](LICENSE): you may freely use, copy and modify the config, including in your own projects.

