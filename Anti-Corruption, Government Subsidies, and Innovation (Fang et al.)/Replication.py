#setup
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import re
from linearmodels import PanelOLS
from stargazer.stargazer import Stargazer  
from tabulate import tabulate

ControlVar1 = ["lsoe", "lpolitical", "lroa", "ltobinq", "lleverage"]
ControlVar2 = ["lnasset", "llnage", "lleverage", "lintangible", "lroa", 
               "ltobinq", "lsoe", "lpolitical"]

###########################################################
############# TABLE 3: DESCRIPTIVE STATISTICS #############
###########################################################

#load data
df = pd.read_stata("FILEPATHNAME/main_dataset.dta") #INSERT YOUR OWN FILEPATH TO THE MAIN DATASET

#define variables
Var1 = ["subsidy_s", "etc_s", "aetc_s", "rd_s", "subsidy_rd", "pat_us", "cite_us", 
        "rdefficiency", "asset_mil", "age", "leverage", "roa", "tobinq", "intangible", 
        "soe", "political", "n_business"] 

variable_labels = {
    "subsidy_s": "Subsidies/Sales",
    "etc_s": "ETC/Sales", 
    "aetc_s": "AETC/Sales",
    "rd_s": "R&D/Sales",
    "subsidy_rd": "Subsidies/R&D",
    "pat_us": "Patents/Sales (U.S.)",
    "cite_us": "Relative Citation Strength (U.S.)",
    "rdefficiency": "R&D Efficiency",
    "asset_mil": "Size (Mil. RMB)",
    "age": "Age (Year)",
    "leverage": "Leverage",
    "roa": "Return on Assets",
    "tobinq": "Tobin's q",
    "intangible": "Intangible Assets/Assets",
    "soe": "SOE",
    "political": "Political Connection",
    "n_business": "Business in Other Regions",
    "lrdefficiency": "R&D Efficiency",
    "laetc_s": "AETC/Sales",
    "lpostremoval": "Post Removal",
    "lrdefficiency_postremoval": "R&D Efficiency x Post Removal",
    "laetc_postremoval": "AETC/Sales x Post Removal",
    "lsoe": "SOE",
    "lpolitical": "Political Connection",
    "lroa": "Return on Assets",
    "ltobinq": "Tobin's q",
    "lleverage": "Leverage",
    "lpostdeparture": "Post Departure",
    "lrdefficiency_postdeparture": "R&D Efficiency x Post Departure",
    "laetc_postdeparture": "AETC/Sales x Post Departure",
}

zero_float = ["asset_mil"] 

descstats = df[Var1].agg(['mean', 'std', 'min', 'median', 'max', 'count'])

#find split point 
split_index = Var1.index("asset_mil") if "asset_mil" in Var1 else len(Var1) // 2

#split variables into Panel A and Panel B
panel_a_vars = Var1[:split_index]  # Everything before asset_mil
panel_b_vars = Var1[split_index:]   # asset_mil and everything after

#generate HTML table
html_output = """
<html>
<head>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            font-family: Times New Roman, serif;
        }
        th, td {
            text-align: center;
        }
        th {
            border-top: 1px solid;    
            border-bottom: 1px solid; 
        }
        .panel-header {
            border-top: 1px solid;    
            border-bottom: 1px solid; 
            text-align: center;
        }
        .variable-name {
            text-align: left;
            font-weight: normal;
        }
    </style>
</head>
<body>
    <h2>Table 3. Sample Descriptive Statistics</h2>
    <table>
        <tr>
            <th style="text-align: left">Variable</th>
            <th>Mean</th>
            <th>Standard Deviation</th>
            <th>Minimum</th>
            <th>Median</th>
            <th>Maximum</th>
            <th>Observations</th>
        </tr>
        
        <!-- Panel A -->
        <tr class="panel-header">
            <td colspan="7">Panel A: Main variables</td>
        </tr>
"""

# Add Panel A rows
for var in panel_a_vars:
    row = descstats[var]
    if var in zero_float: html_output += f"""
        <tr>
            <td class="variable-name"><i>{variable_labels.get(var, var)}</i></td>
            <td>{row['mean']:.0f}</td>
            <td>{row['std']:.0f}</td>
            <td>{row['min']:.0f}</td>
            <td>{row['median']:.0f}</td>
            <td>{row['max']:.0f}</td>
            <td>{row['count']:.0f}</td>
        </tr>
    """
        
    else: html_output += f"""
        <tr>
            <td class="variable-name"><i>{variable_labels.get(var, var)}</i></td>
            <td>{row['mean']:.3f}</td>
            <td>{row['std']:.3f}</td>
            <td>{row['min']:.3f}</td>
            <td>{row['median']:.3f}</td>
            <td>{row['max']:.3f}</td>
            <td>{row['count']:.0f}</td>
        </tr>
    """

# Add Panel B header
html_output += """
        <!-- Panel B -->
        <tr class="panel-header">
            <td colspan="7">Panel B: Control variables</td>
        </tr>
"""

# Add Panel B rows
for var in panel_b_vars:
    row = descstats[var]
    if var in zero_float: html_output += f"""
        <tr>
            <td class="variable-name"><i>{variable_labels.get(var, var)}</i></td>
            <td>{row['mean']:.0f}</td>
            <td>{row['std']:.0f}</td>
            <td>{row['min']:.0f}</td>
            <td>{row['median']:.0f}</td>
            <td>{row['max']:.0f}</td>
            <td>{row['count']:.0f}</td>
        </tr>
    """
        
    else: html_output += f"""
        <tr>
            <td class="variable-name"><i>{variable_labels.get(var, var)}</i></td>
            <td>{row['mean']:.3f}</td>
            <td>{row['std']:.3f}</td>
            <td>{row['min']:.3f}</td>
            <td>{row['median']:.3f}</td>
            <td>{row['max']:.3f}</td>
            <td>{row['count']:.0f}</td>
        </tr>
    """

html_output += """
    </table>
</body>
</html>
"""

# Save to file
with open('descriptive_statistics.html', 'w') as f:
    f.write(html_output)

print("HTML table saved as 'descriptive_statistics.html'")

########################################################################################
############# TABLE 5: Panel Regressions: Merit, Corruption, and Subsidies #############
########################################################################################


############# PANEL A #############
df = pd.read_stata("/Users/maggiewang/Downloads/Year_4/Thesis/replication_package_MS-ENI-21-00153/main_dataset.dta")
df_clean = df.dropna(subset=['subsidy_s', 'lrdefficiency', 'inddummy', 'prodummy', 'year', 'firm'])
results = []

##regression 1
model1 = smf.ols(
    'subsidy_s ~ lrdefficiency + C(inddummy) + C(prodummy) + C(year)', 
    data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results.append(model1)
print("model 1 successful")

##regression 2
model2_df =df[df['lrdefficiency'].notna()] ##create if condition

model2 = smf.ols(                          ##regression
    'subsidy_s ~ laetc_s + C(inddummy) + C(prodummy) + C(year)',
    data=model2_df
).fit(cov_type='cluster', cov_kwds={'groups': model2_df['firm']})
results.append(model2)
print("model 2 success!")

##regression 3
model3 = smf.ols(
    'subsidy_s ~ lrdefficiency + laetc_s + lpostremoval + C(inddummy) + C(prodummy) + C(year)',
    data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results.append(model3)
print("model 3 af")

##reg 4
model4 = smf.ols(
    'subsidy_s ~ lrdefficiency + laetc_s + lpostremoval + lrdefficiency_postremoval + laetc_postremoval + C(inddummy) + C(prodummy) + C(year)',
    data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results.append(model4)
print("model 4 done")

##reg 5
model5_formula = 'subsidy_s ~ lrdefficiency + laetc_s + lpostremoval + lrdefficiency_postremoval + laetc_postremoval + ' + ' + '.join(ControlVar1) + ' + C(inddummy) + C(prodummy) + C(year)'
model5 = smf.ols(model5_formula, data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results.append(model5)
print("model 5")

#reg 6
model6_formula = 'subsidy_s ~ lrdefficiency + laetc_s + lpostremoval + lrdefficiency_postremoval + laetc_postremoval + ' + ' + '.join(ControlVar1) + ' + C(year) + C(firm)'
model6 = smf.ols(model6_formula, data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results.append(model6)
print("mod6")

#reg7
model7_formula = (
    'subsidy_s ~ lrdefficiency + laetc_s + lpostremoval + ' +
    'lrdefficiency_postremoval + laetc_postremoval + ' +
    ' + '.join(ControlVar1) + ' + C(year) + C(firm) + ' +
    'C(year):lrdefficiency + C(year):laetc_s + ' +
    'C(prodummy):lrdefficiency + C(prodummy):laetc_s'
)
model7 = smf.ols(model7_formula, data=df_clean).fit(
    cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results.append(model7)
print("777")

#generate table
df_panelA = df.drop(columns=['year', 'prodummy'])              ##dropped columns in options

stargazer = Stargazer(results)
stargazer.custom_columns(
    ['Subsidies/Sales_t+1', 'Subsidies/Sales_t+1', 'Subsidies/Sales_t+1', 'Subsidies/Sales_t+1', 'Subsidies/Sales_t+1', 'Subsidies/Sales_t+1', 'Subsidies/Sales_t+1'], 
    [1, 1, 1, 1, 1, 1, 1]
)
stargazer.significance_levels([0.1, 0.05, 0.01])               ##applying options
stargazer.show_degrees_of_freedom(False)
stargazer.title("Table 5: Panel Regressions: Merit, Corruption, and Subsidies Panel A")
stargazer.covariate_order(['lrdefficiency', 'laetc_s', 'lpostremoval', 
                           'lrdefficiency_postremoval', 'laetc_postremoval', 
                           'lsoe', 'lpolitical', 'lroa', 'ltobinq', 'lleverage'])
html_output = stargazer.render_html()
for var_name, label in variable_labels.items():
        html_output = html_output.replace(f'>{var_name}<', f'>{label}<')
with open('panel_A_results.html', 'w') as f:
    f.write(html_output)
    print("table saved!")

############# PANEL B #############
results_b = []
##regression 1
model1 = smf.ols(
    'subsidy_s ~ lrdefficiency + C(inddummy) + C(prodummy) + C(year)', 
    data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results_b.append(model1)
print("panel b.1 donee")

##regression 2
model2_df =df[df['lrdefficiency'].notna()] ##create if condition

model2 = smf.ols(                          ##regression
    'subsidy_s ~ laetc_s + C(inddummy) + C(prodummy) + C(year)',
    data=model2_df
).fit(cov_type='cluster', cov_kwds={'groups': model2_df['firm']})
results_b.append(model2)
print("panel b.2 success!")

##regression 3
model3 = smf.ols(
    'subsidy_s ~ lrdefficiency + laetc_s + lpostdeparture + C(inddummy) + C(prodummy) + C(year)',
    data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results_b.append(model3)
print("panel b.3 af")

##reg 4
model4 = smf.ols(
    'subsidy_s ~ lrdefficiency + laetc_s + lpostdeparture + lrdefficiency_postdeparture + laetc_postdeparture + C(inddummy) + C(prodummy) + C(year)',
    data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results_b.append(model4)
print("panel b.4 done")

##reg 5
model5_formula = 'subsidy_s ~ lrdefficiency + laetc_s + lpostdeparture + lrdefficiency_postdeparture + laetc_postdeparture+ ' + ' + '.join(ControlVar1) + ' + C(inddummy) + C(prodummy) + C(year)'
model5 = smf.ols(model5_formula, data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results_b.append(model5)
print("panel b.5 ate")

#reg 6
model6_formula = 'subsidy_s ~ lrdefficiency + laetc_s + lpostdeparture + lrdefficiency_postdeparture + laetc_postdeparture + ' + ' + '.join(ControlVar1) + ' + C(year) + C(firm)'
model6 = smf.ols(model6_formula, data=df_clean
).fit(cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results_b.append(model6)
print("panel b.6")

#reg7
model7_formula = (
    'subsidy_s ~ lrdefficiency + laetc_s + lpostdeparture + ' +
    'lrdefficiency_postdeparture + laetc_postdeparture + ' +
    ' + '.join(ControlVar1) + ' + C(year) + C(firm) + ' +
    'C(year):lrdefficiency + C(year):laetc_s + ' +
    'C(prodummy):lrdefficiency + C(prodummy):laetc_s'
)
model7 = smf.ols(model7_formula, data=df_clean).fit(
    cov_type='cluster', cov_kwds={'groups': df_clean['firm']})
results_b.append(model7)
print("panel b.7")

#generate table
df_panelA = df.drop(columns=['year', 'prodummy'])              ##dropped columns in options

stargazer = Stargazer(results_b)
stargazer.custom_columns(
    ['(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)'], 
    [1, 1, 1, 1, 1, 1, 1]
)
stargazer.significance_levels([0.1, 0.05, 0.01])               ##applying options
stargazer.show_degrees_of_freedom(False)
stargazer.title("Table 5: Panel Regressions: Merit, Corruption, and Subsidies Panel B")
stargazer.covariate_order(['lrdefficiency', 'laetc_s', 'lpostdeparture', 
                           'lrdefficiency_postdeparture', 'laetc_postdeparture', 
                           'lsoe', 'lpolitical', 'lroa', 'ltobinq', 'lleverage'])
html_output = stargazer.render_html()
for var_name, label in variable_labels.items():
        html_output = html_output.replace(f'>{var_name}<', f'>{label}<')
with open('panel_B_results.html', 'w') as f:
    f.write(html_output)
    print("table 2 saved!")
