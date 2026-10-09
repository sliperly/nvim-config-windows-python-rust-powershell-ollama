# Neovim setup from scratch (Windows 11)

English | [Русский](install-neovim_ru.md) | [PDF (Russian and English)](install-neovim_ru-en.pdf)

A step-by-step guide to reproduce this configuration on another computer · October 2026

## What you get

- Neovim 0.12 with the lazy.nvim plugin manager.
- Syntax highlighting (Treesitter), autocompletion (blink.cmp), file and text search (Telescope), a file tree (nvim-tree), the tokyonight theme, icons (Nerd Font).
- Hints, errors and go-to-definition for Python (Pyright), Rust (rust-analyzer) and PowerShell (PowerShell Editor Services).
- A local AI assistant: Ollama, the qwen2.5-coder:7b model and the codecompanion.nvim plugin.

You need an internet connection. For the local model a graphics card with 8 GB of memory is recommended: without one the model runs on the CPU and is noticeably slower. All commands are run in PowerShell. After installing programs, close PowerShell and open it again so the paths are updated.

Markdown and LaTeX are covered separately, in the guide [`install-markdown-latex`](install-markdown-latex_en.md). Read it after this one.

## Step 1. Install the programs

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

Notes:

- If winget cannot find a package, search for it with `winget search name`: identifiers sometimes change.
- Node.js is needed for Pyright, Python is needed for parsing Python code, and Rust is installed via rustup.
- Building Treesitter parsers requires a C compiler. The original computer has Visual Studio. If `:TSInstall` complains about a missing compiler, install Build Tools for Visual Studio with the “Desktop development with C++” workload, or another compiler (for example, zig).
- The Neovim clipboard usually works through win32yank, which is bundled. Check: `:checkhealth vim.provider`.

## Step 2. Choose the font in Windows Terminal

1. Press `Ctrl+,` (the settings open).
2. On the left, under “Profiles”, choose “Defaults”, then the “Appearance” tab.
3. In the “Font face” field choose JetBrainsMono Nerd Font and click “Save”.

If the font is not in the list, close Windows Terminal completely and open it again. Without this step you will see diamonds instead of icons.

## Step 3. Bring the config over

The config lives in the folder `$env:LOCALAPPDATA/nvim`. If it already exists, rename it:

```powershell
Rename-Item $env:LOCALAPPDATA/nvim nvim.old
```

**Option A: from GitHub.** Run the commands below the text.

```powershell
cd $env:LOCALAPPDATA
git clone https://github.com/sliperly/nvim-config-windows-python-rust-powershell-ollama.git nvim
```

**Option B: without GitHub.** Copy the `nvim` folder from the old computer (flash drive, archive) into `$env:LOCALAPPDATA`. Check:

```powershell
Get-ChildItem $env:LOCALAPPDATA/nvim
```

You should see `init.lua`, `lua` and `lazy-lock.json`.

**Option C: by hand.** Create the files from the appendix at the end of this guide.

The file `lazy-lock.json` pins exact plugin versions, so on the new computer everything is installed exactly as it works now.

## Step 4. First launch

```powershell
nvim
```

lazy.nvim will download itself and all the plugins. A window with a list appears: wait until loading finishes and close the window with `q`. On first launch the blink.cmp plugin downloads a prebuilt binary (internet needed). If red errors appear, close Neovim and start it again.

If the config was taken from the repository, it already contains plugins and settings for Markdown and LaTeX. They install by themselves. Until you complete the second guide, opening a `.md` or `.tex` file may show a message that the texlab or marksman server was not found. This is normal.

## Step 5. Highlighting parsers

In Neovim run:

```vim
:TSInstall lua python rust
```

Give each language 20–40 seconds. Check: `:checkhealth nvim-treesitter`. The Installed languages list should contain `lua`, `python` and `rust`.

## Step 6. Language servers

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

**PowerShell (PowerShell Editor Services).** Download and unpack (commands below the text). The last command should print `True`.

```powershell
$dir = Join-Path $env:LOCALAPPDATA 'nvim-data/pses'
New-Item -ItemType Directory -Force $dir | Out-Null
$url = 'https://github.com/PowerShell/PowerShellEditorServices/releases/latest/download/PowerShellEditorServices.zip'
$zip = Join-Path $dir 'pses.zip'
Invoke-WebRequest $url -OutFile $zip
Expand-Archive $zip -DestinationPath $dir -Force
Test-Path (Join-Path $dir 'PowerShellEditorServices/Start-EditorServices.ps1')
```

Important: in `lsp.lua` the server is started through `powershell` (the built-in Windows PowerShell 5.1), because Neovim cannot launch PowerShell 7 from the Microsoft Store. If PowerShell 7 was installed with the regular installer, you can replace `powershell` with `pwsh`.

## Step 7. Local model

Ollama starts by itself after installation (a llama icon in the tray). Then:

```powershell
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b 'Hello'
ollama ps
```

The model takes about 4.7 GB. In the PROCESSOR column of `ollama ps` you should see `100% GPU`. The plugin is set to a 16384-token context, which is about 5.5 GB of video memory. If you have less than 8 GB of video memory, reduce `num_ctx` in `lazy.lua` to 8192.

## Step 8. Punto Switcher (if installed)

Punto Switcher switches the keyboard layout on the fly and breaks command input. Right-click its tray icon, then “Settings”, the “Exception programs” section, and add `WindowsTerminal.exe`.

## Step 9. Check

- `:checkhealth` shows no red errors, and `:checkhealth vim.provider` shows Python, Node, Perl and Ruby as Disabled. These are Neovim's internal providers being switched off; it has nothing to do with programs installed in Windows.
- A file `test.py` with the single line `print(abc)`: an error `abc is not defined` appears on the right.
- `Ctrl+p` (find file), `Ctrl+f` (find text) and `Ctrl+n` (tree) work.
- Typing `pri` in a Python file opens the completion menu.
- Space, then `a` opens the chat, then `i`, a question and `Ctrl+s`: the model replies.

## Appendix. Configuration files

Folder: `$env:LOCALAPPDATA/nvim`. The code below is the same for both languages.

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

In the repository the PowerShell launch string in `lsp.lua` is written as one long line. Here it is split into parts so that copying from the PDF does not introduce stray line breaks. It works the same way.

## Config backup

Save a version:

```powershell
cd $env:LOCALAPPDATA/nvim
git add .
git commit -m 'Update config'
```

If the folder is not yet a Git repository (option C), first run `git init -b master`.

Git signs commits with your name and email. If it does not know them, set them:

```powershell
git config --global user.name 'YOUR_NAME'
git config --global user.email 'YOUR_EMAIL'
```

**Important:** in a public repository the email from commits is visible to everyone. On GitHub open Settings, then Emails, and turn on “Keep my email addresses private”. The same page shows a hidden address like `12345678+name@users.noreply.github.com`: use it instead of `YOUR_EMAIL`. Do this before the first commit, otherwise old commits have to be rewritten.

Publish to GitHub (optional): create an empty repository on github.com (private or public). Replace `YOUR_REPO_URL` in the command with its address.

If the config came from someone else's repository (option A), the origin address now points to the author's repository. Redirect it to your own:

```powershell
git remote set-url origin YOUR_REPO_URL
git push -u origin master
```

If origin is not set yet (options B and C), run `git remote add origin YOUR_REPO_URL` instead of the first line.

Only your files and `lazy-lock.json` go into the copy. The plugins themselves are not included: lazy downloads them on first launch. Do not put passwords or access keys into the repository (there are none in the config now).

## What next

If you need Markdown and LaTeX, continue with the guide [`install-markdown-latex`](install-markdown-latex_en.md). Key reference: [`cheatsheet-neovim`](cheatsheet-neovim_en.md).
