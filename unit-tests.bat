if ["%1"]==["coverage"] goto :coverage else goto :regular

:regular
nosetests --where=ai
goto :end

:coverage
nosetests --where=ai --with-coverage --cover-package=ai
goto :end

:end