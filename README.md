# AtCoder Numba AOT Tools

Numba の JIT を使用したコードを AOT(事前)コンパイルするためのミニツールです。以下のような Numba の JIT を使ったコードがあった時に、AOT コンパイルをしようと思ったら、普通は`@cc.export`というデコレータを付ける必要があります。それを付けずに AOT コンパイルをします。

```
@jit('i8(i8)', nopython=True)
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 2) + fib(n - 1)
```

AtCoder の場合であれば、Python3 で動作するコードを修正する必要がなくなるので便利になります。


## インストール



## 使い方

atcoder-numba compile 

atcoder-numba submit

現在の AtCoder でも動作します。ただし、バイナリーコードは OS によって異なるので、コードの作成に使用するマシンは、AtCoder のサーバーと同じ OS である linux を使う必要があります。また、glibc のバージョンを合わせておかないとエラーになります。

現在の AtCoder で動作するコードを作成するための環境

ubutu 14.04 サーバを用意

```
wget https://repo.anaconda.com/miniconda/Miniconda3-3.7.3-Linux-x86_64.sh
bash Miniconda3-3.7.3-Linux-x86_64.sh
Miniconda にパスをとおす
conda install binstar
conda install anaconda-client
conda install numpy==1.8.2 scipy==0.13.3 llvmlite
python -m pip install numba==0.35.0
```



