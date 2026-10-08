# Neovim cheat sheet: keys and commands

English | [Русский](cheatsheet-neovim_ru.md) | [PDF (Russian and English)](cheatsheet-neovim_ru-en.pdf)

Configuration for Windows 11: Python, Rust, PowerShell, Markdown, LaTeX, a local AI assistant · October 2026

## How to read

- `Esc` switches to normal mode (commands), `i` switches to insert mode (typing). Unless stated otherwise, the keys below are pressed in normal mode.
- `Space a` means: press the space bar, release it, press `a`.
- Anything that starts with a colon is a command: type it and press Enter.
- Words such as `word`, `old`, `new`, `file` in commands are placeholders: replace them with your own.
- In PowerShell you can write paths with forward slashes: `$env:LOCALAPPDATA/nvim` works the same as with backslashes.

## Modes

| Keys | What it does |
|---|---|
| `i` | Insert mode before the cursor |
| `o / O` | New line below / above and insert mode |
| `Esc` | Back to normal mode |
| `jk` | In insert mode, pressed quickly: same as Esc |
| `V` | Select whole lines (then j / k extend the selection) |
| `v` | Select by characters |

## Saving and quitting

| Command | What it does |
|---|---|
| `:w` | Save |
| `:wq` | Save and quit |
| `:q` | Quit (will not work if there are unsaved changes) |
| `:q!` | Quit without saving |
| `:qa` | Close all windows |
| `:qa!` | Close all windows without saving (helps when the chat or the tree is open) |
| `:e!` | Discard unsaved changes and restore the file as of the last save |

## Moving around

| Keys | What it does |
|---|---|
| `j / k` | Down / up |
| `0` | To the start of the line |
| `gg` | To the start of the file |
| `G` | To the end of the file |
| `:30 or 30G` | To line 30 |
| `Ctrl+Home` | To the start of the file |
| `Ctrl+w, w` | Switch between windows (file, tree, chat) |

## Searching and editing text

| Keys | What it does |
|---|---|
| `/word, Enter` | Find a word in the file |
| `:44d` | Delete line 44 |
| `:25,$d` | Delete lines from 25 to the end of the file |
| `:%s/old/new/` | Replace text in the file (first match on each line) |
| `cw` | Replace the word under the cursor: deletes the word and starts insert mode |
| `0, D` | Clear the whole line (D deletes from the cursor to the end of the line) |
| `gg=G` | Re-indent the whole file |
| `u` | Undo the last action (can be pressed several times) |
| `Ctrl+r` | Redo what was undone |

## Files and search

| Keys | What it does |
|---|---|
| `:e $MYVIMRC` | Open init.lua |
| `:e $LOCALAPPDATA/nvim/lua/config/lazy.lua` | Open a file by path |
| `Ctrl+p` | Find a file by name (replaces the default key) |
| `Ctrl+f` | Search text across all project files (replaces page scrolling) |
| `Ctrl+n` | Open and close the file tree on the left |
| `Arrows, Enter, Esc` | In the search windows and the tree: choose, open, close |

The configuration files live in `$LOCALAPPDATA/nvim/`: `init.lua`, `lua/config/options.lua`, `lua/config/lazy.lua` (plugins), `lua/config/lsp.lua` (language servers), `lazy-lock.json` (plugin versions).

## Code: hints and completion

| Keys | What it does |
|---|---|
| `gd` | Go to the definition of a function or variable (Python, Rust, PowerShell) |
| `Ctrl+y` | Accept the selected item |
| `Ctrl+n / Ctrl+p / arrows` | Choose an item in the menu |
| `Ctrl+e` | Close the menu |
| `Ctrl+Space` | Open the menu manually |

Errors and warnings from the language server are shown as text to the right of the line. The entry `E:2 W:1` in the status line shows the number of errors and warnings in the file. The completion menu appears by itself while you type.

Note: in the default blink.cmp key layout the Enter key does not accept an item; use `Ctrl+y` for that.

The server starts 10–30 seconds after you open a file. If there are no hints, run `:checkhealth vim.lsp`.

## Markdown

| Command | What it does |
|---|---|
| `:RenderMarkdown toggle` | Turn the rendered Markdown view on or off |
| `:set ft?` | Which file type Neovim detected (for Markdown it should be filetype=markdown) |

The rendered view is shown in normal mode, while insert mode shows the raw markup. The language server for Markdown is called marksman; whether it is attached is shown by `:checkhealth vim.lsp`.

## LaTeX (VimTeX)

| Keys | What it does |
|---|---|
| `\ll` | Start continuous PDF build |
| `\lv` | Open the PDF |
| `\le` | Show build errors |
| `\lk` | Stop the build |
| `\li` | VimTeX info (project, compiler) |
| `\lc` | Remove build auxiliary files (.aux, .log, etc.) |
| `:VimtexInfo` | Same as `\li`, as a command |
| `:Mason` | Language server manager window |
| `:MasonInstall texlab marksman` | Install the LaTeX and Markdown servers |

The sign `\` is the Backslash key. Building requires MiKTeX and Perl; see the guide [`install-markdown-latex`](install-markdown-latex_en.md) for details.

## AI assistant (local model)

Ollama must be running before you start (the llama icon in the tray). Model: `qwen2.5-coder:7b`, context 16384 tokens.

| Keys | What it does |
|---|---|
| `Space a` | Open and close the chat |
| `V, j/k, Space c` | Send the selected code to the chat |
| `V, j/k, Space i` | Edit the selected code according to your task |
| `i, Ctrl+s` | In the chat: start typing and send the question |
| `g2 / g3 / g1` | Accept / reject / always accept the edit |
| `ga` | In the chat: choose another model |

Commands: `:CodeCompanionChat` (open the chat), `:CodeCompanionChat Toggle`, `:CodeCompanionChat Add` (add the selection), `:CodeCompanion task text` (edit in place; write your task instead of `task text`).

The keys `g1`, `g2`, `g3` and `ga` are assigned by the codecompanion.nvim plugin itself; other versions of the plugin may use different ones.

**A question about code.** Select the code (`V`, `j`/`k`), `Space c`, `i`, the question, `Ctrl+s`. The answer arrives in 10–20 seconds.

**Editing code.** Select the code, `Space i`, write the task, Enter. The edit appears as a separate block: `g2` accepts, `g3` rejects. Always review the result: a 7B model sometimes gets details wrong (for example, puts a comment in the wrong place).

Tip: select the function you need rather than the whole file. Answers are more accurate and the context does not overflow. To check that it runs on the video card: `ollama ps` (it should say `100% GPU`).

## Diagnostics and utility commands

| Command | What it does |
|---|---|
| `:checkhealth` | General health check |
| `:checkhealth vim.lsp` | Are the language servers working |
| `:checkhealth lazy` | Plugin manager state |
| `:checkhealth nvim-treesitter` | Installed highlighting parsers |
| `:checkhealth vim.provider` | Provider check (Python, Node, etc.) |
| `:Inspect` | What highlights the word under the cursor (confirms Treesitter works) |
| `:set ft?` | Which file type Neovim detected |
| `:TSInstall python` | Install a highlighting parser for a language (also rust, lua) |
| `:Lazy` | Plugin manager window; q closes it |

## PowerShell commands that were used

| Command | What for |
|---|---|
| `nvim file` | Open a file in Neovim |
| `nvim $env:LOCALAPPDATA/nvim/lua/config/lsp.lua` | Open a configuration file |
| `pwsh --version`<br>`rustc --version`<br>`cargo --version` | Check installed programs |
| `rust-analyzer --version`<br>`pyright --version` | Check the language servers |
| `cargo new rust_test` | Create a test Rust project |
| `nvidia-smi` | Video memory and GPU load |
| `ollama pull qwen2.5-coder:7b` | Download the model |
| `ollama run qwen2.5-coder:7b` | Ask the model a question in the terminal |
| `ollama ps` | Which models are loaded and what they run on |
| `git init`<br>`git add .`<br>`git commit -m 'message'` | Create a repository and save a config version |
| `git log --oneline`<br>`git status` | History and state of the repository |

## Common problems

- **E37: No write since last change.** The file is not saved. Press `:wq` or `:q!`.
- **E486: Pattern not found.** The text is not in the current file or window. Often the search is started in the wrong file.
- **The chat or commands “break”.** Punto Switcher interferes. Settings, then “Exception programs”, add `WindowsTerminal.exe`.
- **The chat does not let you type.** It opens in normal mode. Press `i`.
- **`:q` does not close the window when the chat or the tree is open.** Use `:qa!`.
- **Parser could not be created for language.** The parser is not installed. Run `:TSInstall language`, replacing it with the language name.
- **No code hints.** Wait 10–30 seconds and run `:checkhealth vim.lsp`.
- **No reply from the model.** Check that Ollama is running (the tray icon, `ollama ps`).
- **The LaTeX build does not start: “could not find the script engine perl”.** Perl is not installed. See the guide [`install-markdown-latex`](install-markdown-latex_en.md).
