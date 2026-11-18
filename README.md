# rsyncer

Simple backup command. Uses `rsync` and `ssh`, with your `ssh` configs.

Need to write `.logs` for it to log.

Dependencies:
- `rsync`
- `ssh`

## Example Config

Default location in `~/.config/rsyncer.toml`.

```
[links]
[links.gitea]
source = "/doom/gitea"
destination = "chinook:/fins/rsyncer"
frequencies = ["daily", "monthly"]

[links.bibtheque]
source = "nanook:/home/doug/bibtheque"
destination = "/doom/rsyncer"
frequencies = ["daily", "monthly"]

[log]
path = "~/.logs/rsyncer.log"
```

## Usage

## For Development

To install locally for testing:

```
source pyenv/bin/activate
pip install -e .
```


