/* SAS - Regression */
/* 20210716 your hubby */


/* comment : ctrl + / */
/* cancel : shift + ctrl + / */

/* read data from .sas7dbat file */

libname test '{path}';

data mydata;
    set '{path\file.sas7dbat}';
run;

/* proc contents; */
/* run; */


/* test : each market's asset mean */

proc univariate data = test.mydata;
    by mkttype;
    var at;
    output out = test.mymean
        mean = at_mean std = at_std;
run;

proc print data = test.mymean;
run;


/* regression test : asset ~ liabilities capital */

proc corr data = test.mydata;
    var at lt capital;

proc reg data = test.mydata;
    model at = lt capital / dw vif collin selection = backward;
    /* option (show ouput for each obs.) : p - predicted value, clm - confidence interval, r - residual */
    /* option : stb - standardized estimate */
run;


/* dummy variable (ex)
    d1 = 0; d2 = 0;
    if var1 = 1 then d1 = 1;
    if var2 = 1 then d2 = 1;

    model y = x1 x2 d1 d2;
*/

/* variable transformation (ex)
    data mydata;
        set 'path';
        x1long = log(x1);
        x2exp = exp(x2);
        x3sq = x3^2;
    run;

    * non-linear regression : use "nlin" or "model" instead of "reg"
*/


/* seems there are very many missing obs. ex) ****** */

/* result output style
    : Tools > Options > Preference > Results > Style : Journal (recommended from your hubby)
*/