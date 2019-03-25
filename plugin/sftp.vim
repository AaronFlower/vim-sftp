if !exists('g:sftp_config_name')
    let g:sftp_config_name = 'sftp-config.json'
endif

function! g:SftpUploadFile()
    python3 vim_sftp.sftp_put()
endfunction

function! g:SftpClearAll()
    python3 vim_sftp.sftp_clear()
endfunction

nnoremap <leader>t :call g:SftpUploadFile()<cr><cr>

augroup vimsftp
    autocmd!
    autocmd VimLeavePre * :call g:SftpClearAll()
augroup END


if !has('python3')
    echom "Vim has to be compliled with +python3 to run this"
    finish
endif

if exists('g:vim_sftp_plugin_loaded')
    finish
endif

" The rest is the plugin VimL Code
let g:vim_sftp_plugin_loaded = 1

let s:plugin_root_dir =  fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF

import sys
from os.path import normpath, join
import vim

plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))

sys.path.insert(0, python_root_dir)

import vim_sftp

EOF
