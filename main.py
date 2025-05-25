import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

#C:\Users\81802\OneDrive\デスクトップ\Python\streamlit
#streamlit run main.py

st.title('test imai')
st.write('DataFrame')

df=pd.DataFrame({
    '1列目':[1,2,3,4],
    '2列目':[10,20,30,40]
})

st.write(df)
st.dataframe(df.style.highlight_max(axis=0),width=300,height=300)#縦横を変えられる
st.table(df.style.highlight_max(axis=0))#静的な表


"""
# 章

## 節

### 項

```Python
import streamlit as st
import numpy as np
import pandas as pd
```

"""

df2=pd.DataFrame(
    np.random.rand(20,3),
    columns=['a','b','c']
)

st.line_chart(df2)
st.area_chart(df2)
st.bar_chart(df2)

df3=pd.DataFrame(
    np.random.rand(100,2)/[50,50]+[35.69,139.70],
    columns=['lat','lon']
)

st.map(df3)

img=Image.open('まこら.png')

st.image(img,caption='makora',use_column_width=True)






