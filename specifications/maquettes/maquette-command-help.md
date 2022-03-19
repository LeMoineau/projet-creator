
usage: projet-creator <command> [arguments]

Manage your project development.

options:
-h, --help                  Print this usage information.
-v, --verbose               Noisy logging, including all shell commands executed.
                            If used with "--help", shows hidden options. If used with "flutter doctor", shows additional diagnostic
                            information. (Use "-vv" to force verbose logging in those cases.)
-d, --device-id             Target device id or name (prefixes allowed).
    --version               Reports the version of this tool.
    --suppress-analytics    Suppress analytics reporting when this command runs.

Manage local project:
  create            Create a new project repository
  add               Add a task to the project
  rm                Remove a task from the project
  check             Check/Uncheck a task from the project
  help              Show command help

Manage global projects:
  global add        Add a task for all the next projects
  global rm         Remove a task for all the next projects

Run "projet-creator help <command>" for more information about a command.