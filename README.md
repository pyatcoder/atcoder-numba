# AtCoder Numba AOT Tools

Numba の JIT を使用したコードを AOT(事前)コンパイルするためのミニツールです。以下のような Numba の JIT を使ったコードがあった時に、AOT コンパイルをしようと思ったら、普通は`@cc.export`というデコレータを付ける必要があります。それを付けずに AOT コンパイルをします。

```
@jit(nopython=True)
def fib(n):
    if n < 2:
        return n
    else:
        return fib(n - 2) + fib(n - 1)
```

AtCoder の場合であれば、Python3 で提出したコードをそのまま提出できるので便利です。


## インストール

```
pip install git+https://github.com/pyatcoder/atcoder-numba
```

## 使い方

AtCoder に提出するコードであれば、Python のコードと同じディレクトリ内に`in_1.txt`という名前のファイルを作成して、入力例のデータを入れておけば、
signature(型指定)をしなくても `@njit`をつけるだけで AOT コンパイルができます。in_1.txt ファイルがあれば、in_1.txt を stdin に設定してコードをインポートし main() 関数を実行します。なければ、コードのインポートだけをします。

なお、`in_1.txt`は、[AtCoder Tools](https://github.com/kyuridenamida/atcoder-tools) のデフォルトの入力例データの保存ファイル名です。

- atcoder-numba compile inputs  
`@jit` デコレータのある関数をコンパイルして、numba_modules という名前の拡張モジュールを作成します。作成されるファイルの名前は OSによって異なります。Linux で Python 3.7 の場合であれば、numba_modules.cpython-37m-x86_64-linux-gnu.so という名前になります。  
Python のコードの方は、inputs が main.py の場合であれば、main_aot.py というファイルを作成します。作成された main_aot.py は、numba を import せずに実行できます。

- atcoder-numba embed inputs  
compile コマンドでは２つのファイルができますが、submit の方では、拡張モジュールを gzip して後 Base64 でエンコードして、main_aot.py に添付することで、ファイルを1つにします。

`atcoder-numba embed`コマンドで作成した Python のコードは、AtCoder にそのまま提出することができます。実行に Numba は必要がないので、現在の AtCoder でも動きます。sample ディレクトリに abc129の問題Dとabc130の問題Eのサンプルコードを置いてあります。main_aot.py の方を提出すれば、実際に AC できます。

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

