const re = /^__version__ = "(\d\.\d\.\d)"/;

function readVersion(contents) {
	const matches = contents.match(re);
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
	// read version
	packageFiles: [tracker],
	// write version
	bumpFiles: [tracker]
};
