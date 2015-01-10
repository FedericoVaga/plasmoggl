
APP=.
OPENDESKTOP=plasmoggl-1.1.plasmoid

all:
	cp toggl-cli/toggl.py contents/code/toggl.py
clean:
	rm -rf $(OPENDESKTOP) $(OPENDESKTOP).tar.gz contents/code/toggl.py

install: clean all
	plasmapkg -t plasmoid -i $(APP)

update: clean all
	plasmapkg -t plasmoid -u $(APP)

uninstall:
	plasmapkg -t plasmoid -r $(APP)

opendesktop: all
	mkdir $(OPENDESKTOP)
	cp -r contents metadata.desktop LICENSE README.md Makefile $(OPENDESKTOP)
	tar -czf $(OPENDESKTOP).tar.gz $(OPENDESKTOP)
	rm -rf $(OPENDESKTOP)
