nnoremap <leader>t :call sftp#SftpUploadFile()<cr><cr>

augroup vimsftp
    autocmd!
    autocmd VimLeavePre * :call sftp#SftpClearAll()
augroup END
