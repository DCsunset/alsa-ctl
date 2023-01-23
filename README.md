# alsa-ctl

[![PyPI](https://img.shields.io/pypi/v/alsa-ctl)](https://pypi.org/project/alsa-ctl/)

Control audio using ALSA API easily.

## Dependencies

`alsa-ctl` depends on the following programs in your PATH:

* `amixer`

## Installation

From pypi (recommended):

```sh
pip install alsa-ctl
```

From git repo (for dev version)

```sh
pip install git+https://github.com/DCsunset/alsa-ctl
```

Or clone and install locally (for dev):

```sh
git clone https://github.com/DCsunset/alsa-ctl
cd alsa-ctl
pip install .
```

## Usage

### CLI

Use the command `alsa-ctl` directly:

```sh
alsa-ctl --help
alsa-ctl get_card
alsa-ctl get_volume
```

See help messages for more usage.

### Library

```py
from alsa_ctl.lib import list_cards
print(list_cards())
```


## LICENSE

AGPL-3.0. Copyright notice:

    alsa-ctl
    Copyright (C) 2022-2023 DCsunset

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

