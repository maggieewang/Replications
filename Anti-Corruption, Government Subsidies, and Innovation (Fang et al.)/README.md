<a id="readme-top"></a>

<!-- ABOUT THE PROJECT -->
## Overview
This project is a replication of the paper "Anti-Corruption, Government Subsidies, and Innovation: Evidence from China"
by Lily Fang, Josh Lerner, Chaopeng Wu and Qi Zhang published in *Management Science* (2023). 

From the abstract: 
> "We leverage an exogenous shock—the crackdown on corrupt Chinese officials beginning in 2012—and examine how the allocation of research subsidies and innovative outcomes were affected. We argue that the staggered removal of provincial heads on corruption charges during China’s anticorruption campaign and the unanticipated departures of local government officials responsible for innovation programs led to plausibly exogenous reductions in corruption. After both events, the allocation of subsidies became more sensitive to firm merit than to corruption and subsidies became more strongly associated with future innovation. Anticorruption efforts and officials’ career incentives improved the efficacy of subsidy programs."

I replicate the descriptive statistics and main results of the paper using the dataset made available by the authors. The program
generates Table 3 (Sample Descriptive Statistics) and Table 5 (Main Regression) from the paper. While the authors'analysis was performed 
using STATA, I use Python for my replication. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Replication
Download the *main_dataset.dta*, then run the .py file. Please remember to change the file path name in the .py file before running.
The program will create and download all tables to your device. 

## Findings
There were minimal discrepancies between my replication and the original. Some values differed by 0.001, which can be attributed to 
differences in rounding. A few values lost their significance in my replication:
- The coefficient on R&D Efficiency x Post Removal (Col. 6, Table 5 Panel A) changed from significant at 1% to insignificant
- The coefficient on AETC/Sales x Post Removal (Col. 6, Table 5 Panel A) changed from significant at 0.1% to 0.5%.
- The coefficient on AETC/Sales x Post Removal (Col. 7, Table 5 Panel A) changed from significant at 1% to insignificant

<!-- CONTACT -->
## Contact

Maggie Wang - 
[![LinkedIn](https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff)](https://www.linkedin.com/in/maggie-wang-51103b1a7/) - magzywang@gmail.com

Project Link: [https://github.com/maggieewang/Replications/Importing%20Inequality%20(Advani%20et%20al.)](https://github.com/maggieewang/Replications/tree/12a352550228bf1b4c67b67c0462e459881bcbfc/Importing%20Inequality%20(Advani%20et%20al.))

<p align="right">(<a href="#readme-top">back to top</a>)</p>
