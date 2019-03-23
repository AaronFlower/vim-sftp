## vim sftp

在文件保存的时候检查当前目录以及遍历到根目录是否有 `sftp-config.json` 文件。如果有则根据根据文件上传到到对应服务器上。
对于文件的上传可以放在一个 map 中进行缓存。


### 调试 Vim Log


```
vim -V9myVim.log
```

### References

1. [Write Vim Plugin in Python](http://candidtim.github.io/vim/2017/08/11/write-vim-plugin-in-python.html)
