# alsa-ctl
# Copyright (C) 2022-2023 DCsunset
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import re
from pathlib import Path
import subprocess
import argparse
import importlib.resources as pkg_resources
from ._version import __version__
from .lib import get_volume_cmd, toggle_cmd, raise_volume_cmd, lower_volume_cmd, list_cards, VOLUME_TYPES, global_options, run_command

def error(msg: str):
	print(msg, file=sys.stderr)
	sys.exit(1)

def get_volume(volume_type: str):
	if volume_type not in VOLUME_TYPES:
		error(f"Invalid volume type: {volume_type}")

	out = run_command(get_volume_cmd(volume_type))
	# filter volume of different volume types
	regex = re.compile(f"{volume_type}.*\\[\\d?\\d?\\d%\\]")
	print("\n".join(
		map(
			lambda l: l.strip(),
			filter(
				lambda l: regex.search(l) is not None,
				out.splitlines()
			)
		)
	))


def main():
	global_config = {
		"formatter_class": argparse.ArgumentDefaultsHelpFormatter
	}

	parser = argparse.ArgumentParser(
		description="Control audio with ALSA API easily via CLI",
		**global_config
	)
	parser.add_argument("-c", "--card", help="control a specific sound card (using the default card if not specified)")
	parser.add_argument("--vs", "--volume-scontrols", action="append", help='possible scontrols used to change volume. If not set, use ["Master", "Headset", "Capture", "PCM"]')
	parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
	
	# For commands
	sub_parser = parser.add_subparsers(
		dest="command",
		metavar="command",
		help="command to execute",
		required=True
	)

	# list cards
	list_cards_parser = sub_parser.add_parser(
		"list_cards",
		help="list available sound devices",
		**global_config
	)
	list_cards_parser.add_argument(
		"max_num",
		nargs="?",
		default=0,
		type=int,
		help="max number of cards to display (non-positive num means no limit)"
	)
	# get_volume
	get_volume_parser = sub_parser.add_parser(
		"get_volume",
		help="get current volume",
		**global_config
	)
	get_volume_parser.add_argument(
		"volume_type",
		nargs="?",
		metavar="type",
		default="Playback",
		choices=["Playback", "Capture"],
		help="get volume of a specific type [choices: %(choices)s]"
	)
	# toggle
	toggle_parser = sub_parser.add_parser(
		"toggle",
		help="toggle (mute/unmute)",
		**global_config
	)
	toggle_parser.add_argument(
		"volume_type",
		nargs="?",
		metavar="type",
		default="Playback",
		choices=["Playback", "Capture"],
		help="change volume of a specific type [choices: %(choices)s]"
	)
	# raise_volume
	raise_volume_parser = sub_parser.add_parser(
		"raise_volume",
		help="raise volume",
		**global_config
	)
	raise_volume_parser.add_argument(
		"volume_type",
		nargs="?",
		metavar="type",
		default="Playback",
		choices=["Playback", "Capture"],
		help="change volume of a specific type [choices: %(choices)s]"
	)
	raise_volume_parser.add_argument(
		"-s",
		"--step",
		default=2,
		type=int,
		help="raise volume by a percentage"
	)
	# lower_volume
	lower_volume_parser = sub_parser.add_parser(
		"lower_volume",
		help="lower volume",
		**global_config
	)
	lower_volume_parser.add_argument(
		"volume_type",
		nargs="?",
		metavar="type",
		default="Playback",
		choices=["Playback", "Capture"],
		help="change volume of a specific type [choices: %(choices)s]"
	)
	lower_volume_parser.add_argument(
		"-s",
		"--step",
		default=2,
		type=int,
		help="lower volume by a percentage"
	)
	# completion
	completion_parser = sub_parser.add_parser(
		"completion",
		help="install completion script",
		**global_config
	)
	completion_parser.add_argument(
		"--shell",
		default="zsh",
		choices=["zsh"],
		help="shell type [choices: %(choices)s]"
	)
	completion_parser.add_argument(
		"directory",
		type=str,
		help="directory to install"
	)

	# Process args
	args = parser.parse_args()
	cmd = args.command
	global_options["card"] = args.card
	if args.vs is not None:
		global_options["volume_scontrols"] = args.vs

	try:
		if cmd == "list_cards":
			print("\n".join(list_cards(args.max_num)))
		elif cmd == "get_volume":
			get_volume(args.volume_type)
		elif cmd == "toggle":
			run_command(toggle_cmd(args.volume_type))
		elif cmd == "raise_volume":
			run_command(raise_volume_cmd(args.volume_type, args.step))
		elif cmd == "lower_volume":
			run_command(lower_volume_cmd(args.volume_type, args.step))
		elif cmd == "completion":
			# resources must be included in package_data in setup.py
			if args.shell == "zsh":
				filename = "_alsa-ctl"
			else:
				error(f"Shell {args.shell} not supported")

			data = pkg_resources.read_text("alsa_ctl.completion", filename)
			dst = Path(args.directory).joinpath(filename)
			with open(dst, "w+") as f:
				f.write(data)
			print(f"Completion script installed at {dst}")
	except Exception as e:
		error("Error executing command")

if __name__ == "__main__":
	main()
