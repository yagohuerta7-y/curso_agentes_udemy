# Resumen - Sección 4

## Runnables y LCEL avanzado

### clase26_runnables.py
`RunnableLambda` - Crea Runnables a partir de funciones simples. Ejemplo: pasar número → duplicar texto

### clase27_proyecto.py
Proyecto: análisis de sentimientos con preprocesamiento, resumen y clasificación en paralelo (manual)

### clase28_runnablesParallel.py
`RunnableParallel` - Ejecuta múltiples Runnables simultáneamente con la misma entrada, agrupa resultados en dict

### clase29_batch.py
`.batch()` - Procesa múltiples textos en paralelo (más rápido que invoke n veces)

---

## Prompt Templates

### clase30_prompt_template.py
`PromptTemplate` - Genera string simple sin roles (solo texto con variables)

### clase31_ChatPromptTemplate.py
`ChatPromptTemplate` - Genera lista de mensajes con roles (system, human, assistant)

### clase32_tarea.py
Tarea: transforma el chatbot para usar `ChatPromptTemplate` + selector de personalidad

### clase33_MessagePlaceholders.py
`MessagesPlaceholder` - Inserta historial de mensajes completo manteniendo roles

### clase34_roles.py
`SystemMessagePromptTemplate` / `HumanMessagePromptTemplate` - Plantillas modulares por rol

---

## Output Parsers

### clase37_output_parsers.py
Intro a **Pydantic** - Define modelos de datos con validación automática (ej: convertir "123" → int)

### clase38_output_parsers.py
`llm.with_structured_output(ClasePydantic)` - Fuerza al LLM a devolver JSON estructurado (validación automática)

---

## Conclusión

**Básicamente sección 4:**

1. **Runnables** - Componentes LangChain que se pueden encadenar con `|`
2. **RunnableParallel** - Ejecución concurrente
3. **.batch()** - Procesamiento de múltiples entradas en paralelo
4. **ChatPromptTemplate** vs PromptTemplate - Con roles vs sin roles
5. **MessagesPlaceholder** - Para inyectar historial de chat
6. **Pydantic** - Para obtener respuestas estructuradas del LLM