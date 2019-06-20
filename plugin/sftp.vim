" keymap
nnoremap <leader>t :call sftp#SftpUploadFile()<cr><cr>

" Autocommand Groups clear sftp connections when exit vim.
augroup vimsftp
    autocmd!
    autocmd VimLeavePre * :call sftp#SftpClearAll()
augroup END
