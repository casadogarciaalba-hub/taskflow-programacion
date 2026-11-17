# Práctica 1.4 — Middleware, CORS y manejo de errores

**Tag:** `practica-1.4`

## Qué se hizo

1. **CORS**: solo se permite el frontend de `http://localhost:5173`.
2. **Middleware propio `X-Process-Time`**: mide cuánto tarda cada petición y lo añade como cabecera de la respuesta.
3. **Handler global de errores**: si hay un error no controlado, el cliente recibe un 500 con `{"error": "Error interno del servidor"}` y nunca ve el *stacktrace*.
4. Endpoint `GET /error-prueba` para comprobar el handler.

**Corrección del profesor:** al principio estaba todo en `main.py`. Lo saqué a `app/core/middlewares.py`, dentro de la función `registrar_middlewares(app)`, y `main.py` solo la llama.

## Conceptos

- **Middleware**: código que se ejecuta en **todas** las peticiones, antes y después del endpoint (`call_next`).
- **CORS**: el navegador bloquea peticiones a otro origen (otro puerto) salvo que el servidor lo permita.
- **No enseñar el stacktrace**: revelaría información interna del código.

## Archivos

`app/core/__init__.py`, `app/core/middlewares.py` (nuevos), `app/main.py`
