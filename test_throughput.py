# this is the test file to check through put of different file
import seaborn as sns, numpy as np
import matplotlib.pyplot as plt
df = sns.load_dataset("iris")
print(df)
 
ax = sns.boxplot(x="species", y="sepal_length", data=df)
 
# Calculate number of obs per group & median to position labels
medians = df.groupby(['species'])['sepal_length'].median().values
nobs = df['species'].value_counts().values
nobs = [str(x) for x in nobs.tolist()]
nobs = ["n: " + i for i in nobs]
 
# Add it to the plot
pos = range(len(nobs))
for tick,label in zip(pos,ax.get_xticklabels()):
	ax.text(pos[tick], medians[tick] + 0.03, nobs[tick],
	horizontalalignment='center', size='x-small', color='w', weight='semibold')
 
plt.show()