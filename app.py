import streamlit as st
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
def main():
    st.image("a3.jpg", width=720)
    st.sidebar.title("Instrucciones")
    st.sidebar.write("¡Bienvenido a la aplicación A3 para resolver problemas!")
    st.sidebar.markdown("Por favor sigue las instrucciones paso a paso para utilizar la herramienta correctamente.")

    st.sidebar.markdown("### Pasos:")
    st.sidebar.markdown("- **Paso 1:** Identificar el problema u oportunidad de mejora.")
    st.sidebar.markdown("- **Paso 2:** Definir el problema de manera clara y concisa.")
    st.sidebar.markdown("- **Paso 3:** Analizar la situación actual, recopilando datos y evidencia relevante.")
    st.sidebar.markdown("- **Paso 4:** Establecer un objetivo o un objetivo deseado.")
    st.sidebar.markdown("- **Paso 5:** Desarrollar un plan de acción para abordar el problema.")
    st.sidebar.markdown("- **Paso 6:** Implementar el plan y llevar a cabo las acciones definidas.")
    st.sidebar.markdown("- **Paso 7:** Evaluar los resultados obtenidos y aprender de la experiencia.")

    st.sidebar.markdown("### Información Adicional:")
    st.sidebar.markdown("👉 **Para más información: [LinkedIn](https://www.linkedin.com/in/josemaguilar/)**")

    st.markdown("## Aplicación A3 para resolver problemas")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("##### Paso 1: Identificar el problema u oportunidad de mejora")
        problema = st.text_area("Descripción del problema u oportunidad de mejora:")
        if problema:
            st.write("Descripción del problema almacenada en el DataFrame:")
            st.write(pd.DataFrame({"Descripción del Problema": [problema]}))

        st.markdown("##### Paso 2: Definir el problema de manera clara y concisa")
        #st.markdown("#### Gráfico de control del indicador clave respecto a su meta")

        # Mover estas entradas a la barra lateral
        with st.sidebar:
            st.sidebar.title(f"Configuración del Indicador Clave:")
            indicador_clave = st.text_input("Indicador Clave")
            valores_control = st.text_area("Valores del gráfico de control (separados por coma)")
            meta = st.number_input("Meta del indicador clave")
            st.sidebar.title(f"Configuración de causas de desviación:")
            num_categorias = st.number_input("Número de categorías de causas:", min_value=1, value=5)
            causas = []
            for i in range(num_categorias):
                categoria = st.text_input(f"Categoría {i+1}")
                frecuencia = st.number_input(f"Frecuencia {i+1}", min_value=0)
                causas.append({"Categoría": categoria, "Frecuencia": frecuencia})
            st.sidebar.title(f"Configuración de tareas:")
            num_tareas = st.number_input("Número de tareas:", min_value=1, value=1)
            tareas = []
            for i in range(num_tareas):
                tarea = st.text_input(f"Tarea {i+1}")
                responsable = st.text_input(f"Responsable {i+1}")
                fecha_inicio = st.date_input(f"Fecha de inicio {i+1}")
                duracion = st.number_input(f"Duración (en días) {i+1}:", min_value=1, value=1)
                tareas.append({"Tarea": tarea, "Responsable": responsable, "Inicio": fecha_inicio, "Duración": duracion})
            st.sidebar.title(f"Configuración de resultados finales de mejora:")
            num_resultados = st.number_input("Número de indicadores clave de resultado:", min_value=1, value=1)
            resultados = []
            for i in range(num_resultados):
                indicador = st.text_input(f"Indicador {i+1}")
                antes = st.number_input(f"Antes {i+1}:", step=0.01)
                meta_resultado = st.number_input(f"Meta {i+1}:", step=0.01)
                resultado = st.number_input(f"Resultado {i+1}:", step=0.01)
                cumplimiento = st.selectbox(f"¿Cumplió con la meta? {i+1}", ["Sí", "No"])
                resultados.append({"Indicador Clave": indicador, "Antes": antes, "Meta": meta_resultado, "Resultado": resultado, "Cumplimiento": cumplimiento})

        st.write(f"Indicador Clave: {indicador_clave}")

        if valores_control:
            valores_control = [float(val.strip()) for val in valores_control.split(",")]
            fig_control = go.Figure()
            fig_control.add_trace(go.Scatter(x=np.arange(1, len(valores_control) + 1), y=valores_control, mode='lines+markers', name='Indicador Clave'))
            fig_control.add_hline(y=meta, line_dash="dash", line_color="red", annotation_text="Meta", annotation_position="top right")
            fig_control.update_layout(title="Gráfico de control del indicador clave",
                                      xaxis_title="Días",
                                      yaxis_title="Valor del Indicador")
            fig_control.update_layout(height=350, width=320)
            st.plotly_chart(fig_control)

        st.markdown("##### Paso 3: Analizar la situación actual, recopilando datos y evidencia relevante")
        #st.markdown("#### Gráfico de causas con su frecuencia")

        # Crear DataFrame a partir de los datos ingresados en la barra lateral
        df_causas = pd.DataFrame(causas)

        # Ordenar el DataFrame por la columna 'Frecuencia' de mayor a menor
        df_causas_sorted = df_causas.sort_values(by='Frecuencia', ascending=False)

        # Crear el gráfico de barras con Plotly Express
        fig = px.bar(df_causas_sorted, x='Categoría', y='Frecuencia', title="Gráfico de causas con su frecuencia",
                    labels={'Frecuencia': 'Frecuencia', 'Categoría': 'Categoría'})
        fig.update_layout(height=450, width=320)
        # Mostrar el gráfico de barras
        st.plotly_chart(fig)
        comentarios_situacion = st.text_area("Comentarios sobre la situación actual:")

    with col2:
        st.markdown("##### Paso 4: Establecer un objetivo o un objetivo deseado")
        #st.markdown("#### Gráfico de gauge")

        if valores_control:
            media = np.mean(valores_control)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=media,
                domain={'x': [0, 1], 'y': [0, 1]},
                title=f"{indicador_clave}",
                gauge={'axis': {'range': [None, 150]},
                       'bar': {'color': "red" if media < meta else "green"},
                       'steps': [
                           {'range': [0, meta], 'color': "lightblue"}],
                       'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': meta}}))
            fig_gauge.update_layout( height=250, width=350)
            st.plotly_chart(fig_gauge)
            st.write(f"Meta del indicador clave: {meta}")  # Se muestra la meta sin ser modificable
            st.write(f"Media de los datos de control: {round(media, 2)}")

        comentarios_objetivo = st.text_area("Comentarios sobre el objetivo deseado:")
   
        # Paso 5: Desarrollar un plan de acción para abordar el problema
        st.markdown("##### Paso 5: Desarrollar un plan de acción para abordar el problema")
        #st.markdown("#### Plan de acción:")
        # Crear DataFrame para el plan de acción
        df_plan_accion = pd.DataFrame(columns=["Tarea", "Responsable", "Inicio", "Duración"])

        # Agregar las tareas ingresadas desde la barra lateral al DataFrame
        for tarea in tareas:
            df_plan_accion = pd.concat([df_plan_accion, pd.DataFrame([tarea])], ignore_index=True)

        # Mostrar el DataFrame actualizado
        st.write(df_plan_accion)

        # Paso 6: Implementar el plan y llevar a cabo las acciones definidas
        st.markdown("##### Paso 6: Implementar el plan y llevar a cabo las acciones definidas")
        #st.markdown("#### Gráfico de Gantt a partir del plan de acción")
        # Crear lista de diccionarios para cada tarea
        fig_data = []
        for index, row in df_plan_accion.iterrows():
            fig_data.append(dict(Task=row['Tarea'], Start=row['Inicio'], Finish=row['Inicio'] + pd.to_timedelta(row['Duración'], unit='D'), Resource=row['Responsable']))

        # Crear gráfico de Gantt
        fig_gantt = ff.create_gantt(fig_data, group_tasks=True, show_colorbar=True, index_col='Resource', showgrid_x=True, showgrid_y=True)

        # Configurar diseño del gráfico
        fig_gantt.update_layout(xaxis_title='Fecha', yaxis_title='Tarea', height=500, legend=dict(orientation="h", yanchor="bottom", y=-0.9, xanchor="right", x=1))
        fig_gantt.update_layout(height=300, width=350)
        # Mostrar el gráfico de Gantt
        st.plotly_chart(fig_gantt, use_container_width=True)

        # Paso 7: Evaluar los resultados obtenidos y aprender de la experiencia
        st.markdown("##### Paso 7: Evaluar los resultados obtenidos y aprender de la experiencia")
        #st.markdown("#### Resultados obtenidos:")
        # Mostrar los indicadores clave de resultado ingresados desde la barra lateral
        df_resultados = pd.DataFrame(resultados)
        st.write(df_resultados)

if __name__ == "__main__":
    main()