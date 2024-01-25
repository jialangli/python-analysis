#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


import codecs
original_data = pd.read_csv(codecs.open(r"C:/Users/ljl20/Downloads/直播串讲课件+数据集20240122/0122直播串讲课件+数据集/电商用户历史数据集.csv", "r", encoding='utf-8', errors='ignore'))


# ##
# 数据每列的含义如下：
# - `InvoiceNo`: 发票号码。6位数，作为交易的唯一标识符。
# - `StockCode`: 产品代码。5位数，作为产品的唯一标识符。
# - `Description`: 产品名称。
# - `Quantity`: 产品在交易中的数量。
# - `InvoiceDate`: 发票日期和时间。交易发生的日期和时间。
# - `UnitPrice`: 单价。价格单位为英镑（£）。
# - `CustomerID`: 客户编号。5位数，作为客户的唯一标识符。
# - `Country`: 国家名称。客户所居住的国家的名称。

# In[3]:


original_data.head(20)


# #### 整洁数据的特点：1.每列是一个变量  2.每行是一个变量  3.每个单元格是一个值

# # 第一步：评估数据

# In[4]:


original_data.sample(20)


# ### 从抽样的10行数据数据来看，数据是符合整洁数据的特点的，因此不存在结构性问题。

# ## 评估数据干净度

# In[5]:


#使用info获取数据的基本信息摘要
original_data.info()  


# ### 从输出结果来看，数据共有541909条观察值，而`Description`、`CustomerID`变量存在缺失值。
# ### 此外，`InvoiceDate`的数据类型应为日期，`CustomerID`的数据类型应为字符串，应当进行数据格式转换。

# ###  DataFrame 中数值列的统计摘要

# In[6]:


original_data. describe()


# ###  通过观察Quantity和UnitPrice的min部分均为负数

# In[7]:


original_data[original_data["Quantity"] < 0]


# ### 通过观察又可以发现InvoiceNo的开头都是C，那我们继续展开猜想，是不是Quantity为负的开头都为C

# In[8]:


original_data[(original_data["Quantity"] < 0) & (original_data["InvoiceNo"].str[0] != "C")]


# ### 猜想错误，那我们就继续添加条件

# ### 看是否存在`Description`变量缺失且`UnitPrice`不为0的数据。

# In[9]:


original_data[(original_data["Quantity"] < 0)&(original_data["InvoiceNo"].str[0] != "C")&(original_data["UnitPrice"] != 0)]


# ### 筛选出来结果数量为0条，说明缺失`Description`值的数据，同时也不具备有效的`UnitPrice`值。

# In[10]:


original_data[original_data["UnitPrice"] < 0]


# In[11]:


original_data["Country"].value_counts()


# #### 国家无重复数据

# #### 根据前面评估部分得到的结论,我们需要进行的数据清理包括:
# #### - 把`InvoiceDate`变量的数据类型转换为为日期时间
# #### - 把`CustomerID`变量的数据类型转换为字符串
# #### - 把`Description`变量缺失的观察值删除
# #### - 把`Quantity`变量值为负数的观察值删除
# #### - 把`UnitPrice`变量值为负数的观察值删除

# In[12]:


cleaned_data=original_data.copy()
cleaned_data


# In[13]:


# 使用pd.to_datetime() 函数,将不同格式的日期时间数据转换为统一的日期时间类型。
cleaned_data["InvoiceDate"] = pd.to_datetime(cleaned_data["InvoiceDate"])
cleaned_data["InvoiceDate"]


# In[14]:


# 将`CustomerID`变量的数据类型转换为字符串：
cleaned_data["CustomerID"] = cleaned_data["CustomerID"].astype(str)
cleaned_data["CustomerID"]


# In[15]:


# 通过使用str.slice() 方法对字符串进行切片将.0去掉
cleaned_data["CustomerID"] = cleaned_data["CustomerID"].str.slice(0, -2)
cleaned_data["CustomerID"]


# ###  把Description变量缺失的观察值删除，使用dropna()删除包含缺失值（NaN）的行或列。

# In[16]:


cleaned_data=cleaned_data.dropna(subset=["Description"])
cleaned_data


# #### 检查删除干净了没有

# In[17]:


cleaned_data["Description"].isnull().sum()


# ### 把Quantity变量值为负数的观察值删除，并检查删除干净了没有

# In[18]:


cleaned_data = cleaned_data[cleaned_data["Quantity"] >= 0]
cleaned_data


# In[19]:


len(cleaned_data[cleaned_data["Quantity"] < 0])


# In[20]:


cleaned_data = cleaned_data[cleaned_data["UnitPrice"] >= 0]
cleaned_data


# In[21]:


len(cleaned_data[cleaned_data["UnitPrice"] < 0])


# In[22]:


cleaned_data.info()


# In[23]:


cleaned_data.describe()


# # 数据分析

# ### 看看哪个东西销量最高

# In[24]:


buy_most=cleaned_data['Quantity']
buy_most


# In[25]:


sorted_indexes = np.argsort(buy_most)
top_twenty_buy_most = sorted_indexes[-20:]


# In[26]:


top_twenty_buy_most = sorted_indexes[-20:]
top_twenty_buy_most_values = zip(cleaned_data['Description'], buy_most.iloc[top_twenty_buy_most])

# 输出 top_twenty_buy_most_values 列表内容
for i in top_twenty_buy_most_values:
    print(i)


# #### 带金属心的食谱盒销量最高？？？？？？？

# ### 看看人们一般什么时候购物

# In[27]:


time=cleaned_data['InvoiceDate']
time


# In[28]:


import pandas as pd

# 将时间数据转换为 Pandas 的 Datetime 类型
time = pd.to_datetime(cleaned_data['InvoiceDate'])

# 将时间转换为分钟数
minutes = time.dt.hour * 60 + time.dt.minute

# 定义不同时区的时间范围（以分钟表示）
time_ranges = [0, 8*60, 12*60, 17*60, 20*60, 24*60]

# 划分时区
time_zones = pd.cut(minutes, bins=time_ranges, labels=['0-8', '8-12', '12-17', '17-20', '20-24'], right=False)

# 打印结果
print(time_zones)


# # 数据可视化分析

# ## 1.地域分析

# In[29]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[30]:


# 设置图表色盘为"pastel"
sns.set_palette("pastel")


# In[31]:


Country_count = cleaned_data["Country"].value_counts()
plt.pie(Country_count, autopct='%.0f%%', labels=Country_count.index)
plt.show()


# In[32]:


from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.faker import Faker


# In[33]:


Country_count= cleaned_data["Country"].value_counts()


# In[34]:


pie = Pie()
pie.set_global_opts(title_opts=opts.TitleOpts(title="电商使用国家分布"),
                    legend_opts=opts.LegendOpts(is_show=False))


# In[35]:


data_list = list(Country_count.items())
pie.add(
"",
data_list,
radius=["30%", "75%"],
label_opts=opts.LabelOpts(formatter="{b}: {d}%"))


# In[36]:


pie.render_notebook()


# ### 由图可知，英国人对于该电商的使用量遥遥领先

# In[37]:


from pyecharts.charts import Funnel  # 导入 Funnel 类


# In[38]:


funnel = Funnel()

funnel.add(
    "",
    data_list,
    sort_="ascending",  # 设置排序方式，可以选择 "ascending"（升序）或 "descending"（降序）
    gap=2,  # 设置各个阶段之间的间隔大小
    label_opts=opts.LabelOpts(formatter="{b}: {d}%")
)
funnel.set_series_opts(legend_opts=opts.LegendOpts(is_show=False))  # 不显示图例
funnel.set_global_opts(
    title_opts=opts.TitleOpts(title="Funnel Chart"),
    tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{b}: {d}%")
)


# In[39]:


funnel.set_global_opts(title_opts=opts.TitleOpts(title="漏斗图"))


# In[40]:


funnel.render_notebook()


# In[41]:


from pyecharts.charts import Bar, Timeline
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# 统计每个时区的数量
time_zone_counts = time_zones.value_counts().sort_index()

# 创建时间线图对象
timeline_chart = Timeline(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))

# 创建柱状图对象
bar_chart = (
    Bar()
    .add_xaxis(time_zone_counts.index.tolist())
    .add_yaxis("时区数量", time_zone_counts.values.tolist(), label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="不同时区的数量"),
        xaxis_opts=opts.AxisOpts(name="时区"),
        yaxis_opts=opts.AxisOpts(name="数量"),
    )
)

timeline_chart.add(bar_chart, "柱状图")
timeline_chart.render_notebook()


# In[42]:


from pyecharts.charts import Line, Timeline
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# 统计每个时区的数量
time_zone_counts = time_zones.value_counts().sort_index()

# 创建时间线图对象
timeline_chart = Timeline(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))

# 创建折线图对象
line_chart = (
    Line()
    .add_xaxis(time_zone_counts.index.tolist())
    .add_yaxis("时区数量", time_zone_counts.values.tolist(), label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="不同时区的数量"),
        xaxis_opts=opts.AxisOpts(name="时区"),
        yaxis_opts=opts.AxisOpts(name="数量"),
    )
)
timeline_chart.add(line_chart, "折线图")
timeline_chart.render_notebook()


# ### 由图可知  顾客一般都是在下午购物的

# In[ ]:





# In[ ]:




