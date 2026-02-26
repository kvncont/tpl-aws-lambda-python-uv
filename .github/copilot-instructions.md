# Copilot Instructions for tpl-lambda-python

## Best Practices for Copilot Agents
- Always follow the project conventions and workflows described below.
- Do not override or duplicate the logic of skills defined in `.github/skills/`.
- When generating test events, prefer using the skills (e.g., lambda-event-generator) for guidance and manual editing if needed.
- For debugging GitHub Actions, use the github-actions-debugging skill as reference.
- If a skill exists for a specific task, use its instructions and examples.
- Document any customizations or manual edits for future reference.


## Arquitectura y Componentes Principales
- **Función principal:** Toda la lógica está en `src/lambda_function.py`.
- **Infraestructura:** Definida en `template.yml` usando AWS SAM (Serverless Application Model). Aquí se configuran Lambda, API Gateway, variables de entorno y eventos.
- **Configuración por ambiente:** Archivos en `config/` (ej: `dev.yml`, `prod.yml`) para separar settings según entorno.
- **Eventos de prueba:** Carpeta `events/` con ejemplos de payloads para pruebas locales. Genera eventos siguiendo las skills y edita manualmente si el recurso no está soportado.
- **Pruebas unitarias:** En `tests/`, usando Pytest.

## Flujos de Trabajo Críticos
- **Desarrollo local y pruebas:**
  - Usa el devcontainer (VS Code) para entorno preconfigurado.
  - Levanta la API localmente con `sam local start-api`.
  - Invoca la Lambda localmente con `sam local invoke LambdaFunction --event events/apigateway-aws-proxy.json`.
  - Para generación de eventos, sigue las skills y edita el JSON si el recurso no está soportado.
- **Instalación de dependencias:**
  - Ejecuta `pip install -r requirements-dev.txt` si agregas nuevas librerías.
- **Construcción y despliegue:**
  - `sam build` para compilar.
  - `sam validate` para validar la plantilla.
  - `sam deploy --guided` para desplegar **solo en ambientes locales o cuentas sandbox**. El aprovisionamiento de infraestructura real (dev, prod) se realiza exclusivamente mediante **Terraform** fuera de este repositorio.
- **Logs y limpieza:**
  - `sam logs -n LambdaFunction` para logs.
  - `sam delete` para eliminar recursos de AWS.

## Convenciones y Patrones del Proyecto
- **Commits:** Usar siempre el estándar **conventional-commits** para los mensajes de commit.
- **Pull Requests:** Las descripciones de los PRs deben estar redactadas en **español**.
- **Handler Lambda:** Siempre en `src/lambda_function.py`, función `lambda_handler`.
- **Configuración:** No hardcodear settings; usar archivos en `config/` y variables de entorno.
- **Eventos:** Generar ejemplos con `sam local generate-event ...` y guardarlos en `events/`. Si el recurso no está soportado, edita el JSON siguiendo las recomendaciones de la skill correspondiente.
- **Pruebas:** Usar Pytest, archivos de test en `tests/`.
- **Infraestructura:** No modificar recursos críticos en `template.yml` sin validación previa.

## Integraciones y Dependencias
- **AWS SAM CLI:** Esencial para desarrollo, pruebas y despliegue.
- **Terraform:** El despliegue a ambientes productivos se realiza fuera de este repo, vía Terraform.
- **Devcontainer:** Facilita la configuración homogénea del entorno de desarrollo.

## Archivos Clave
- `src/lambda_function.py`: Lógica principal.
- `template.yml`: Infraestructura y eventos.
- `config/`: Configuración por ambiente.
- `events/`: Ejemplos de eventos.
- `tests/`: Pruebas unitarias.

---

---

> Si algún flujo, convención o integración no está claro, consulta el README.md, revisa las skills en `.github/skills/` o pregunta para mejorar estas instrucciones.
