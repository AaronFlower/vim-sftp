## vim sftp

在文件保存的时候检查当前目录以及遍历到根目录是否有 `sftp-config.json` 文件。如果有则根据根据文件上传到到对应服务器上。
对于文件的上传可以放在一个 map 中进行缓存。


### 调试 Vim Log


```
vim -V9myVim.log
```


### How to use.

- `let g:sftp_config_file = 'sftp-config.json'`, 默认使用的是和 Sublime 中的 SFTP 插件配置文件名是一样的。可以通过在 `~/.vimrc` 中修改这个文件来配置配置自己的文件。


### TODO

[-] dir create -p
[-] doc

### References

1. [Write Vim Plugin in Python](http://candidtim.github.io/vim/2017/08/11/write-vim-plugin-in-python.html)
