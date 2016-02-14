build: components static/js/ExifLocation.js
	@component static/js --dev --name exiflocation
	@component static/js --standalone ExifLocation --name exiflocation.standalone

components: component.json
	@component install --dev

clean:
	rm -fr build components

.PHONY: clean build
