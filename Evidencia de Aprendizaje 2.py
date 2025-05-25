import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(page_title="Dashboard Retail", layout="wide")
st.title("💲 Dashboard Ventas Retail México")

# Cargar datos
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1oS1OgbYcYaKLuBdjpA2T9PCnxjtTe-Um/edit?usp=sharing&ouid=105963250605137917591&rtpof=true&sd=true"
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    #path = 'user_behavior_dataset.csv'
    df = pd.read_csv(path)
    return df

df_retail = load_data()

# Filtros en fila superior
#colf1, colf2, colf3 = st.columns(3)
#with colf1:
#    os_filter = st.multiselect(
#        "Sistema operativo",
#        options=df["Operating System"].unique(),
#        default=df["Operating System"].unique()
#    )
#
#with colf2:
#    gender_filter = st.multiselect(
#        "Género",
#        options=df["Gender"].unique(),
#        default=df["Gender"].unique()
#    )
#
#with colf3:
#    behavior_filter = st.multiselect(
#        "Clase de comportamiento",
#        options=sorted(df["User Behavior Class"].unique()),
#        default=sorted(df["User Behavior Class"].unique())
#    )

ven_gan_mes_filter = st.sidebar.multiselect(
    "Ventas y Ganancias por Mes",
    options=df_retail["mes_pedido"].unique(),
    options=df_retail["mes_pedido"].unique(),
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
    fig1 = sns.lineplot(data=df_retail, x='mes_pedido', y='Ventas', marker='o', estimator='sum', label='Ventas')
    sns.lineplot(data=df_retail, x='mes_pedido', y='Ganancia', marker='o', estimator='sum', label='Ganancia')
    plt.title('Ventas y Ganancias por Mes')
    plt.xlabel('Mes')
    plt.ylabel('Monto')
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(ticks=range(1, 13))
    plt.yticks(ticks=range(0, 1000000, 50000))
    plt.legend()
    plt.show()
    st.pyplot(fig1, use_container_width=True)

# with colv1:
#     fig1 = px.box(
#         df_filtered,
#         x="User Behavior Class",
#         y="App Usage Time (min/day)",
#         title="Uso por clase de usuario",
#         points="all"
#     )
#     st.plotly_chart(fig1, use_container_width=True)

with colv2:
    sf_ventas_segmento = df_retail.groupby('Segmento')['Ventas'].sum().reset_index()
    fig2 = px.bar(sf_ventas_segmento, x='Segmento', y='Ventas', title='Ventas Totales por Segmento de Cliente en México', color='Segmento', width=800)
    fig2.update_layout(xaxis_title='Segmento de Cliente', yaxis_title='Ventas Totales')
    st.plotly_chart(fig2, use_container_width=True)

# with colv2:
#     avg_data = df_filtered.groupby("Operating System")["Data Usage (MB/day)"].mean().reset_index()
#     fig2 = px.bar(avg_data, x="Operating System", y="Data Usage (MB/day)", title="Uso de datos por OS")
#     st.plotly_chart(fig2, use_container_width=True)


# Fila 2
colv3, colv4, colv5 = st.columns(3)

with colv3:
    fig3 = sns.catplot(x='Categoría', y='Ventas', data=df_retail, kind='bar', hue='Categoría', estimator='sum')
    plt.xticks(rotation=45)
    plt.title('Ventas Totales por Categoría de Producto en México')
    plt.xlabel('Categoría de Producto')
    plt.ylabel('Ventas Totales')
    plt.show()
    st.pyplot(fig3, use_container_width=True)

with colv4:
    ganancia_cat = df_retail.groupby('Categoría')['Ganancia'].sum().reset_index()
    fig4 = plt.pie(ganancia_cat['Ganancia'], labels=ganancia_cat['Categoría'], autopct='%1.1f%%')
    plt.title('Proporción de Ganancias por Categoría de Producto en México')
    plt.show()
    st.pyplot(fig4, use_container_width=True)

with colv5:
    fig6 = sns.barplot(x='Segmento', y='Ganancia', data=df_retail, hue='año_pedido', estimator='sum', palette='viridis')
    plt.legend(title='Año del Pedido')
    plt.xticks(rotation=45)
    plt.title('Ganancias Totales por año por Segmento de Cliente')
    plt.xlabel('Segmento de Cliente')
    plt.ylabel('Ganancias Totales')
    st.pyplot(fig6, use_container_width=True)

# Conclusiones
st.markdown("*Realizado por: John Fredy López Ramírez \n Carlos Ramírez Martínez*")
