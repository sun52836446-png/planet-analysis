import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns


# 设置中文字体（SimHei = 黑体）
plt.rcParams['font.sans-serif'] = ['SimHei']

# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False


df = pd.read_excel("planet.xlsx")

#数据清洗

df = df.drop(columns=['Unnamed: 0'])
df['距地距离'] = df['距地距离'].fillna(df['距地距离'].median())#填充距地距离为中位数
df = df.dropna(subset=['轨道周期']) #删除轨道周期
mass_def = df.dropna(subset=['行星质量']) #忽略行星质量

yearly_count = df.groupby('发现时间')['发现数量'].sum()
method_count = df.groupby('观测方法')['发现数量'].sum()
method_stats = mass_def.groupby('观测方法')[['行星质量','轨道周期','距地距离']].mean()

num_cols=['行星质量','轨道周期','距地距离']
corr_matrix = mass_def[num_cols].corr() #计算相关性矩阵

year_method_count = df.groupby(['发现时间','观测方法'])['发现数量'].sum().unstack()
#分组，每组数量求和，最后将行索引变成列索引

print(df.head()) #显示前五行
#print(df.info()) #查看数据信息
#print(df.describe()) #查看数值列统计信息

#折线图
plt.figure(figsize=(12,6)) #设置图像大小
plt.plot(yearly_count.index, yearly_count.values, marker='o')
plt.title('行星发现数量年度趋势',fontsize=16)
plt.xlabel('年份',fontsize=12)
plt.ylabel('发现数量',fontsize=12)
plt.grid(True) #打开网格线
#plt.savefig('年度折线图.png')
#plt.show()


#柱状图
plt.figure(figsize=(12,6)) #设置图像大小

method_count.plot(kind='bar',color='skyblue')

plt.title('不同观测方法下发现行星数量',fontsize=16)
plt.xlabel('观测方法',fontsize=12)
plt.ylabel('发现数量',fontsize=12)
plt.xticks(rotation=0) #控制 x 轴标签旋转
plt.grid(axis='y') #只画y网格线
#plt.savefig('年度柱状图.png')
#plt.show()

#饼图
plt.figure(figsize=(12,6))
method_count.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('观测方法发现占比', fontsize=16)
plt.xlabel('观测方法',fontsize=12)
plt.ylabel('')
plt.xticks(rotation=0) #控制 x 轴标签旋转
plt.grid(axis='y') #只画y网格线
#plt.savefig('年度饼图.png')
#plt.show()

#散点图
plt.figure(figsize=(12,6))
sns.scatterplot(
    data=mass_def,
    x='轨道周期',
    y='行星质量',
    hue='观测方法', #不同颜色表示观测方法
    size='距地距离', #点的大小表示离地球的距离
    sizes=(20,200), #点大小范围
    alpha=0.7 #点透明度（0，1）
)
plt.title('行星质量vs轨道周期(按观测方法分类)', fontsize=16)
plt.xlabel('轨道周期',fontsize=12)
plt.ylabel('行星质量',fontsize=12)
plt.legend(bbox_to_anchor=(1.05,1),loc='upper left')
plt.grid(True)


#平均特征柱状图
plt.figure(figsize=(12,6)) #设置图像大小
method_stats.plot(kind='bar',color='skyblue')
plt.title('不同观测方法发现行星的平均特征',fontsize=16)
plt.ylabel('平均值',fontsize=12)
plt.xticks(rotation=0) #控制 x 轴标签旋转
plt.grid(axis='y') #只画y网格线
plt.savefig('观测方法的平均柱状图.png')
plt.show()

#箱线图
plt.figure(figsize=(12,6)) #设置图像大小
sns.boxplot(data=mass_def[['行星质量','轨道周期','距地距离']])
plt.title('行星特征箱线图-异常值分析',fontsize=16)
plt.ylabel('数值',fontsize=12)
plt.grid(axis='y') #只画y网格线


#热力图
plt.figure(figsize=(12,6))
sns.heatmap(
    corr_matrix,
    annot=True, # 在格子里显示数值
    cmap='coolwarm', # 颜色主题
    fmt=".2f",  # 保留两位小数
    linewidths=0.5

)
plt.title('行星特征相关热力图', fontsize=16)

#多折线图
plt.figure(figsize=(12,6)) #设置图像大小
#绘制每列
for method in year_method_count.columns:
    plt.plot(
        year_method_count.index,
        year_method_count[method],
        marker = 'o',
        label = method
    )
plt.title('按观测方法分组的年份发现数量趋势', fontsize=16)   
plt.xlabel('年份',fontsize=12)
plt.ylabel('发现数量',fontsize=12)
plt.xticks(rotation=0) #控制 x 轴标签旋转
plt.grid(True) #打开网格线
plt.legend(bbox_to_anchor=(1.05,1),loc='upper left') #放右边
plt.tight_layout() #自动调整布局
plt.savefig('年度方法分组折线图.png')
plt.show()