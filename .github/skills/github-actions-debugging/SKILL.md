---
name: github-actions-debugging
description: Skill para debuggear workflows de GitHub Actions fallidos, especialmente CI/CD. Proporciona pasos, recomendaciones y ejemplos para identificar y solucionar errores en pipelines automatizados.
---

# Debug de GitHub Actions (CI/CD)

## Contexto
Utiliza este skill para analizar y resolver errores en workflows de GitHub Actions, especialmente en procesos de CI/CD. Sigue los pasos recomendados y usa las herramientas de logs para identificar la causa raíz.

## Uso
- Usa el MCP de GitHub para obtener información de workflows fallidos:
	1. Utiliza `list_workflow_runs` para consultar los últimos runs y su estado.
	2. Utiliza `summarize_job_log_failures` para obtener un resumen AI de los logs de jobs fallidos.
	3. Si necesitas más detalle, usa `get_job_logs` o `get_workflow_run_logs` para obtener los logs completos.
- Revisa los últimos runs del workflow en la pestaña Actions del repositorio.
- Identifica el job o paso que falla y copia el mensaje de error principal.
- Usa la opción "View raw logs" para obtener el log completo del job fallido.
- Busca problemas comunes: variables de entorno faltantes, versiones incompatibles, permisos insuficientes o timeouts.
- Si el error no es claro, comparte el mensaje o log relevante para análisis.

## Ejemplo de prompt
```
Ayúdame a debuggear el workflow CI/CD, el job build falla con error de permisos.
```

## Ejemplo de respuesta
- Revisa el log del job build y verifica si falta algún secreto o permiso.
- Si el error es "Permission denied", revisa los permisos del token o de la acción.
- Si es un error de versión, valida que las versiones de las acciones y dependencias sean compatibles.

## Mejores Prácticas
- Documenta los errores y soluciones encontradas para referencia futura.
- Usa nombres descriptivos para los workflows y jobs.
- Mantén actualizadas las versiones de las acciones y dependencias.
- Configura correctamente los secretos y variables de entorno.
- Si el error persiste, intenta reproducirlo localmente antes de modificar el workflow.

## Problemas Comunes
- Variables de entorno o secretos faltantes.
- Versiones incompatibles de acciones o dependencias.
- Permisos insuficientes en el workflow o job.
- Timeouts por jobs demasiado largos.
