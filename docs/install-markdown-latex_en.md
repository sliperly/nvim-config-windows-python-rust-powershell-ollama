# Additional setup: Markdown and LaTeX

English | [Русский](install-markdown-latex_ru.md) | [PDF (Russian and English)](install-markdown-latex_ru-en.pdf)

A guide for the ready-made Neovim configuration from this repository (Windows 11).

## Purpose

This guide adds and checks: Markdown; LaTeX; LSP for both; nice Markdown rendering; LaTeX-to-PDF builds. The base installation is described in [`install-neovim`](install-neovim_en.md).

## 1. Prerequisites

Windows 11; Neovim 0.12 or newer; Git; the configuration from this repository starting without errors. PowerShell 7 is recommended. Check the Neovim version (in PowerShell):

```powershell
nvim --version
```

## 2. Install MiKTeX

MiKTeX is a LaTeX distribution for Windows. Download it from the official site `https://miktex.org/download`, install it and restart PowerShell. Check:

```powershell
xelatex --version
latexmk --version
```

Both commands must run without a “command not found” message. To see where the programs are launched from:

```powershell
Get-Command xelatex
Get-Command latexmk
```

## 3. Install Perl (required)

`latexmk` is written in Perl, and MiKTeX does not include Perl. Without it the build fails with “MiKTeX could not find the script engine perl”. Install Strawberry Perl from `https://strawberryperl.com`, restart PowerShell and check:

```powershell
perl -v
```

The Perl version should be printed. Then restart Neovim as well.

## 4. Check XeLaTeX and Russian text

Create a temporary file `test.tex`:

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

Go to the folder with the file and run:

```powershell
xelatex test.tex
```

`test.pdf` should appear next to it. Open it: the Russian text and the formula must display correctly. Any other installed font with Cyrillic support will do.

## 5. Plugins in lazy.lua

If the config was taken from the repository (options A and B of the base guide), the required plugins are already in `lua/config/lazy.lua`: Mason (server manager), render-markdown and VimTeX. If you created the files by hand (option C), add these three blocks to the `spec` list in `lazy.lua`. VimTeX is set to XeLaTeX:

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

The block for Mason (the server manager):

```lua
{
  "mason-org/mason.nvim",
  opts = {},
},
```

The block for render-markdown is in section 9.

After changing the configuration, restart Neovim. In an open `.tex` file run:

```vim
:VimtexInfo
```

The compiler `latexmk` should be listed.

## 6. Building LaTeX with VimTeX

Open a `.tex` file in Neovim. The sign `\` is the Backslash key.

- `\ll` — start the build;
- `\lv` — open the PDF;
- `\le` — show errors;
- `\lk` — stop the build;
- `\li` — VimTeX info.

For example, to build: `Esc`, then `\`, `l`, `l`. If Windows refuses to rebuild the file, close the PDF in the viewer.

## 7. Servers texlab and marksman (Mason)

LSP servers are installed through Mason *inside Neovim*. They are not stored in the repository but in Neovim's data folder, so on a new computer they must be installed again:

```vim
:MasonInstall texlab marksman
```

Mason itself opens with `:Mason`. Wait until the installation finishes and restart Neovim.

## 8. Server settings in lsp.lua

`lua/config/lsp.lua` (from the repository) already contains the following; with a manual install (option C) add it to the end of the file:

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

Open a `.tex` or `.md` file and list the attached servers:

```vim
:lua for _, c in ipairs(vim.lsp.get_clients({bufnr=0})) do print(c.name) end
```

A `.tex` file should show `texlab`, a `.md` file `marksman`.

## 9. Markdown rendering

Nice rendering is done by the render-markdown.nvim plugin. It turns on by itself for Markdown files:

```lua
{
  "MeanderingProgrammer/render-markdown.nvim",
  ft = "markdown",
  opts = {},
},
```

Open any `.md` file: headings, lists and emphasis should appear formatted right inside Neovim. File type:

```vim
:set filetype?
```

Expected: `filetype=markdown`.

## 10. Final check

**Markdown.** Create a temporary file `test.md`:

```text
# Test

Plain text, **bold** and *italic*.

- first item
- second item

[Neovim site](https://neovim.io)
```

Open it in Neovim. Three conditions must hold: the heading and the list are shown formatted, `:set filetype?` prints `filetype=markdown`, and `marksman` is in the server list.

**LaTeX.** Open `test.tex` from section 4, run `:VimtexInfo`, then `\ll` and `\lv`. The PDF must build and open, and `texlab` must be in the server list.

## 11. What ends up installed

- Markdown LSP — Marksman;
- Markdown rendering — render-markdown.nvim;
- LaTeX LSP — texlab;
- LaTeX integration — VimTeX;
- build — latexmk (needs Perl) and XeLaTeX;
- distribution — MiKTeX.

## 12. Common problems

### Build fails: “could not find the script engine perl”

Perl is not installed. See section 3.

### xelatex or latexmk not found

Run `Get-Command xelatex`. If it is not found, make sure the MiKTeX folder is in `PATH` and restart PowerShell and Neovim.

### Russian text does not build

Use XeLaTeX with the `fontspec` and `babel` packages (`russian`), and a font with Cyrillic.

### texlab or marksman does not attach

Run `:MasonInstall texlab marksman`, restart Neovim and repeat the check from section 8.

### MiKTeX message “you have not checked for MiKTeX updates”

This is not a build error if the PDF was created. You can check for updates in MiKTeX Console.

### A command from the PDF does not work in PowerShell

Copy commands from the code blocks. If a strange character appears instead of a hyphen, please report it in the repository Issues.
