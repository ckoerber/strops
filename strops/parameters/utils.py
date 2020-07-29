"""Utility function for parameters."""
from numpy import log10


def _ndec(x, offset=2):
    ans = offset - log10(x)
    ans = int(ans)
    if ans > 0 and x * 10.0 ** ans >= [0.5, 9.5, 99.5][offset]:
        ans -= 1
    return 0 if ans < 0 else ans


def format_gvar(mean, sdev):
    """Format mean and sdev to string.

    Copied from Peter Legape's gvar package:

    https://github.com/gplepage/gvar/blob/
        c19a50734f5bbacac1c1051a997e35aeab53f1a2/src/gvar/_gvarcore.pyx#L138
    """
    sdev = abs(sdev)

    if sdev >= 9.95:
        if abs(mean) >= 9.5:
            return "%.0f(%.0f)" % (mean, sdev)
        else:
            ndecimal = _ndec(abs(mean), offset=1)
            return "%.*f(%.*f)" % (ndecimal, mean, ndecimal, sdev)
    if sdev >= 0.995:
        if abs(mean) >= 0.95:
            return "%.1f(%.1f)" % (mean, sdev)
        else:
            ndecimal = _ndec(abs(mean), offset=1)
            return "%.*f(%.*f)" % (ndecimal, mean, ndecimal, sdev)
    else:
        ndecimal = max(_ndec(abs(mean), offset=1), _ndec(sdev))
        return "%.*f(%.0f)" % (ndecimal, mean, sdev * 10.0 ** ndecimal)
