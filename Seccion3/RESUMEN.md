# Resumen - Sección 3

## 1. clases_10_12.py

**Temática:** Fundamentos de LangChain (Prompt Templates + LCEL)

- **PromptTemplate**: Crea plantillas de reutilizables con variables dinámicas (`{personaje}`)
- **Chains (LCEL)**: Usa el operador `|` para encadenar componentes - `plantilla | llm` significa que la salida de la plantilla se pasa al LLM
- Ejemplo práctico: generar los 5 datos más relevantes de un personaje histórico

---

## 2. proyecto_unidad.py

**Temática:** Chatbot completo con Streamlit (proyecto final de sección)

- **Sidebar de configuración**: Slider para ajustar la temperatura del modelo (0.0 - 1.0)
- **Streaming de respuestas**: Muestra la respuesta palabra por palabra en tiempo real usando `chain.stream()`
- **Nueva conversación**: Botón que limpia el historial de mensajes
- **Historial persistente**: Usa `st.session_state` para mantener la conversación
- **Mensajes estructurados**: Usa `SystemMessage`, `HumanMessage`, `AIMessage` de LangChain

---

## Conclusión

**Básicamente:** La sección 3 te enseña a conectar LangChain con una UI (Streamlit), usando PromptTemplates, Chains, y streaming para hacer un chatbot similar a ChatGPT.