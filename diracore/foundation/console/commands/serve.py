import click
import subprocess
from diracore.main import cli
from click.core import Context, Option
from diracore.main import config

def flag_with_value(ctx: Context, param: Option, value):
    param.name = param.opts[0]
    return value

@cli.command("serve")
@click.option('--reload', is_flag=True)
@click.option('--proxy-headers', is_flag=True)
@click.option('--port', callback=flag_with_value)
@click.option('--host', callback=flag_with_value)
@click.option('--ssl-keyfile', callback=flag_with_value)
@click.option('--ssl-certfile', callback=flag_with_value)
@click.option('--forwarded-allow-ips', callback=flag_with_value)
def serve(**args):
    flags = []
    params = []
    for arg,value in args.items():
        if isinstance(value, bool):
            if value == True:
                flags.append('--'+arg)
        elif value != None:
            params.append(arg)
            params.append(value)
            
    if "--proxy_headers" in flags:
        i = flags.index("--proxy_headers")
        flags[i] = "--proxy-headers"

    if '--host' not in params:
        params += ['--host', config('app.host', 'localhost')]
    if '--port' not in params:
        params += ['--port', config('app.port', '8000')]

    subprocess.run(['uvicorn', 'dira:serve']+flags+params)