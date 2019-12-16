# br: A Browser controller
# Setup
## Using default commands
    Create this file under PATH and make it executable.

```python
#!/usr/bin/env python3
from br.default import run_default

#Replace 'port' with the number you prefer.
run_default(port) 
```

## Writing your own init command

``` python
#!/usr/bin/env python3

from brws import run
from brws.default import default_commands, run_default
from brws.lib import User

commands = default_commands

with User("USERNAME", "PASSWORD") as u:
    u.add("github", "https://github.com/login", "login_field", "password")
    
run("Chrome", 54422, commands)

```
  
  Compose the `commands` variable and pass it to `run`.

# Default commands

| Command | Action                             | Equevalent shortcut in Chrome |
| g       | Visit the url                      | Control-L + ... +Enter        |
| g       | Click the link with text           |                               |
| b       | Go back                            | Alt-LeftArrow                 |
| g       | Go forward                         | Alt-RightArrow                |
| signup  | Click the link with text 'Sign up' |                               |
| signin  | Click the link with text 'Sign in' |                               |
| d       | scroll half a page down            | PageUp                        |
| u       | scroll half a page up              | PageDown                      |
| ddg     | Search with DuckDuckGo             |                               |
| google  | Search with Google                 |                               |
| get_pid | Show the pid of the server         |                               |
| get_url | Show the url of the browser        |                               |
