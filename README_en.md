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
├── .gitignore
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

The sources are the `docs/*_ru-en.tex` files. The `.md` files are generated from them: after editing a `.tex` file run `python tools/tex2md.py` and rebuild the PDF (`latexmk -xelatex -cd docs/name_ru-en.tex`).

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
   git clone https://github.com/sliperly/nvim-config-windows-python-rust-powershell-ollama.git $env:LOCALAPPDATA/nvim
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
