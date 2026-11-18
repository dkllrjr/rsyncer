import click
from shutil import which
from pathlib import Path
import tomllib
import subprocess
from datetime import datetime
from time import sleep
import importlib.metadata

#  ──────────────────────────────────────────────────────────────────────────
# global variables

rsyncer_version = importlib.metadata.version('rsyncer')
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

#  ──────────────────────────────────────────────────────────────────────────
# global functions

def _log(config, content):
    with open(Path(config['log']['path']).expanduser(), 'a') as file:
        file.write(content + '\n')


def _run(source, destination, frequency):
    cmd = ['rsync', '--progress', '-r', source, destination + '/' + frequency]
    subprocess.run(cmd)

#  ──────────────────────────────────────────────────────────────────────────
# global options

force_option = click.option('--force', is_flag=True, default=False, show_default=True, help='Force command', type=bool)

#  ──────────────────────────────────────────────────────────────────────────
# base command

# done for the config
@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.version_option(rsyncer_version)
@click.option('-c', '--config', default='~/.config/rsyncer.toml', type=str, help="Config file path", show_default=True)
@click.pass_context
def rsyncer(ctx, config):
    """Simple and quick backup program."""

    # check if rsync and ssh are available
    if which('rsync') and which('ssh'):
        pass
    else:
        raise click.ClickException('rsync and ssh not found')

    # setting up config
    ctx.ensure_object(dict)

    config = Path(config).expanduser()
    if config.exists():

        with open(config, 'rb') as file:
            toml = tomllib.load(file)

        # required config options
        required = ['source', 'destination', 'frequencies']
        for key in required:
            for link in toml['links']:
                if key not in toml['links'][link]:
                    raise click.ClickException('Config requires "' + key + '" to be set for link "' + link + '".')

        # setting config
        ctx.obj = toml

    else:
        raise click.ClickException('No config file, exiting.')

#  ──────────────────────────────────────────────────────────────────────────
# run command

@rsyncer.command('run', short_help="Run rsyncer.")
@click.option('-s', '--sleep', 'loop_sleep', default=3, help="Sleep time in hours within run loop.", type=int)
@force_option
@click.pass_obj
def run(obj, loop_sleep, force):
    """Run"""

    def _run_loop(config, current_time, old_time, force):
        for link in config['links']:
            source = config['links'][link]['source']
            destination = config['links'][link]['destination']

            for frequency in config['links'][link]['frequencies']:
                if frequency == 'daily':
                    if current_time.day > old_time.day or force:
                        _run(source, destination, frequency)
                        _log(config, current_time.isoformat() + ' ' + link + ', ' + source + ', ' + destination + ', ' + frequency)

                elif frequency == 'weekly':
                    if current_time.weekday() == 6 or force: 
                        _run(source, destination, frequency)
                        _log(config, current_time.isoformat() + ' ' + link + ', ' + source + ', ' + destination + ', ' + frequency)

                elif frequency == 'monthly':
                    if current_time.day == 1 or force: 
                        _run(source, destination, frequency)
                        _log(config, current_time.isoformat() + ' ' + link + ', ' + source + ', ' + destination + ', ' + frequency)


    # run time loop
    old_time = datetime.now()
    while True:
        current_time = datetime.now()

        if current_time > old_time or force:
            _run_loop(obj, current_time, old_time, force)

            if force:
                return

        old_time = current_time
        sleep(loop_sleep*3600) # waits for 3 hours
