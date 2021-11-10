# ![Dragoman](https://github.com/SDM-TIB/Dragoman/blob/master/images/dragoman.png "Dragoman")
An Optimized, RML-engine-agnostic Interpreter for Functional Mappings. It planns the optimized execution of FnO functions integrated in RML mapping rules, interprets and transforms the rules into function-free ones efficiently. Since Dragoman is engine-agnostic it can be adopted by any RML-compliant Knowledge Graph creation framework.

## You can use Dragoman with your own library of functions! Here is [how](https://tib.eu/cloud/s/ikjiHyf8RNrEHSY):
1. Make a copy of functions.py that is located in ./Interpreter/ and rename it (we consider it as new_function_script.py)
2. Edit new_function_script.py by adding your functions definitions following the sctructure provided in the script and save the chnages
3. Go to the connection.py and replace ".functions" with ".new_function_script" at line 6 and save the changes

That's it! You are ready to go :)

# Installing and Running the Dragoman 
From PyPI (https://pypi.org/project/dragoman-tool/):
```
python3 -m pip install dragoman-tool
python3 -m Interpreter -c /path/to/config/file
```
From Docker (sdmtib/dragoman):
```
docker run -d -p 4000:4000 -v /path/to/yourdata:/data dragoman
Send a GET request with the configuration file to Dragoman container.

curl localhost:4000/mapping_transformation/data/your-config-file.ini
```

## Version 
```
1.0
```

## License
This work is licensed under Apache 2.0

# Authors
- Samaneh Jozashoori (samaneh.jozashoori@tib.eu) 
- Enrique Iglesias (iglesias@l3s.de) 
- Maria-Esther Vidal (maria.vidal@tib.eu)
