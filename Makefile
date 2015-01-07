
APP=plasmoggl

all:
	cp toggl-cli/toggl.py plasmoggl/contents/code/toggl.py

install: all
	plasmapkg -t plasmoid -i $(APP)

update: all
	plasmapkg -t plasmoid -u $(APP)
uninstall:
	plasmapkg -t plasmoid -r $(APP)