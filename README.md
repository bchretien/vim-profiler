vim-profiler
============

Utility script to profile (n)vim (e.g. startup). For now, only startup time
w.r.t. plugins is analyzed. The plugin directory is automatically found.

The script is inspired from [vim-plugins-profile][vim-plugins-profile], but
only depends on Python.

## Dependencies

Required:

- Python 2 or Python 3,
- vim or neovim.

Optional:

- Matplotlib (for bar plot)

## Usage

To list the available options:
```sh
$ vim-profiler -h
```

```txt
usage: vim-profiler.py [-h] [-o CSV] [-p] [-n N] [exe]

Analyze startup times of vim/neovim plugins.

positional arguments:
  exe         vim or neovim executable

optional arguments:
  -h, --help  show this help message and exit
  -o CSV      Export result to a csv file
  -p          Plot result as a bar chart
  -n N        Number of plugins to list in the summary
```

The text summary looks like this:

```txt
$ vim-profiler.py nvim

Running nvim to generate startup logs... done.
Loading and processing logs... done.
=====================================
Top 10 plugins slowing nvim's startup
=====================================
1       4.559   vim-fugitive
2       4.162   tcomment_vim
3       3.936   vim-hybrid
4       2.922   lightline.vim
5       1.551   supertab
6       1.522   vim-sneak
7       1.100   ultisnips
8       0.929   fzf.vim
9       0.916   fzf
10      0.877   vim-surround
=====================================
```

As for the plot (using Matplotlib):

![plot](https://raw.githubusercontent.com/bchretien/vim-profiler/master/.images/plot.png "Plot")

## License

GPLv3

[vim-plugins-profile]: https://github.com/hyiltiz/vim-plugins-profile
