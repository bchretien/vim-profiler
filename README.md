vim-profiler
============

[![Build Status](https://travis-ci.org/bchretien/vim-profiler.svg?branch=master)](https://travis-ci.org/bchretien/vim-profiler)

Utility script to profile (n)vim (e.g. startup). For now, only startup time
w.r.t. plugins is analyzed. The plugin directory is automatically found.

The script is inspired from [vim-plugins-profile][vim-plugins-profile], but
only depends on Python. It supports the following features:

- run any vim/neovim command,
- detect the plugin directory automatically,
- handle GUI versions,
- compute the average time/standard deviation over multiple runs,
- export the result to a CSV file,
- plot a bar chart.

## Dependencies

Required:

- Python 2 or Python 3,
- vim or neovim.

Optional:

- Matplotlib (for bar plot)

## Usage

To list the available options:
```sh
$ vim-profiler.py -h
```

```txt
usage: vim-profiler.py [-h] [-o CSV] [-p] [-s] [-n N] [-r RUNS] ...

Analyze startup times of vim/neovim plugins.

positional arguments:
  cmd         vim/neovim executable or command

optional arguments:
  -h, --help  show this help message and exit
  -o CSV      Export result to a csv file
  -p          Plot result as a bar chart
  -s          Consider system plugins as well (marked with *)
  -n N        Number of plugins to list in the summary
  -r RUNS     Number of runs (for average/standard deviation)
```

The text summary looks like this:

```txt
$ vim-profiler.py nvim

Running nvim to generate startup logs... done.
Loading and processing logs... done.
Plugin directory: /home/user/.config/nvim/plugged
=====================================
Top 10 plugins slowing nvim's startup
=====================================
1         4.559   vim-fugitive
2         4.162   tcomment_vim
3         3.936   vim-hybrid
4         2.922   lightline.vim
5         1.551   supertab
6         1.522   vim-sneak
7         1.100   ultisnips
8         0.929   fzf.vim
9         0.916   fzf
10        0.877   vim-surround
=====================================
```

As for the plot (using Matplotlib):

```
$ vim-profiler.py -p -r 10 nvim
=====================================
Top 10 plugins slowing nvim's startup
=====================================
1         3.326   vim-fugitive
2         2.936   tcomment_vim
3         2.315   vim-hybrid
4         1.751   lightline.vim
5         0.959   vim-sneak
6         0.943   supertab
7         0.542   vim-surround
8         0.536   fzf.vim
9         0.450   fzf
10        0.434   auto-pairs
=====================================
```

![plot](https://raw.githubusercontent.com/bchretien/vim-profiler/master/.images/plot.png "Plot")

You can also use a custom command. Simply write it after the other options:

```txt
$ vim-profiler.py vim -u NONE

Running vim to generate startup logs... done.
Loading and processing logs...
No plugin found. Exiting.
```

This is particularly useful if you want to test your plugin manager's lazy
loading feature:

```txt
$ vim-profiler.py -n 5 nvim foo.cc

Running nvim to generate startup logs... done.
Loading and processing logs... done.
Plugin directory: /home/user/.config/nvim/plugged
====================================
Top 5 plugins slowing nvim's startup
====================================
1         5.613   vim-cpp-enhanced-highlight
2         3.457   vim-fugitive
3         2.864   tcomment_vim
4         2.389   vim-hybrid
5         1.870   lightline.vim
====================================

$ vim-profiler.py -n 5 nvim foo.cc -c ":exec ':normal ia' | :q\!"

Running nvim to generate startup logs... done.
Loading and processing logs... done.
Plugin directory: /home/user/.config/nvim/plugged
====================================
Top 5 plugins slowing nvim's startup
====================================
1       144.766   ultisnips
2        95.977   YouCompleteMe
3        11.408   vim-cpp-enhanced-highlight
4         3.463   vim-fugitive
5         2.992   tcomment_vim
====================================
```

Here `ultisnips` and `YouCompleteMe` were only loaded after entering insert
mode.

## License

GPLv3

[vim-plugins-profile]: https://github.com/hyiltiz/vim-plugins-profile
