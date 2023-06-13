import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import io

uploaded_file = st.sidebar.file_uploader('Choose a file')

if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)

  st.sidebar.divider()
  chbx_showDf = st.sidebar.checkbox('Show Data Frame', key = 'chbx_showDf')
  chbx_showDfInfo = st.sidebar.checkbox('Show Relevant Info', key = 'chbx_showDfInfo')
  st.sidebar.divider()

  if chbx_showDf:
    st.subheader('Uploaded Data')
    st.write(df)
    st.divider()

  if chbx_showDfInfo:
    st.subheader('Column Data Types')
    content_infoTable = pd.DataFrame(df.dtypes).reset_index()
    content_infoTable.rename(columns = {'index': 'Column Name', 0: 'Data Type'}, inplace = True)
    st.table(content_infoTable)

    st.subheader('Relevant Information')
    col_info1, col_info2, col_info3 = st.columns(3)
    col_info1.metric('Num of Rows', df.shape[0])
    col_info2.metric('Num of Columns', df.shape[1])
    col_info3.metric('Size', df.size)

    st.divider()

  slct_columnType = st.sidebar.selectbox('Select Data Type', ('Numerical', 'Categorical'), key = "slct_columnType")

  if slct_columnType == 'Numerical':
    slct_numericalColumn = st.sidebar.selectbox(
        'Select a Column', df.select_dtypes(include = ['int64', 'float64']).columns)
    st.sidebar.divider()

    tab_5numSummary, tab_hist, tab_kde = st.tabs(['5 Number Summary', 'Histogram', 'Kernel Density Estimate (KDE)'])

    with tab_5numSummary:
      col_summ1, col_summ2, col_summ3, col_summ4, col_summ5 = st.columns(5)

      col_summ1.metric('Min', df[slct_numericalColumn].describe().loc['min'])
      col_summ2.metric('25%', df[slct_numericalColumn].describe().loc['25%'])
      col_summ3.metric('50%', df[slct_numericalColumn].describe().loc['50%'])
      col_summ4.metric('75%', df[slct_numericalColumn].describe().loc['75%'])
      col_summ5.metric('Max', df[slct_numericalColumn].describe().loc['max'])

    with tab_hist:
      color_histCol = st.color_picker('Pick a Color', '#69b3a2', key = 'color_histCol')
      sld_histBin = st.slider('Number of bins', min_value = 5, max_value = 150, value = 30, key = 'sld_histBin')
      txt_histTitle = st.text_input('Set Title', 'Histogram', key = 'txt_histTitle')
      txt_histAx = st.text_input('Set x-axis Title', slct_numericalColumn, key = 'txt_histAx')

      fig, ax = plt.subplots()
      ax.hist(df[slct_numericalColumn], bins = sld_histBin,
              edgecolor = 'black', color = color_histCol)
      ax.set_title(txt_histTitle)
      ax.set_xlabel(txt_histAx)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = 'plot.png'
      fig.savefig(filename, dpi = 300)

      with open('plot.png', 'rb') as file:
        btn = st.download_button(
            label = 'Download image',
            data = file,
            file_name = 'WebApp_HistFig.png',
            mime = 'image/png'
        )

    with tab_kde:
      color_kdeCol = st.color_picker('Pick a Color', '#69b3a2', key = 'color_kdeCol')
      txt_kdeTitle = st.text_input('Set Title', 'KDE Plot', key = 'txt_kdeTitle')
      txt_kdeAx = st.text_input('Set x-axis Title', slct_numericalColumn, key = 'txt_kdeAx')

      fig, ax = plt.subplots()
      sns.kdeplot(data = df, x = slct_numericalColumn, color = color_kdeCol)
      ax.set_title(txt_kdeTitle)
      ax.set_xlabel(txt_kdeAx)
      ax.set_ylabel('Density')

      st.pyplot(fig)
      filename = 'plot.png'
      fig.savefig(filename, dpi = 300)

      with open('plot.png', 'rb') as file:
        btn = st.download_button(
            label = 'Download image',
            data = file,
            file_name = 'WebApp_KdeFig.png',
            mime = 'image/png'
        ) 
  
  elif slct_columnType == 'Categorical':
    slct_categorialColumn = st.sidebar.selectbox(
        'Select a Column', df.select_dtypes(include = ['bool', 'object']).columns)
    st.sidebar.divider()

    content_categoricalLevels = df
    content_categoricalLevels['count'] = 0
    content_categoricalLevels = content_categoricalLevels.groupby(slct_categorialColumn)['count'].count().reset_index()
    content_categoricalLevels['proportion'] = content_categoricalLevels['count'] / content_categoricalLevels['count'].sum()
    st.table(content_categoricalLevels)

    slct_barColorPalette = st.selectbox('Select Data Type', ('magma', 'viridis', 'rocket', 'mako'), key = "slct_barColorPalette")
    txt_barTitle = st.text_input('Set Title', 'Proportion Bar Plot', key = 'txt_barTitle')
    txt_barXAx = st.text_input('Set x-axis Title', slct_categorialColumn, key = 'txt_barXAx')
    txt_barYAx = st.text_input('Set y-axis Title', 'count', key = 'txt_barYAx')

    fig, ax = plt.subplots()
    sns.barplot(data = content_categoricalLevels, x = slct_categorialColumn, y = 'count', palette = slct_barColorPalette)
    ax.set_title(txt_barTitle)
    ax.set_xlabel(txt_barXAx)
    ax.set_ylabel(txt_barYAx)

    st.pyplot(fig)
    filename = 'plot.png'
    fig.savefig(filename, dpi = 300)

    with open('plot.png', 'rb') as file:
      btn = st.download_button(
          label = 'Download image',
          data = file,
          file_name = 'WebApp_BarFig.png',
          mime = 'image/png'
      )

