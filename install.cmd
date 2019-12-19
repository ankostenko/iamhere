REM We are installing dependencies
cd libs
for %%x in (dir *.whl) do py -3 -m pip install %%x
cd ..
set PYTHONPATH=%cd%
py -3 server/app.py