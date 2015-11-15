KeepUp is a **very** simple command-line tool for helping to have things up-to-date.

# Usage

KeepUp simpy stores in a text file a tag and a timestamp
You can add a tag, display all tags stored, display tags older than an amount of time, and update a tag's timestamp.

To add a tag:

```
KeepUp -a <TAG>
```

To display all stored tags:

```
KeepUp -l
```

To display tags older than <AMOUNT-OF-TIME>:

```
KeepUp -o <AMOUNT-OF-TIME>
```


where amount of time is written like a repetition of **<num><id>** where **<id>** is a letter of {s,m,h,d,w,M,Y} for second, minute, hour, day, week, month, years.
So that if you want to see tags older than 2 weeks 3 days 4 hours and 5 minutes, write:

```
KeepUp -o 2w3d4h5m
```


# Install

To install it, you need to use Autotools with python support.
First of all, you have to get the source code, **cd** inside the main tree and hit:

```
aclocal
autoconf
automake
./configure
make
sudo make install
```

Easy, right?

## Fine tuning

A usefull feature of autotools is the capability to install the whole things in a use directory (avoiding usage of sudo stuff). Instead of `./configure`, use `./configure --prefix=<PATH-YOU-HAVE-ACCESS>`.

## Generate documentation

If you want to generate documentation (usefull for developpers, not for standard users) use `make doxygen-doc` after `make` command. You'll need support for dowygen with autotools.


# Todo

First of all, the project needs some documentation.

The Python implementation is not good enough. The items might have their own class.

The output of the program needs better formating and a flag to have a *machine* formating, which could be used to feed another program.

Their is no way to remove an existing tag. Consider adding this feature.
