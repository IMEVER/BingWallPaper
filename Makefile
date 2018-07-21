.PHONY:deb clean

PREFIX = /usr
DESTDIR = dist/
BUILDDIR = build

install:
	mkdir -p ${DESTDIR}${BUILDDIR}
	mkdir -p ${DESTDIR}${BUILDDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${BUILDDIR}${PREFIX}/share/applications
	mkdir -p ${DESTDIR}${BUILDDIR}${PREFIX}/share/icons/hicolor/scalable/apps
	mkdir -p ${DESTDIR}${BUILDDIR}${PREFIX}/share/bingwallpaper
	mkdir -p ${DESTDIR}${BUILDDIR}${PREFIX}/share/doc/bingwallpaper
	find src/ -name *.pyc | xargs rm -f
	cp -r resource src ${DESTDIR}${BUILDDIR}${PREFIX}/share/bingwallpaper
	cp BingWallPaper.desktop ${DESTDIR}${BUILDDIR}${PREFIX}/share/applications
	cp resource/bing-wallpaper.png ${DESTDIR}${BUILDDIR}${PREFIX}/share/icons/hicolor/scalable/apps
	chmod a+x ${DESTDIR}${BUILDDIR}${PREFIX}/share/bingwallpaper/src/App.py
	cp bingwallpaper ${DESTDIR}${BUILDDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${BUILDDIR}/var/log/bingwallpaper/
	cp copyright ${DESTDIR}${BUILDDIR}${PREFIX}/share/doc/bingwallpaper/copyright
	cp -r DEBIAN ${DESTDIR}${BUILDDIR}/

clean:
	rm -rf ${DESTDIR}

deb:clean install
	cd ${DESTDIR};\
	fakeroot dpkg -b ${BUILDDIR} bingwallpaper_2.0.1.deb
