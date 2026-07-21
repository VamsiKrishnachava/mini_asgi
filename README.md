# Mini ASGI

A minimal ASGI framework built for learning how ASGI servers (such as Uvicorn) interact with Python web applications.

## Assumptions

The current version has the following assumptions:

- All endpoint responses are Python dictionaries (`dict`).
- Only successful (`200 OK`) responses are supported.
- `404 Not Found` is handled for unknown routes.
- Advanced features such as middleware, request validation, templating, streaming, and different response types are not yet implemented.

## Usage

Refer to `main.py` for an example application.

### Install Uvicorn

```bash
pip install uvicorn
```

### Run the Application

From the project root directory, execute:

```bash
uvicorn main:app --reload
```

The application will start on the default development server.

## Current Limitations

- Responses must be of type `dict`.
- Only basic routing is supported.
- Only `200 OK` and `404 Not Found` responses are implemented.
- Intended for educational purposes to understand the ASGI protocol rather than production use.