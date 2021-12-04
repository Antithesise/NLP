# CipherTool

CLI for helping decode substitution and transposition ciphers.


Substitution mode:
```
> z a        # assign the letter a to the letter z
> wig ing    # assign w to i, i to n, g to g etc.
> wig        # clear the letters assigned to w, i and g
> !          # enter Reverse mode
> :          # enter Ceaser Cipher mode (Reverse Mode is still active)
> +          # increment shift in Ceaser chiper by 1
> !          # exit Reverse mode (Ceaser Cipher Mode is still active)
> -          # decrement shift in Ceaser cipher by 1
> :          # exit Ceaser Cipher mode
> ?          # clear entire cipher
>            # exit program
```

Transposition mode:
```
> 4          # set grid to width 4 and place letters into it
> 8          # set grid to width 8 and place letters into it
>            # exit program
```


Substitution and Transposition mode can be switched between with '#'
```
> #          # swap to Substitution/Transposition mode
```