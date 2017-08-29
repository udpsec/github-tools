# Shadowsocks proxy for git
-  在linux中利用shadowsocks 给git配置 http 和 ssh 代理，加速git操作. 

【1】 编写一个shell

```sh
$ nano  ~/gitproxy.sh
```
【2】 拷贝代码到 ``` gitproxy.sh ```

```sh
#!/bin/sh 
nc -X 5 -x 127.0.0.1:1080 "$@"
```
【3】然后修改 ``` ～/.gitconfig ``` 支持http代理

```sh
[core]
gitproxy=~/gitproxy.sh
[http]
proxy=socks5://127.0.0.1:1080
```
【4】修改``` /etc/ssh/ssh_config ``` 设置``` ssh:// ``` 全局代理

```sh
ProxyCommand nc -X 5 -x 127.0.0.1:1080 %h %p
```
