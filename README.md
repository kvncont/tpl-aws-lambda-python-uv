# Lambda Python

Esta función Lambda se encarga de [describir aquí la funcionalidad principal].

## Pre-requisitos

- Tener instalado Docker o acceso de crear un Codespace en GitHub.
- (Opcional pero recomendable) Acceso a una cuenta de AWS para pruebas y despliegue.


## Características principales

- Entorno de desarrollo preconfigurado con devcontainer (VS Code):
  - Python 3.13
  - AWS CLI, SAM CLI, Docker, GitHub CLI
  - Extensiones recomendadas para Python, linting, formateo y Postman
- Workflows de GitHub Actions para:
  - Validación de código (CI/CD)
  - Análisis de calidad
  - Despliegue automático a entornos DEV y QA
- Estructura organizada:
  - `template.yml`: Define recursos AWS (Lambda, API Gateway, etc.)
  - `src/lambda_function.py`: Lógica de la función Lambda
  - `config/`: Configuración por ambiente
  - `tests/`: Pruebas unitarias

## Uso del entorno

Al abrir el repositorio en VS Code, el devcontainer instala todo lo necesario para empezar a desarrollar y probar funciones Lambda localmente.

## Instalación de dependencias

Solo es necesario instalar dependencias manualmente si agregas nuevas librerías después de crear el devcontainer o codespace.

```bash
uv sync --group dev
```

## Linting y formato

Usa `ruff` para linting y formato:

```bash
uv add --dev ruff  # si no está instalado
ruff check . --fix
```

## Entorno virtual

Se recomienda usar `uv venv` para crear el entorno virtual:

```bash
uv venv
source .venv/bin/activate
```
## Inicio de sesión en AWS con SSO

Antes de ejecutar comandos que accedan a recursos remotos de AWS, inicia sesión con el perfil correspondiente:

```bash
aws sso login --profile default --use-device-code
```

El comando mostrará una URL y un código. Abre la URL en el navegador, ingresa el código y completa la autenticación. Si utilizas un perfil distinto de `default`, reemplázalo en el comando.

También puedes iniciar sesión con el task incluido en VS Code:

1. Abre la paleta de comandos con `Ctrl+Shift+P` o `F1` en Windows/Linux, o `Cmd+Shift+P` o `F1` en macOS.
2. Selecciona `Tasks: Run Task`.
3. Ejecuta `AWS SSO Login`.
4. Indica el perfil de AWS que deseas utilizar; el valor predeterminado es `default`.
5. Completa la autenticación en el navegador con la URL y el código mostrados.

Este paso es importante porque AWS CLI y SAM necesitan credenciales temporales válidas para consultar logs, validar recursos remotos, desplegar o eliminar infraestructura. AWS SSO evita guardar credenciales permanentes en el equipo y aplica los permisos asociados al perfil seleccionado. Si la sesión expira, ejecuta nuevamente el comando o el task.

También debes tener disponible el archivo `~/.aws/config` con la configuración del perfil SSO. En un devcontainer local, este repositorio monta automáticamente el directorio `~/.aws` de la máquina host dentro del contenedor, por lo que el perfil debe estar configurado previamente en el host; consulta la guía de [montaje de archivos locales en un devcontainer](https://code.visualstudio.com/remote/advancedcontainers/add-local-file-mount). En GitHub Codespaces, puedes usar un repositorio de [dotfiles para personalizar Codespaces](https://docs.github.com/en/codespaces/setting-your-user-preferences/personalizing-github-codespaces-for-your-account) y crear `~/.aws/config` durante su instalación. Puedes consultar el formato requerido en la documentación de [configuración de AWS CLI con IAM Identity Center](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html). No incluyas credenciales, tokens ni el contenido de `~/.aws/sso/cache` en los dotfiles; únicamente la configuración no sensible del perfil.

## Comandos útiles con AWS SAM CLI

### Comandos locales para desarrollo y pruebas

- **Levantar la API en local:**

    ```bash
    sam local start-api
    ```
    Inicia un servidor local en http://localhost:3000 para probar los endpoints definidos en template.yml.

    **O puedes usar el task de VS Code para levantar el API Gateway localmente:**
    1. Abre la paleta de comandos:
      - En Windows/Linux: `Ctrl+Shift+P` o `F1`.
      - En macOS: `Cmd+Shift+P` o `F1`.
    2. Busca y selecciona `Tasks: Run Task`.
    3. Elige la tarea `Iniciar API Gateway`.
    4. El servidor local iniciará y podrás probar los endpoints en http://localhost:3000.

- **Invocar la función Lambda en local:**
  ```bash
  sam local invoke LambdaFunction --event events/apigateway-aws-proxy.json
  ```
  Ejecuta la función Lambda usando un evento de ejemplo.

  **O puedes usar el task de VS Code para invocar la Lambda fácilmente:**
    1. Abre la paleta de comandos:
      - En Windows/Linux: `Ctrl+Shift+P` o `F1`.
      - En macOS: `Cmd+Shift+P` o `F1`.
  2. Busca y selecciona `Tasks: Run Task`.
  3. Elige la tarea `Invocar Lambda`.
  4. Selecciona el archivo de evento que quieres usar (por ejemplo, `cloudwatch-scheduled-event.json` o ingresa la ruta de tu archivo).
  5. Revisa la salida en el panel de terminal.

  Esto te permite invocar la función Lambda localmente sin escribir el comando manualmente, facilitando pruebas rápidas con diferentes eventos.

- **Generar eventos de ejemplo:**
  ```bash
  # Ver todos los eventos disponibles
  sam local generate-event [OPTIONS] COMMAND [ARGS]...
  # Ejemplos:
  sam local generate-event s3 put > events/s3-put.json
  sam local generate-event apigateway aws-proxy > events/apigateway-aws-proxy.json
  sam local generate-event cloudwatch scheduled-event > events/cloudwatch.json
  ```
  Permite crear archivos de eventos para simular invocaciones desde distintos servicios AWS.

### Comandos para construcción, validación y despliegue

- **Compilar el proyecto:**
  ```bash
  sam build
  ```
  Prepara el código y dependencias para su despliegue.

- **Validar la plantilla SAM:**
  ```bash
  sam validate
  ```
  Verifica que el archivo template.yml esté correctamente definido.

- **Desplegar en AWS:**
  ```bash
  sam deploy --guided
  ```
  Despliega la función Lambda y recursos definidos en AWS. _Requiere permisos de despliegue en una cuenta de AWS._
  > Nota: Este comando debería usarse solo para pruebas en cuentas sandbox, ya que la creación de la infraestructura en los diferentes ambientes se realiza mediante Terraform.

- **Ver logs de Lambda:**
  ```bash
  sam logs -n LambdaFunction
  ```
  Muestra los logs de ejecución de la función Lambda en AWS. _Requiere permisos de acceso a CloudWatch Logs._

- **Eliminar recursos desplegados:**
  ```bash
  sam delete
  ```
  Elimina los recursos creados por el despliegue. _Requiere permisos de eliminación en la cuenta de AWS._

## Sobre el archivo template.yml

El archivo `template.yml` define la infraestructura y configuración necesaria para desplegar la función Lambda y sus recursos asociados usando AWS SAM (Serverless Application Model).

### ¿Qué contiene este archivo?
- **AWSTemplateFormatVersion y Transform:** Indican el formato y que se usa SAM para simplificar la definición de recursos serverless.
- **Description:** Breve descripción del stack.
- **Globals:** Configuración global para todas las funciones Lambda (runtime, memoria, timeout, variables de entorno).
- **Parameters:** Permite parametrizar el entorno (dev, qa, prod) y otros recursos opcionales.
- **Resources:**
  - **ApiGateway:** Define una API Gateway REST para exponer la Lambda vía HTTP, con configuración de CORS y stage.
  - **LambdaFunction:** Define la función Lambda principal, su código, handler, variables de entorno y los eventos que la disparan (GET/POST a /lambda).
- **Outputs:** Expone información útil tras el despliegue, como la URL de la API, el ARN de la Lambda, etc.

Puedes modificar este archivo para agregar más funciones, recursos, permisos o eventos según las necesidades de tu proyecto.


## Recursos adicionales

Más información sobre cómo estructurar y personalizar este archivo en la documentación oficial de AWS SAM:
- https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html
- https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-template-basics.html

