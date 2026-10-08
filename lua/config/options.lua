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
