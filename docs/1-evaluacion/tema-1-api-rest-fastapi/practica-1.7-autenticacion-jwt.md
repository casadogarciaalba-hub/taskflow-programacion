# Práctica 1.7 — Autenticación JWT

**Tag:** `practica-1.7`

## Qué pide la práctica

- Modelo `User` (username, hashed_password) y su router `auth.py`.
- `POST /auth/register`: hashea la contraseña con `passlib[bcrypt]`.
- `POST /auth/login`: verifica las credenciales y devuelve un JWT con `python-jose`.
- `get_current_user` usando `OAuth2PasswordBearer`.
- Proteger todos los endpoints de escritura (`POST`/`PUT`/`DELETE`) de tasks y projects.
- Expiración del token: 30 minutos.

**Criterios de aceptación:** las contraseñas nunca se guardan en texto plano, un endpoint protegido devuelve 401 sin token válido y el token caduca.

## Librerías instaladas

    python -m pip install "passlib[bcrypt]" "bcrypt==4.0.1" python-jose python-multipart

- **passlib[bcrypt]**: hashear y comprobar contraseñas.
- **bcrypt==4.0.1**: esta versión porque passlib no se actualiza desde 2020 y da error con las nuevas.
- **python-jose**: crear y comprobar los JWT.
- **python-multipart**: FastAPI la necesita para leer el formulario del login.

## Archivos

| Archivo | Qué hay |
|---|---|
| `app/core/security.py` | **Nuevo.** Hashear contraseñas, crear el token y `get_current_user` |
| `app/routers/auth.py` | **Nuevo.** `POST /auth/register` y `POST /auth/login` |
| `app/models.py` | `User.password` pasa a ser `hashed_password` |
| `app/schemas.py` | `UserCreate`, `UserRead` y `Token` |
| `app/routers/tasks.py` y `projects.py` | Los `POST`, `PUT` y `DELETE` piden token |
| `app/main.py` | Incluye el router `auth` |

Como `User` cambió, borré `taskflow.db` para que se volviera a crear con la columna nueva (`create_all` no modifica tablas que ya existen).

## Cómo funciona

**Registro.** La contraseña se pasa por `pwd_context.hash()` y en la base de datos se guarda un hash tipo `$2b$12$...`, nunca la contraseña. bcrypt mete un *salt* aleatorio en cada hash, así que dos usuarios con la misma contraseña tienen hashes distintos. Además bcrypt es lento a propósito (el registro tarda casi 1 segundo), lo que frena a quien intente adivinar contraseñas probando millones. La respuesta usa `UserRead`, que no tiene contraseña.

**Login.** Busca el usuario y comprueba la contraseña con `pwd_context.verify()`. Si el usuario no existe o la contraseña está mal devuelve el **mismo** error 401 (`Usuario o contraseña incorrectos`), así no se puede saber qué usuarios existen. Si todo va bien devuelve el token.

**El token JWT** lleva:
- `sub`: el usuario.
- `exp`: cuándo caduca (30 minutos después del login).

Va firmado con `SECRET_KEY` y HS256. Si alguien lo modifica, la firma deja de coincidir.

**`get_current_user`.** `OAuth2PasswordBearer` lee la cabecera `Authorization: Bearer <token>` (si no viene, 401). `jwt.decode` comprueba la firma y la caducidad; si el token está mal o caducado, 401 `Token no válido o caducado`.

**Proteger un endpoint** = añadirle el parámetro:

    usuario: models.User = Depends(get_current_user)

| Recurso | Sin token | Con token |
|---|---|---|
| tasks | `GET` | `POST`, `PUT`, `DELETE` |
| projects | `GET` | `POST`, `PUT`, `DELETE` |

## Pruebas (Swagger)

| Prueba | Resultado |
|---|---|
| `POST /projects` sin token | **401** `Not authenticated` |
| `POST /auth/register` | **201**, sin contraseña en la respuesta |
| Login con el botón **Authorize** | **Authorized** |
| `POST /projects` con token | **201** |
| `POST /projects` con el token caducado | **401** `Token no válido o caducado` |

Para probar la caducidad sin esperar 30 minutos puse un momento `ACCESS_TOKEN_EXPIRE_MINUTES = 1`, hice login, esperé un minuto y la misma petición pasó de 201 a 401. Después lo dejé otra vez en 30.
