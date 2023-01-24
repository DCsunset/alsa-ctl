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

import subprocess
import sys
import re

VOLUME_TYPES = ("Playback", "Capture")

global_options = {
	# None means using the default card
	"card": None,
	# Possible scontrols used to change volume
	"volume_scontrols": ["Master", "Headset", "Capture", "PCM"]
}

def run_command(cmd: list[str]) -> str:
	return subprocess.check_output(cmd).decode(sys.stdout.encoding)

# Build card options
def card_options(card: str | None):
	options = []
	if card is not None:
		options.extend(["-c", card])
	return options

# List all sound cards
# max_num <= 0 means no limit
def list_cards(max_num: int = 0) -> list[str]:
	with open("/proc/asound/cards", "r") as f:
		out = f.read()
	regex = re.compile(r"\[\s*(.+?)\s*\]")
	cards = regex.findall(out)
	if max_num > 0:
		n = min(max_num, len(cards))
		# prioritize cards from the end
		# because they are external
		cards = cards[-n:]
	return cards
   
# Get scontrols of a sound card
def get_scontrols(card: str | None) -> list[str]:
	try:
		out = run_command(["amixer", *card_options(card), "scontrols"])

		lines = out.splitlines()
		p = re.compile(r"'(.+)'")
		names = []
		for l in lines:
			# find the last occurrence of the quoted name
			name = p.search(l).groups()[-1]
			names.append(name)
		return names
	except Exception as e:
		print(e, file=sys.stderr)

	# return empty on failure
	return []

# Get volume types of a specific scontrol (check for Playback and Capture)
def get_scontrol_volume_types(card: str | None, scontrol: str) -> list[str]:
	try:
		out = run_command(["amixer", *card_options(card), "sget", scontrol])
			
		types = []
		for volume_type in VOLUME_TYPES:
			regex = re.compile(f"{volume_type}.*\\[\\d?\\d?\\d%\\]")
			# find the last occurrence of the quoted name
			if len(regex.findall(out)) > 0:
				types.append(volume_type)
		return types
	except Exception as e:
		print(e, file=sys.stderr)

	# return empty on failure
	return []

	
# Get current volume scontrol and card for amixer
def get_volume_scontrol(card: str | None, volume_type: str) -> str:
	scontrols = get_scontrols(card)

	# possible scontrols for volume
	for sc in global_options["volume_scontrols"]:
		if sc in scontrols:
			types = get_scontrol_volume_types(card, sc)
			if volume_type in types:
				return sc
	
	print(f"No suitable amixer volume control", file=sys.stderr)
	return ""

def get_volume_cmd(volume_type: str) -> list[str]:
	card = global_options["card"]
	scontrol = get_volume_scontrol(card, volume_type)
	return ["amixer", *card_options(card), "sget", scontrol]

def toggle_cmd(volume_type: str) -> list[str]:
	card = global_options["card"]
	scontrol = get_volume_scontrol(card, volume_type)
	return ["amixer", *card_options(card), "sset", scontrol, volume_type, "toggle"]

def lower_volume_cmd(volume_type: str, step: int) -> list[str]:
	card = global_options["card"]
	scontrol = get_volume_scontrol(card, volume_type)
	return ["amixer", *card_options(card), "sset", scontrol, volume_type, f"{step}%-"]

def raise_volume_cmd(volume_type: str, step: int) -> list[str]:
	card = global_options["card"]
	scontrol = get_volume_scontrol(card, volume_type)
	return ["amixer", *card_options(card), "sset", scontrol, volume_type, f"{step}%+"]

