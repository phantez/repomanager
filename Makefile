
DOCFILES	= AUTHORS COPYING TODO README

default : all

all :
	echo "not yet implemented"

install :
	python setup.py install
	
develop :
	python setup.py develop

clean :
	-find -name "*.pyc" -exec rm -f {} \;
	-rm -Rf RepoManager.egg-info
