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
  [[& '%s/PowerShellEditorServices/Start-EditorServices.ps1' -BundledModulesPath '%s' -LogPath '%s/powershell_es.log' -SessionDetailsPath '%s/powershell_es.session.json' -FeatureFlags @() -AdditionalModules @() -HostName nvim -HostProfileId 0 -HostVersion 1.0.0 -Stdio -LogLevel Normal]],
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
