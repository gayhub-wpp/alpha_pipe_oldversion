# -*- coding: utf-8 -*-


import sys
import subprocess
from functools import wraps

import matplotlib as mpl
import seaborn as sns
import pandas as pd


def customize(func):

    @wraps(func)
    def call_w_context(*args, **kwargs):

        if not PlotConfig.FONT_SETTED:
            _use_chinese(True)

        set_context = kwargs.pop('set_context', True)
        if set_context:
            with plotting_context(), axes_style():
                sns.despine(left=True)
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return call_w_context


def plotting_context(context='notebook', font_scale=1.5, rc=None):

    if rc is None:
        rc = {}

    rc_default = {'lines.linewidth': 1.5}

    for name, val in rc_default.items():
        rc.setdefault(name, val)

    return sns.plotting_context(context=context, font_scale=font_scale, rc=rc)


def axes_style(style='darkgrid', rc=None):

    if rc is None:
        rc = {}

    rc_default = {}

    for name, val in rc_default.items():
        rc.setdefault(name, val)

    return sns.axes_style(style=style, rc=rc)


def print_table(table, name=None, fmt=None):

    from IPython.display import display

    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)

    if isinstance(table, pd.DataFrame):
        table.columns.name = name

    prev_option = pd.get_option('display.float_format')
    if fmt is not None:
        pd.set_option('display.float_format', lambda x: fmt.format(x))

    display(table)

    if fmt is not None:
        pd.set_option('display.float_format', prev_option)


class PlotConfig(object):
    FONT_SETTED = False
    USE_CHINESE_LABEL = False
    MPL_FONT_FAMILY = mpl.rcParams["font.family"]
    MPL_FONT = mpl.rcParams["font.sans-serif"]
    MPL_UNICODE_MINUS = mpl.rcParams["axes.unicode_minus"]


def get_chinese_font():
    if sys.platform.startswith('linux'):
        cmd = 'fc-list :lang=zh -f "%{family}\n"'
        output = subprocess.check_output(cmd, shell=True)
        if isinstance(output, bytes):
            output = output.decode("utf-8")
        zh_fonts = [
            f.split(',', 1)[0] for f in output.split('\n') if f.split(',', 1)[0]
        ]
        return zh_fonts

    return []


def _use_chinese(use=None):
    if use is None:
        return PlotConfig.USE_CHINESE_LABEL
    elif use:
        PlotConfig.USE_CHINESE_LABEL = use
        PlotConfig.FONT_SETTED = True
        _set_chinese_fonts()
    else:
        PlotConfig.USE_CHINESE_LABEL = use
        PlotConfig.FONT_SETTED = True
        _set_default_fonts()


def _set_chinese_fonts():
    default_chinese_font = ['SimHei', 'FangSong', 'STXihei', 'Hiragino Sans GB',
                            'Heiti SC', 'WenQuanYi Micro Hei']
    chinese_font = default_chinese_font + get_chinese_font()
    # ??????????????????
    mpl.rc(
        "font", **{
            # seaborn ???????????? sans-serif
            "sans-serif": chinese_font,
            "family": ','.join(chinese_font) + ',sans-serif'
        }
    )
    # ??????????????????
    mpl.rcParams["axes.unicode_minus"] = False


def _set_default_fonts():
    mpl.rc(
        "font", **{
            "sans-serif": PlotConfig.MPL_FONT,
            "family": PlotConfig.MPL_FONT_FAMILY
        }
    )
    mpl.rcParams["axes.unicode_minus"] = PlotConfig.MPL_UNICODE_MINUS


class _PlotLabels(object):

    def get(self, v):
        if _use_chinese():
            return getattr(self, v + "_CN")
        else:
            return getattr(self, v + "_EN")


class ICTS(_PlotLabels):
    TITLE_CN = "{} IC"
    TITLE_EN = "{} Period Forward Return Information Coefficient (IC)"
    LEGEND_CN = ["IC", "1??????????????????"]
    LEGEND_EN = ["IC", "1 month moving avg"]
    TEXT_CN = "?????? {:.3f} \n?????? {:.3f}"
    TEXT_EN = "Mean {:.3f} \nStd. {:.3f}"


ICTS = ICTS()


class ICHIST(_PlotLabels):
    TITLE_CN = "%s IC ???????????????"
    TITLE_EN = "%s Period IC"
    LEGEND_CN = "?????? {:.3f} \n?????? {:.3f}"
    LEGEND_EN = "Mean {:.3f} \nStd. {:.3f}"


ICHIST = ICHIST()


class ICQQ(_PlotLabels):
    NORM_CN = "??????"
    NORM_EN = "Normal"
    T_CN = "T"
    T_EN = "T"
    CUSTOM_CN = "?????????"
    CUSTOM_EN = "Theoretical"
    TITLE_CN = "{} IC {}?????? Q-Q ???"
    TITLE_EN = "{} Period IC {} Dist. Q-Q"
    XLABEL_CN = "{} ???????????????"
    XLABEL_EN = "{} Distribution Quantile"
    YLABEL_CN = "Observed Quantile"
    YLABEL_EN = "Observed Quantile"


ICQQ = ICQQ()


class QRETURNBAR(_PlotLabels):
    COLUMN_CN = "{} ???"
    COLUMN_EN = "{} Day"
    TITLE_CN = "????????????????????????"
    TITLE_EN = "Mean Period Wise Return By Factor Quantile"
    YLABEL_CN = "???????????? (bps)"
    YLABEL_EN = "Mean Return (bps)"


QRETURNBAR = QRETURNBAR()


class QRETURNVIOLIN(_PlotLabels):
    LEGENDNAME_CN = "????????????"
    LEGENDNAME_EN = "forward_periods"
    TITLE_CN = "???????????????????????????"
    TITLE_EN = "Period Wise Return By Factor Quantile"
    YLABEL_CN = "?????? (bps)"
    YLABEL_EN = "Return (bps)"


QRETURNVIOLIN = QRETURNVIOLIN()


class QRETURNTS(_PlotLabels):
    TITLE_CN = "??????????????????????????????????????? ({} ???)"
    TITLE_EN = "Top Minus Bottom Quantile Mean Return ({} Period Forward Return)"
    LEGEND0_CN = "???????????? (?????? {:.2f} ??????????????????)"
    LEGEND0_EN = "mean returns spread (+/- {:.2f} std)"
    LEGEND1_CN = "1 ??????????????????"
    LEGEND1_EN = "1 month moving avg"
    YLABEL_CN = "???????????????????????? (bps)"
    YLABEL_EN = "Difference In Quantile Mean Return (bps)"


QRETURNTS = QRETURNTS()


class ICGROUP(_PlotLabels):
    TITLE_CN = "?????? IC"
    TITLE_EN = "Information Coefficient By Group"


ICGROUP = ICGROUP()


class AUTOCORR(_PlotLabels):
    TITLE_CN = "?????????????????? (?????? {} ???)"
    TITLE_EN = "{} Period Factor Autocorrelation"
    YLABEL_CN = "????????????"
    YLABEL_EN = "Autocorrelation Coefficient"
    TEXT_CN = "?????? {:.3f}"
    TEXT_EN = "Mean {:.3f}"


AUTOCORR = AUTOCORR()


class TBTURNOVER(_PlotLabels):
    TURNOVER_CN = "{:d} ???????????????"
    TURNOVER_EN = "quantile {:d} turnover"
    TITLE_CN = "{} ????????????"
    TITLE_EN = "{} Period Top and Bottom Quantile Turnover"
    YLABEL_CN = "??????????????????"
    YLABEL_EN = "Proportion Of Names New To Quantile"


TBTURNOVER = TBTURNOVER()


class ICHEATMAP(_PlotLabels):
    TITLE_CN = "{} ??? IC ????????????"
    TITLE_EN = "Monthly Mean {} Period IC"


ICHEATMAP = ICHEATMAP()


class CUMRET(_PlotLabels):
    YLABEL_CN = "????????????"
    YLABEL_EN = "Cumulative Returns"
    TITLE_CN = "??????????????????????????????????????? ({} ?????????)"
    TITLE_EN = """Factor Weighted Long/Short Portfolio Cumulative Return
                  ({} Fwd Period)"""


CUMRET = CUMRET()


class TDCUMRET(_PlotLabels):
    YLABEL_CN = "????????????"
    YLABEL_EN = "Cumulative Returns"
    TITLE_CN = "?????????????????????????????????????????????????????? ({} ?????????)"
    TITLE_EN = """Long Top/Short Bottom Factor Portfolio Cumulative Return
                  ({} Fwd Period)"""


TDCUMRET = TDCUMRET()


class CUMRETQ(_PlotLabels):
    YLABEL_CN = "????????????(?????????)"
    YLABEL_EN = "Log Cumulative Returns"
    TITLE_CN = "????????? {} ??? Forward Return ???????????? (?????????)"
    TITLE_EN = """Cumulative Return by Quantile
                  ({} Period Forward Return)"""


CUMRETQ = CUMRETQ()


class AVGCUMRET(_PlotLabels):
    TITLE_CN = "?????????????????? (??? {} ???, ??? {} ???)"
    TITLE_EN = "Average Cumulative Returns by Quantile ({} days backword, {} days forward)"
    COLUMN_CN = "{} ??????"
    COLUMN_EN = "Quantile {}"
    XLABEL_CN = "??????"
    XLABEL_EN = "Periods"
    YLABEL_CN = "?????????????????? (bps)"
    YLABEL_EN = "Mean Return (bps)"


AVGCUMRET = AVGCUMRET()


class EVENTSDIST(_PlotLabels):
    TITLE_CN = "???????????????????????????"
    TITLE_EN = "Distribution of events in time"
    XLABEL_CN = "??????"
    XLABEL_EN = "Date"
    YLABEL_CN = "????????????"
    YLABEL_EN = "Number of events"


EVENTSDIST = EVENTSDIST()


class MISSIINGEVENTSDIST(_PlotLabels):
    TITLE_CN = "???????????????????????????"
    TITLE_EN = "Distribution of missing events in time"
    XLABEL_CN = "??????"
    XLABEL_EN = "Date"
    YLABEL_CN = "???????????????"
    YLABEL_EN = "Rate of missing events"


MISSIINGEVENTSDIST = MISSIINGEVENTSDIST()
