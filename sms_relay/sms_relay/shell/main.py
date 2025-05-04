import click
import IPython

from sms_forwarding.shell.utils.import_models import import_all_models


@click.command()
@click.option("-m", "--models", is_flag=True, help="Load models before launching the shell")
def main(models: bool):
    """Launch an IPython shell with optional model loading."""
    if models:
        import_all_models()
    IPython.embed(banner1="SMS Relay shell")

if __name__ == "__main__":
    main()