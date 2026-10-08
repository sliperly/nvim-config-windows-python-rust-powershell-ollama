local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

if not (vim.uv or vim.loop).fs_stat(lazypath) then
	local lazyrepo = "https://github.com/folke/lazy.nvim.git"
	local out = vim.fn.system({
		"git",
		"clone",
		"--filter=blob:none",
		"--branch=stable",
		lazyrepo,
		lazypath,
	})

	if vim.v.shell_error ~= 0 then
		vim.api.nvim_echo({
			{ "Failed to clone lazy.nvim:\n", "ErrorMsg" },
			{ out, "WarningMsg" },
		}, true, {})
		return
	end
end

vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
	spec = {
		{
			"olimorris/codecompanion.nvim",
			dependencies = {
				"nvim-lua/plenary.nvim",
				"nvim-treesitter/nvim-treesitter",
			},
			cmd = { "CodeCompanion", "CodeCompanionChat", "CodeCompanionActions" },
			opts = {
				interactions = {
					chat = { adapter = { name = "ollama", model = "qwen2.5-coder:7b" } },
					inline = { adapter = { name = "ollama", model = "qwen2.5-coder:7b" } },
				},
				adapters = {
					http = {
						ollama = function()
							return require("codecompanion.adapters").extend("ollama", {
								schema = {
									num_ctx = { default = 16384 },
									keep_alive = { default = "30m" },
								},
							})
						end,
					},
				},
			},
		},	
		{
			"nvim-tree/nvim-tree.lua",
			dependencies = { "nvim-tree/nvim-web-devicons" },
			keys = { { "<C-n>", "<cmd>NvimTreeToggle<cr>" } },
			opts = {},
		},
		{
			"nvim-treesitter/nvim-treesitter",
			build = ":TSUpdate",
		},
		{
			"saghen/blink.cmp",
			version = "1.*",
			opts = {},
		},
		{
			"nvim-telescope/telescope.nvim",
			dependencies = { "nvim-lua/plenary.nvim" },
			keys = {
				{ "<C-p>", "<cmd>Telescope find_files<cr>" },
				{ "<C-f>", "<cmd>Telescope live_grep<cr>" },
			},
		},
		{
			"folke/tokyonight.nvim",
			lazy = false,
			priority = 1000,
			config = function() vim.cmd.colorscheme("tokyonight") end,
		},
		{
			"MeanderingProgrammer/render-markdown.nvim",
			ft = "markdown",
			opts = {},
		},
		{
			"lervag/vimtex",
			ft = "tex",
			init = function()
				vim.g.vimtex_compiler_latexmk_engines = {
					_ = "-xelatex",
				}
			end,
		},
		{
			"mason-org/mason.nvim",
			opts = {},
		},
	},
	rocks = { enabled = false },
})
