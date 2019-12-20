REM We are installing dependencies
cd libs
for %%x in (dir *.whl) do py -3 -m pip install --no-index --find-links=%cd% %%x
py -3 -m pip install --no-index --find-links=%cd% SQLAlchemy-1.3.12.tar.gz
cd ..
set PYTHONPATH=%cd%
py -3 server/app.py fill