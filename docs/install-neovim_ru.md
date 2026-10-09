# Установка и настройка Neovim с нуля (Windows 11)

Русский | [English](install-neovim_en.md) | [PDF (русский и английский)](install-neovim_ru-en.pdf)

Пошаговая инструкция, как повторить эту конфигурацию на другом компьютере · октябрь 2026

## Что получится

- Neovim 0.12 с менеджером плагинов lazy.nvim.
- Подсветка кода (Treesitter), автодополнение (blink.cmp), поиск файлов и текста (Telescope), файловое дерево (nvim-tree), тема tokyonight, значки (Nerd Font).
- Подсказки, ошибки и переход к определению для Python (Pyright), Rust (rust-analyzer) и PowerShell (PowerShell Editor Services).
- Локальный ИИ-помощник: Ollama, модель qwen2.5-coder:7b и плагин codecompanion.nvim.

Нужен интернет. Для локальной модели желательна видеокарта с 8 ГБ памяти: без неё модель работает на процессоре и заметно медленнее. Все команды выполняются в PowerShell. После установки программ закройте PowerShell и откройте заново, чтобы обновились пути.

Markdown и LaTeX описаны отдельно, в инструкции [`install-markdown-latex`](install-markdown-latex_ru.md). Её читайте после этой.

## Шаг 1. Установить программы

```powershell
winget install Neovim.Neovim
winget install Git.Git
winget install Python.Python.3.12
winget install OpenJS.NodeJS
winget install BurntSushi.ripgrep.MSVC
winget install tree-sitter.tree-sitter-cli
winget install DEVCOM.JetBrainsMonoNerdFont
winget install Rustlang.Rustup
winget install Ollama.Ollama
```

Заметки:

- Если winget не находит пакет, найдите его командой `winget search имя`: идентификаторы иногда меняются.
- Node.js нужен для Pyright, Python нужен для разбора Python-кода, Rust ставится через rustup.
- Для сборки парсеров Treesitter нужен компилятор C. На исходном компьютере стоит Visual Studio. Если `:TSInstall` пожалуется на отсутствие компилятора, поставьте Build Tools для Visual Studio с компонентом «Разработка классических приложений на C++» или другой компилятор (например, zig).
- Буфер обмена Neovim обычно работает через win32yank, который идёт в комплекте. Проверка: `:checkhealth vim.provider`.

## Шаг 2. Выбрать шрифт в Windows Terminal

1. Нажмите `Ctrl+,` (откроются настройки).
2. Слева в разделе «Профили» выберите «По умолчанию», затем вкладку «Оформление».
3. В поле «Шрифт» выберите JetBrainsMono Nerd Font и нажмите «Сохранить».

Если шрифта нет в списке, закройте Windows Terminal полностью и откройте заново. Без этого шага вместо значков будут ромбики.

## Шаг 3. Перенести конфиг

Конфиг лежит в папке `$env:LOCALAPPDATA/nvim`. Если она уже есть, переименуйте её:

```powershell
Rename-Item $env:LOCALAPPDATA/nvim nvim.old
```

**Вариант А: из GitHub.** Команды ниже выполните под текстом.

```powershell
cd $env:LOCALAPPDATA
git clone https://github.com/sliperly/nvim-config-windows-python-rust-powershell-ollama.git nvim
```

**Вариант Б: без GitHub.** Скопируйте папку `nvim` со старого компьютера (флешка, архив) в `$env:LOCALAPPDATA`. Проверка:

```powershell
Get-ChildItem $env:LOCALAPPDATA/nvim
```

Должны быть `init.lua`, `lua` и `lazy-lock.json`.

**Вариант В: вручную.** Создайте файлы по приложению в конце этой инструкции.

Файл `lazy-lock.json` закрепляет точные версии плагинов, поэтому на новом компьютере всё ставится ровно таким, как работает сейчас.

## Шаг 4. Первый запуск

```powershell
nvim
```

lazy.nvim скачает сам себя и все плагины. Появится окно со списком: подождите, пока загрузка закончится, и закройте окно клавишей `q`. Плагин blink.cmp при первом запуске скачивает готовый бинарный файл (нужен интернет). Если появились красные ошибки, закройте Neovim и запустите заново.

Если конфиг взят из репозитория, в нём уже есть плагины и настройки для Markdown и LaTeX. Они установятся сами. Пока вы не прошли вторую инструкцию, при открытии `.md`- или `.tex`-файла может появиться сообщение, что сервер texlab или marksman не найден. Это нормально.

## Шаг 5. Парсеры подсветки

В Neovim выполните:

```vim
:TSInstall lua python rust
```

Дайте каждому языку 20–40 секунд. Проверка: `:checkhealth nvim-treesitter`. В списке Installed languages должны быть `lua`, `python` и `rust`.

## Шаг 6. Языковые серверы

**Python (Pyright):**

```powershell
npm install -g pyright
pyright --version
```

**Rust (rust-analyzer):**

```powershell
rustup component add rust-analyzer
rust-analyzer --version
```

**PowerShell (PowerShell Editor Services).** Скачать и распаковать (команды ниже, под текстом). Последняя команда должна вывести `True`.

```powershell
$dir = Join-Path $env:LOCALAPPDATA 'nvim-data/pses'
New-Item -ItemType Directory -Force $dir | Out-Null
$url = 'https://github.com/PowerShell/PowerShellEditorServices/releases/latest/download/PowerShellEditorServices.zip'
$zip = Join-Path $dir 'pses.zip'
Invoke-WebRequest $url -OutFile $zip
Expand-Archive $zip -DestinationPath $dir -Force
Test-Path (Join-Path $dir 'PowerShellEditorServices/Start-EditorServices.ps1')
```

Важно: в `lsp.lua` сервер запускается через `powershell` (встроенный Windows PowerShell 5.1), потому что PowerShell 7 из Microsoft Store Neovim запустить не может. Если PowerShell 7 установлен обычным установщиком, можно заменить `powershell` на `pwsh`.

## Шаг 7. Локальная модель

Ollama после установки запускается сама (значок ламы в трее). Затем:

```powershell
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b 'Hello'
ollama ps
```

Модель занимает около 4,7 ГБ. В колонке PROCESSOR команды `ollama ps` должно быть `100% GPU`. Плагин настроен на контекст 16384 токена, это около 5,5 ГБ видеопамяти. Если видеопамяти меньше 8 ГБ, уменьшите `num_ctx` в `lazy.lua` до 8192.

## Шаг 8. Punto Switcher (если установлен)

Punto Switcher переключает раскладку на лету и ломает ввод команд. Правый клик по значку в трее, затем «Настройки», раздел «Программы-исключения», добавить `WindowsTerminal.exe`.

## Шаг 9. Проверка

- `:checkhealth` не показывает красных ошибок, а `:checkhealth vim.provider` показывает Python, Node, Perl и Ruby как Disabled. Это отключены внутренние провайдеры Neovim; к программам, установленным в Windows, это отношения не имеет.
- Файл `test.py` с одной строкой `print(abc)`: справа появляется ошибка `abc is not defined`.
- Работают `Ctrl+p` (поиск файла), `Ctrl+f` (поиск текста), `Ctrl+n` (дерево).
- Набор `pri` в Python-файле открывает меню автодополнения.
- Пробел, затем `a` открывает чат, затем `i`, вопрос и `Ctrl+s`: приходит ответ модели.

## Приложение. Файлы конфигурации

Папка: `$env:LOCALAPPDATA/nvim`. Код ниже одинаков для обоих языков.

**init.lua**

```lua
vim.g.loaded_perl_provider = 0
vim.g.loaded_ruby_provider = 0
vim.g.loaded_node_provider = 0
vim.g.loaded_python3_provider = 0

require('config.options')
require('config.lazy')
require('config.lsp')
```

**lua/config/options.lua**

```lua
vim.opt.number = true
vim.opt.mouse = "a"
vim.opt.scrolloff = 7
vim.opt.swapfile = false
vim.opt.termguicolors = true
vim.keymap.set('i', 'jk', '<Esc>')
vim.api.nvim_create_autocmd('FileType', {
  pattern = { 'python', 'lua', 'rust' },
  callback = function() pcall(vim.treesitter.start) end,
})
vim.g.mapleader = ' '
vim.keymap.set({ 'n', 'v' }, '<leader>a', '<cmd>CodeCompanionChat Toggle<cr>')
vim.keymap.set({ 'n', 'v' }, '<leader>i', ':CodeCompanion ')
vim.keymap.set('v', '<leader>c', '<cmd>CodeCompanionChat Add<cr>')
```

**lua/config/lazy.lua**

```lua
local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.fn.system({ 'git', 'clone', '--filter=blob:none', '--branch=stable',
    'https://github.com/folke/lazy.nvim.git', lazypath })
end
vim.opt.rtp:prepend(lazypath)

require('lazy').setup({
  spec = {
    { 'nvim-treesitter/nvim-treesitter', build = ':TSUpdate' },
    { 'saghen/blink.cmp', version = '1.*', opts = {} },
    {
      'nvim-telescope/telescope.nvim',
      dependencies = { 'nvim-lua/plenary.nvim' },
      keys = {
        { '<C-p>', '<cmd>Telescope find_files<cr>' },
        { '<C-f>', '<cmd>Telescope live_grep<cr>' },
      },
    },
    {
      'folke/tokyonight.nvim',
      lazy = false,
      priority = 1000,
      config = function() vim.cmd.colorscheme('tokyonight') end,
    },
    {
      'nvim-tree/nvim-tree.lua',
      dependencies = { 'nvim-tree/nvim-web-devicons' },
      keys = { { '<C-n>', '<cmd>NvimTreeToggle<cr>' } },
      opts = {},
    },
    {
      'olimorris/codecompanion.nvim',
      dependencies = {
        'nvim-lua/plenary.nvim',
        'nvim-treesitter/nvim-treesitter',
      },
      cmd = { 'CodeCompanion', 'CodeCompanionChat', 'CodeCompanionActions' },
      opts = {
        interactions = {
          chat = { adapter = { name = 'ollama', model = 'qwen2.5-coder:7b' } },
          inline = { adapter = { name = 'ollama', model = 'qwen2.5-coder:7b' } },
        },
        adapters = {
          http = {
            ollama = function()
              return require('codecompanion.adapters').extend('ollama', {
                schema = {
                  num_ctx = { default = 16384 },
                  keep_alive = { default = '30m' },
                },
              })
            end,
          },
        },
      },
    },
  },
  rocks = { enabled = false },
})
```

**lua/config/lsp.lua**

```lua
vim.lsp.config('pyright', {
  cmd = { 'pyright-langserver', '--stdio' },
  filetypes = { 'python' },
  root_markers = { 'pyrightconfig.json', 'pyproject.toml', 'setup.py', 'requirements.txt', '.git' },
})
vim.lsp.enable('pyright')

vim.diagnostic.config({ virtual_text = true })

vim.api.nvim_create_autocmd('LspAttach', {
  callback = function(args)
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, { buffer = args.buf })
  end,
})

local pses = vim.fs.normalize(vim.fn.stdpath('data') .. '/pses')
local cache = vim.fs.normalize(vim.fn.stdpath('cache'))
local pses_cmd = string.format(
  "& '%s/PowerShellEditorServices/Start-EditorServices.ps1' "
    .. "-BundledModulesPath '%s' "
    .. "-LogPath '%s/powershell_es.log' "
    .. "-SessionDetailsPath '%s/powershell_es.session.json' "
    .. "-FeatureFlags @() -AdditionalModules @() "
    .. "-HostName nvim -HostProfileId 0 -HostVersion 1.0.0 "
    .. "-Stdio -LogLevel Normal",
  pses, pses, cache, cache
)

vim.lsp.config('powershell_es', {
  cmd = { 'powershell', '-NoLogo', '-ExecutionPolicy', 'Bypass', '-NoProfile', '-Command', pses_cmd },
  filetypes = { 'ps1' },
  root_markers = { 'PSScriptAnalyzerSettings.psd1', '.git' },
})
vim.lsp.enable('powershell_es')

vim.lsp.config('rust_analyzer', {
  cmd = { 'rust-analyzer' },
  filetypes = { 'rust' },
  root_markers = { 'Cargo.toml', 'rust-project.json', '.git' },
})
vim.lsp.enable('rust_analyzer')
```

В репозитории строка запуска PowerShell в `lsp.lua` записана одной длинной строкой. Здесь она разбита на части, чтобы при копировании из PDF не появились лишние переводы строк. Работает она так же.

## Резервная копия конфига

Сохранить версию:

```powershell
cd $env:LOCALAPPDATA/nvim
git add .
git commit -m 'Update config'
```

Если папка ещё не репозиторий Git (вариант В), сначала выполните `git init -b master`.

Git подписывает коммиты вашим именем и почтой. Если он их не знает, задайте:

```powershell
git config --global user.name 'YOUR_NAME'
git config --global user.email 'YOUR_EMAIL'
```

**Важно:** в публичном репозитории почта из коммитов видна всем. На GitHub откройте Settings, затем Emails и включите «Keep my email addresses private». Там же будет скрытый адрес вида `12345678+имя@users.noreply.github.com`: подставьте его вместо `YOUR_EMAIL`. Сделайте это до первого коммита, иначе старые коммиты придётся переписывать.

Выложить на GitHub (по желанию): создайте на github.com пустой репозиторий (закрытый или публичный). Замените в команде `YOUR_REPO_URL` на его адрес.

Если конфиг был взят из чужого репозитория (вариант А), адрес origin сейчас ведёт на репозиторий автора. Перенаправьте его на свой:

```powershell
git remote set-url origin YOUR_REPO_URL
git push -u origin master
```

Если origin ещё не задан (варианты Б и В), вместо первой строки выполните `git remote add origin YOUR_REPO_URL`.

В копию попадают только ваши файлы и `lazy-lock.json`. Сами плагины в неё не входят: lazy скачает их при первом запуске. Не кладите в репозиторий пароли и ключи доступа (сейчас их в конфиге нет).

## Что дальше

Если нужны Markdown и LaTeX, продолжайте по инструкции [`install-markdown-latex`](install-markdown-latex_ru.md). Шпаргалка по клавишам: [`cheatsheet-neovim`](cheatsheet-neovim_ru.md).
