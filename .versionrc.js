const re = /^__version__ = "(\d\.\d\.\d)"/gm;

function readVersion(contents) {
	const matches = re.exec(contents);
	return matches[1];
}

function writeVersion(contents, version) {
	return contents.replace(re, `__version__ = "${version}"`);
}

const tracker = {
	filename: "alsa_ctl/_version.py",
	updater: {
		readVersion,
		writeVersion
	}
};

module.exports = {
	packageFiles: [tracker]
};
