
yaml_url=www.yaml.de/download/release/yaml412-130728.zip
jquery_url=https://code.jquery.com/jquery-3.4.1.min.js

all: src/html/css/yaml src/html/js/jquery.min.js

ext/yaml412-130728.zip:
	wget -O $@ ${yaml_url}

ext/yaml: ext/yaml412-130728.zip
	mkdir $@
	unzip $< -d $@
src/html/css/yaml: ext/yaml
	cp -r $</yaml412-130728/yaml $@
src/html/js/jquery.min.js: 
	wget -O $@ ${jquery_url}
clean:
	rm  -rf ext/*
	rm -rf src/html/js/jquery.min.js
	rm -rf src/html/css/yaml
