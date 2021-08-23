2021-08-23
Becase the go-python3 repo only support the python version 3.7 at present,
if you want to import the algorithm module for embedded python, you have to downgrade the python to 3.7
to compile the "egg" file, or you can utilize the venv to do this job.

after you get py3.7 egg file, remember add the path of the embedded python so that it can know
where to find the library.