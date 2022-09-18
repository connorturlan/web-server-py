# Python Web Server (inc. File Server)

## Setup

This repository implements a Webpage host and File Server at the specified `hostname` with:

> `main.py <hostname> <port>`

This servers as an example of what this python module can be used to create.

## MVP

### Web Server

Create a modular web server that allows for adding independently running plugins/modules.

### File server

The file server is to include full **CRUD** functionality for files within the specified shared folder.

1. **CREATE** - upload:
    - send files from the client's file system to the server's.
2. **READ** - download:
    - send files from the server's file system to the client's.
3. **UPDATE** - cut/copy/paste:
    - cut/copy files within the server's file system and paste them in another directory.
4. **DELETE** - delete:
    - remove a file from the server's file system permanently.

## Implementation

### Web Server

The web server has three classes:

-   WebModule
-   HTTPController
-   WebServer

#### `WebModule`

WebModule is a class that implement the functionality for the WebServer. It includes methods for each HTTP/1.1 method which can be modified to provide custom behavior.

> Usage: `WebModule(<path>, <url_params>)`

-   `path` denotes the url that will trigger the module.
-   `url_params` signifies how parameters are mapped by the module. All parts of the url following the mapped params are accessible with the `''` key.

Modules are executed in the order that they are added to the WebServer. If two modules share the same path, only the first will be run by default. In this case the first module is **terminal**.

All modules at the end of their HTTP method implementation must return `True` or `False`, signalling a terminal or non-terminal module. Non-terminal modules will not block the execution of any following modules.

#### `HTTPController`

#### `WebServer`

### File Server

#### `FileServer`

#### `WebpageServer`

## Known Issues

## Retrospective

## Future Plans

-   Remove default terminal behaviour for `WebModule`.
-   Implement PATCH and DELETE for the `FileServer` module.
-   Implement OPTION for preflight CORS requests in the base module for simplicity.
-   Allow toggling and configuring CORS within the `WebModule` or `HTTPController`.
-   Use `os.path.exists` instead of `try-catch` for existence checking.

## License

CC by attribution non-commercial, derivatives allowed.

## Contributions

Made by Connor Turlan 2022.
