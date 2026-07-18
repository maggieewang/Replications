**import data
import delimited /Users/maggiewang/Downloads/Advani_et_al_1.csv, clear

**replicating figure 1.a)**
**creating last data point
preserve
drop if pctile > 99.91
egen avg_99 = mean(migrant_prop) if pctile > 98
drop if pctile > 99
replace migrant_prop = avg_99 if pctile > 98

gen reddot = pctile == 99

**generate graph
graph set window fontface "Times New Roman"

twoway (scatter migrant_prop pctile if reddot == 0, ///
title("Proportion of migrants at all percentiles of the income distribution") ///
xtitle("Percentiles") ytitle("Proportion of Migrants") ///
ylabel(0(0.05)0.25,format(%4.2f) glpattern(solid) noticks) ///
xlabel(1 20 40 60 80 100, nogrid noticks) scale(0.9)) ///
(scatter migrant_prop pctile if reddot == 1, mcolor(red) legend(off))

graph export figure1a.png

**replicating figure 1.b)

restore
preserve 

**recoding top 10%
drop if pctile < 90

recode pctile (90=1) (91=2) (92=3) (93=4) (94=5) (95=6) (96=7) (97=8) (98=9) (99=10) 
replace pctile = 11 if abs(pctile - 99.9) < 0.001
replace pctile = 12 if abs(pctile - 99.99) < 0.001
replace pctile = 13 if abs(pctile - 99.999) < 0.001

gen reddots = pctile > 9

**generate graph
twoway (scatter migrant_prop pctile if reddots == 0, xline(9.5, lcolor(red)) title("Proportion of migrants within the top decile") xtitle("Percentiles") ytitle("Proportion of Migrants") xlabel(1 "90" 2 "91" 3 "92" 4 "93" 5 "94" 6 "95" 7 "96" 8 "97" 9 "98" 10 "Top 1 - 0.1" 11 "0.1 - 0.01" 12 "0.01 - 0.001" 13 "Top 0.001", nogrid noticks angle(45)) ylabel(0.0(0.1)0.4,format(%3.1f) glpattern(solid) noticks)) (scatter migrant_prop pctile if reddots == 1, mcolor (red)  legend(off))


graph export figure1b.png
restore

**figure 2c replication**
import delimited /Users/maggiewang/Downloads/Advani_et_al_2.csv, clear

**filter data
**part a)
preserve
drop if prop_income == "NA"
destring prop_income, replace
keep if tax_year >= 2000 & tax_year <= 2010

summarize prop_income if ts == "Top 1"
summarize prop_income if ts == "Top 0.1"
summarize prop_income if ts == "Top 0.01"
summarize prop_income if ts == "Top 0.001"

table ts, statistic(mean prop_income)

**part b)
restore
drop if prop_income == "NA"
destring prop_income, replace

gen topshares = .
replace topshares = 1 if ts == "Top 1"
replace topshares = 2 if ts == "Top 0.1"
replace topshares = 3 if ts == "Top 0.01"
replace topshares = 4 if ts == "Top 0.001"

twoway (connected prop_income tax_year if ts == "Top 1", msymbol(s) mcolor(ebblue) lcolor(ebblue)) (connected prop_income tax_year if ts == "Top 0.1", msymbol(o) mcolor(navy) lcolor(navy)) (connected prop_income tax_year if ts == "Top 0.01", msymbol(t) mcolor(maroon) lcolor(maroon)) (connected prop_income tax_year if ts == "Top 0.001", msymbol(d) mcolor(red) lcolor(red) ylabel(0(0.1)0.4,format(%3.1f) glpattern(solid) noticks) xlabel(1997 2000 2003 2006 2009 2012 2015 2018, nogrid noticks) scale(0.7) title("Share of income in top fractiles that goes to migrants") ytitle("Share of income") xtitle("Years") legend(label(1 "Top 1") label(2 "Top 0.1") label(3 "Top 0.01") label(4 "Top 0.001")))

graph export figure2c.png








