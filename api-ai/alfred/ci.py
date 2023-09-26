import alfred


@alfred.command('ci', help="use continuous integration process")
@alfred.option('--verbose', '-v', is_flag=True, help='show detailed information on the execution')
def ci(verbose=False) -> None:
    alfred.invoke_command("lint")
    alfred.invoke_command("tests:units", verbose=verbose)
    alfred.invoke_command("tests:acceptances", verbose=verbose)
    alfred.invoke_command("tests:migrations", verbose=verbose)
