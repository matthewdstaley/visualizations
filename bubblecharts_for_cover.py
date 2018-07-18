import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def scatter_plot(x,y,z,z_mag,clr,x_lab,y_lab,title):
    fig, ax = plt.subplots()
    ax.scatter(x,y, s=z*z_mag,c=clr, alpha=0.5)
    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.set_title(title)
    ax.grid()
    fig.autofmt_xdate()
    plt.show()

def bubble_chart_group1(df):
    group1 = df.groupby('hours_to_respond',as_index=False)['sold_customer'].sum()
    x = group1['hours_to_respond'].values
    y = group1['sold_customer'].values
    scatter_plot(x=x,y=y,z=y,z_mag=10,clr=y,x_lab='hours_to_respond',y_lab='conversions',title='conversions by hours_to_respond')

def bubble_chart_group2(df):
    group2 = df.groupby(['cohort_install'],as_index=False)['sold_customer', 'agent_time_to_respond_minutes'].sum()
    x=group2['cohort_install'].values
    y=group2['sold_customer'].values
    z=group2['agent_time_to_respond_minutes'].values
    scale_z = np.divide(z,y)
    scatter_plot(x=x,y=y,z=scale_z,z_mag=1,clr=y,x_lab='install_time',y_lab='conversions',title='conversions increase over time as agent response time decreases')

def main(df):
    df = df[df['user_id']!= 227126] #exclude user_id 227126 as an outlier // decided on this to make the graphs cleaner
    df['cohort_install'] = pd.to_datetime(df['cohort_install']) # this calculation was made in the googlesheet:

    df['sold_customer'] = pd.to_numeric(df['sold_customer'])
    df['agent_time_to_respond_minutes']=pd.to_numeric(df['agent_time_to_respond_minutes'])
    df['hours_to_respond'] = (df['agent_time_to_respond_minutes']/60).apply(np.floor)

    bubble_chart_group1(df)
    bubble_chart_group2(df)

    return df


if __name__ == "__main__":
    df = pd.read_csv('converted_users.csv')
    main(df)
