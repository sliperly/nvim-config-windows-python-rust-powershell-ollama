# Дополнительная установка Markdown и LaTeX

Русский | [English](install-markdown-latex_en.md) | [PDF (русский и английский)](install-markdown-latex_ru-en.pdf)

Инструкция для готовой конфигурации Neovim из этого репозитория (Windows 11).

## Назначение

Инструкция добавляет и проверяет: Markdown; LaTeX; LSP для обоих; красивое отображение Markdown; сборку LaTeX в PDF. Основная установка описана в файле [`install-neovim`](install-neovim_ru.md).

## 1. Что нужно заранее

Windows 11; Neovim 0.12 или новее; Git; конфигурация из этого репозитория, которая запускается без ошибок. PowerShell 7 желателен. Проверка версии Neovim (в PowerShell):

```powershell
nvim --version
```

## 2. Установка MiKTeX

MiKTeX — дистрибутив LaTeX для Windows. Скачайте его с официального сайта `https://miktex.org/download`, установите и перезапустите PowerShell. Проверка:

```powershell
xelatex --version
latexmk --version
```

Обе команды должны выполниться без сообщения «команда не найдена». Если нужно узнать, откуда запускаются программы:

```powershell
Get-Command xelatex
Get-Command latexmk
```

## 3. Установка Perl (обязательно)

Программа `latexmk` написана на Perl, а MiKTeX Perl не содержит. Без него сборка падает с сообщением «MiKTeX could not find the script engine perl». Установите Strawberry Perl с сайта `https://strawberryperl.com`, затем перезапустите PowerShell и проверьте:

```powershell
perl -v
```

Должна показаться версия Perl. После этого перезапустите и Neovim.

## 4. Проверка XeLaTeX и русского текста

Создайте временный файл `test.tex`:

```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[russian]{babel}
\begin{document}
\section{Тест}
Это обычный русский текст.
\[
E = mc^2
\]
\end{document}
```

Перейдите в папку с файлом и выполните:

```powershell
xelatex test.tex
```

Рядом должен появиться `test.pdf`. Откройте его: русский текст и формула должны отображаться правильно. Можно использовать любой другой установленный шрифт с кириллицей.

## 5. Плагины в lazy.lua

Если конфиг взят из репозитория (варианты А и Б основной инструкции), нужные плагины уже есть в `lua/config/lazy.lua`: Mason (менеджер серверов), render-markdown и VimTeX. Если вы создавали файлы вручную (вариант В), добавьте эти три блока в список `spec` в `lazy.lua`. VimTeX настроен на XeLaTeX:

```lua
{
  "lervag/vimtex",
  ft = "tex",
  init = function()
    vim.g.vimtex_compiler_latexmk_engines = {
      _ = "-xelatex",
    }
  end,
},
```

Блок для Mason (менеджера серверов):

```powershell
{
  "mason-org/mason.nvim",
  opts = {},
},
```

Блок для render-markdown приведён в разделе 9.

После изменения конфигурации перезапустите Neovim. В открытом `.tex`-файле выполните:

```vim
:VimtexInfo
```

В информации должен быть виден компилятор `latexmk`.

## 6. Сборка LaTeX через VimTeX

Откройте `.tex`-файл в Neovim. Знак `\` — это клавиша Backslash.

- `\ll` — запустить сборку;
- `\lv` — открыть PDF;
- `\le` — показать ошибки;
- `\lk` — остановить сборку;
- `\li` — информация VimTeX.

Например, для сборки: `Esc`, затем `\`, `l`, `l`. Если Windows не даёт пересобрать файл, закройте PDF в просмотрщике.

## 7. Серверы texlab и marksman (Mason)

LSP-серверы ставятся через Mason *внутри Neovim*. Они хранятся не в репозитории, а в папке данных Neovim, поэтому на новом компьютере их нужно поставить заново:

```vim
:MasonInstall texlab marksman
```

Сам Mason можно открыть командой `:Mason`. Подождите, пока установка закончится, и перезапустите Neovim.

## 8. Настройка серверов в lsp.lua

В `lua/config/lsp.lua` (из репозитория) уже есть следующее; при ручной установке (вариант В) добавьте это в конец файла:

```lua
vim.lsp.config('texlab', {
  cmd = { 'texlab' },
  filetypes = { 'tex' },
  root_markers = { '.latexmkrc', '.git' },
})
vim.lsp.enable('texlab')

vim.lsp.config('marksman', {
  cmd = { 'marksman', 'server' },
  filetypes = { 'markdown' },
  root_markers = { '.git' },
})
vim.lsp.enable('marksman')
```

Откройте `.tex`- или `.md`-файл и выведите подключённые серверы:

```vim
:lua for _, c in ipairs(vim.lsp.get_clients({bufnr=0})) do print(c.name) end
```

Для `.tex` должен быть `texlab`, для `.md` — `marksman`.

## 9. Отображение Markdown

За красивое отображение отвечает плагин render-markdown.nvim. Он включается сам для файлов Markdown:

```powershell
{
  "MeanderingProgrammer/render-markdown.nvim",
  ft = "markdown",
  opts = {},
},
```

Откройте любой `.md`-файл: заголовки, списки и выделение должны отображаться оформленными прямо в Neovim. Тип файла:

```vim
:set filetype?
```

Ожидается `filetype=markdown`.

## 10. Итоговая проверка

**Markdown.** Создайте временный файл `test.md`:

```text
# Тест

Обычный текст, **жирный** и *курсив*.

- первый пункт
- второй пункт

[Сайт Neovim](https://neovim.io)
```

Откройте его в Neovim. Должны выполняться три условия: заголовок и список показаны оформленными, `:set filetype?` выдаёт `filetype=markdown`, а в списке серверов есть `marksman`.

**LaTeX.** Откройте `test.tex` из раздела 4, выполните `:VimtexInfo`, затем `\ll` и `\lv`. PDF должен собраться и открыться, а в списке серверов должен быть `texlab`.

## 11. Что в итоге установлено

- Markdown LSP — Marksman;
- отображение Markdown — render-markdown.nvim;
- LaTeX LSP — texlab;
- интеграция LaTeX — VimTeX;
- сборка — latexmk (нужен Perl) и XeLaTeX;
- дистрибутив — MiKTeX.

## 12. Типичные проблемы

### Сборка падает: «could not find the script engine perl»

Не установлен Perl. См. раздел 3.

### xelatex или latexmk не найден

Проверьте `Get-Command xelatex`. Если не найден, убедитесь, что папка MiKTeX есть в `PATH`, и перезапустите PowerShell и Neovim.

### Русский текст не собирается

Используйте XeLaTeX и пакеты `fontspec` и `babel` с `russian`, а также шрифт с кириллицей.

### texlab или marksman не подключается

Выполните `:MasonInstall texlab marksman`, перезапустите Neovim и повторите проверку из раздела 8.

### Сообщение MiKTeX «you have not checked for MiKTeX updates»

Это не ошибка сборки, если PDF создан. Обновления можно проверить в MiKTeX Console.

### Команда из PDF не работает в PowerShell

Копируйте команды из блоков кода. Если вставился странный символ вместо дефиса, сообщите об этом в Issues репозитория.
