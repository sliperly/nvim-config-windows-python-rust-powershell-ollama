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
├── .gitignore
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

Исходники документов — файлы `docs/*_ru-en.tex`. Файлы `.md` из них генерируются: после правки `.tex` выполните `python tools/tex2md.py` и пересоберите PDF (`latexmk -xelatex -cd docs/имя_ru-en.tex`).

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
   git clone https://github.com/sliperly/nvim-config-windows-python-rust-powershell-ollama.git $env:LOCALAPPDATA/nvim
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
