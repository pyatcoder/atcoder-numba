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

AtCoder の場合であれば、Python3 で提出したコードをそのまま（型指定をしていなければ型指定は必要）提出できるので便利です。


## インストール

```
pip install git+https://github.com/pyatcoder/atcoder-numba
```

## 使い方

Python のコードは、作成の過程でモジュールとして import するので、`if __name__ == "__main__":`を使用して、スクリプトが実行されない形式にしておく必要があります。

- atcoder-numba compile inputs  
型シグネチャ付きの `@jit` デコレータのある関数をコンパイルして、numba_modules という名前の拡張モジュールを作成します。作成されるファイルの名前は OSによって異なります。Linux で Python 3.7 の場合であれば、numba_modules.cpython-37m-x86_64-linux-gnu.so という名前になります。  
Python のコードの方は、inputs が main.py の場合であれば、main_aot.py というファイルを作成します。作成された main_aot.py は、numba を import せずに実行できます。

- atcoder-numba submit inputs  
compile コマンドでは２つのファイルができますが、submit の方では、拡張モジュールを gzip して後 Base64 でエンコードして、main_aot.py に添付することで、ファイルを1つにします。

`atcoder-numba submit`コマンドで作成した Python のコードは、AtCoder にそのまま提出することができます。実行に Numba は必要がないので、現在の AtCoder でも動きます。sample ディレクトリに abc129の問題Dとabc130の問題Eのサンプルコードを置いてあります。main_aot.py の方を提出すれば、実際に AC できます。

ただし、バイナリーコードは機種依存です。使用するマシンは、AtCoder のサーバーと同じ OS である linux を使う必要があります。また、glibc のバージョンを合わせておかないとエラーになります。sample ファイルを作成した環境を参考までに書いておきます。

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

## ライセンス

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

