# scrapper-ipi.be
simple script to retrieve the list of Belgian real estate agents.
It's not beautiful code but it's functional.


## how to use
```python3 ./get_realtor.py```


## how to configure
As long as now, you have to modify the code to change the parameters. (sorry about that).
The good news is that all parameter changes are done in one place: get_realtor.py line 125 (at the end of the file)

The line is:
```python3
scrapper(preformat_url=preformat_url, zipcode_list=belgium_zipcode.zipcode_list, outputdir="./data", debug=True)
```

### - specify a postal code list
zipcode_list is the argument to change

example:
```python3
scrapper(preformat_url=preformat_url, zipcode_list=[4000, 4020, 4030], outputdir="./data", debug=True)
```

### - change output directory
outputdir is the argument to change.

*WARNING:* - the directory must exist (with the rights in writing) before the execution of the script.

example:
```python3
scrapper(preformat_url=preformat_url, zipcode_list=belgium_zipcode.zipcode_list, outputdir="./42", debug=True)
```

### - disable standard output
outputdir is the argument to change to "False" value.

example:
```python3
scrapper(preformat_url=preformat_url, zipcode_list=belgium_zipcode.zipcode_list, debug=False)
```


## Todo
- add comments.
- add configurable parameters (output folder, specific postal code ...)

