import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(page_title="Dashboard Retail", layout="wide")
st.title("💲 Dashboard Ventas Retail Mexico")

# Cargar datos
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1oS1OgbYcYaKLuBdjpA2T9PCnxjtTe-Um/edit?usp=sharing&ouid=105963250605137917591&rtpof=true&sd=true"
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    #path = 'user_behavior_dataset.csv'
    df = pd.read_excel(path)
    return df

df_retail = load_data()

ven_gan_mes_filter = st.sidebar.multiselect(
    "Ventas y Ganancias por Mes",
    options=sorted(df_retail["mes_pedido"].unique()),
    default=sorted(df_retail["mes_pedido"].unique()),
)

cat_prod_filter = st.sidebar.multiselect(
    "Categoría de Producto",
    options=df_retail["Categoría"].unique(),
    default=df_retail["Categoría"].unique()
)

seg_cliente_filter = st.sidebar.multiselect(
    "Segemento de Cliente",
    options=sorted(df_retail["Segmento"].unique()),
    default=sorted(df_retail["Segmento"].unique())
)

anual_filter = st.sidebar.multiselect(
    "Año de Ventas",
    options=sorted(df_retail["año_pedido"].unique()),
    default=sorted(df_retail["año_pedido"].unique())
)

# Filtrar el dataframe
df_filtered = df_retail[
    (df_retail["mes_pedido"].isin(ven_gan_mes_filter)) &
    (df_retail["Categoría"].isin(cat_prod_filter)) &
    (df_retail["Segmento"].isin(seg_cliente_filter)) &
    (df_retail["año_pedido"].isin(anual_filter))
]

# KPIs (compacto)
col1, col2 = st.columns(2)
with col1:
    st.metric("💰 Ventas", df_filtered['Ventas'].sum())
with col2:
    st.metric("💱 Ganancias", (df_filtered['Ganancia'].sum()))

# Fila 1
colv1, colv2 = st.columns(2)

with colv1:
    fig1, ax = plt.subplots()

    sns.lineplot(data=df_filtered, x='mes_pedido', y='Ventas', marker='o', estimator='sum', label='Ventas', ax=ax)
    sns.lineplot(data=df_filtered, x='mes_pedido', y='Ganancia', marker='o', estimator='sum', label='Ganancia', ax=ax)
    ax.set_title('Ventas y Ganancias por Mes')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Monto')
    ax.grid(True)
    ax.set_xticks(range(1, 13))
    ax.set_yticks(range(0, 3200000, 200000))
    ax.legend()
    st.pyplot(fig1)

with colv2:
    sf_ventas_segmento = df_filtered.groupby('Segmento')['Ventas'].sum().reset_index()
    fig2 = px.bar(sf_ventas_segmento, x='Segmento', y='Ventas', title='Ventas Totales por Segmento de Cliente en México', color='Segmento', width=800)
    fig2.update_layout(xaxis_title='Segmento de Cliente', yaxis_title='Ventas Totales')
    st.plotly_chart(fig2)

# Fila 2
colv3, colv4, colv5 = st.columns(3)

with colv3:
    fig3 = sns.catplot(x='Categoría', y='Ventas', data=df_filtered, kind='bar', hue='Categoría', estimator='sum', height=4, aspect=1.5)
    fig3.set_xticklabels(rotation=45)
    fig3.set_axis_labels('Categoría de Producto', 'Ventas Totales')
    fig3.fig.suptitle('Ventas Totales por Categoría de Producto en México')
    plt.tight_layout()
    st.pyplot(fig3.fig, use_container_width=True)

with colv4:
    ganancia_cat = df_filtered.groupby('Categoría')['Ganancia'].sum().reset_index()

    fig4, ax = plt.subplots()
    ax.pie(ganancia_cat['Ganancia'], labels=ganancia_cat['Categoría'], autopct='%1.1f%%', startangle=90)
    ax.set_title('Proporción de Ganancias por Categoría de Producto en México')
    ax.axis('equal')

    st.pyplot(fig4, use_container_width=True)

with colv5:
    fig5, ax = plt.subplots()

    sns.barplot(x='Segmento', y='Ganancia', data=df_filtered, hue='año_pedido', estimator='sum', palette='viridis', ax=ax)
    ax.set_title('Ganancias Totales por año por Segmento de Cliente')
    ax.set_xlabel('Segmento de Cliente')
    ax.set_ylabel('Ganancias Totales')
    ax.legend(title='Año del Pedido')
    ax.tick_params(axis='x', rotation=45)

    st.pyplot(fig5, use_container_width=True)

# Conclusiones
st.markdown("*Realizado por: John Fredy López Ramírez - Carlos Ramírez Martínez*")
