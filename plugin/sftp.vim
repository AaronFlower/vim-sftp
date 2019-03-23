echom "load sftp config"
echom expand("<sfile>")
echom resolve(expand('<sfile>:p'))
echom fnamemodify(resolve(expand('<sfile>:p')), ':h')

function! g:SftpUploadFile()
    echom "call SftpUploadFile()"
endfunction

nnoremap <leader>t :call g:SftpUploadFile()<cr>

if !has('python3')
    echom "Vim has to be compliled with +python3 to run this"
    finish
endif

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
