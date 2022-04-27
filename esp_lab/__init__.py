from pkg_resources import DistributionNotFound, get_distribution
from .data_access import get_monthly_data
from .data_access import preprocessor
from .stats import leadtime_skill_seas_resamp

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # pragma: no cover
    __version__ = '0.0.0'  # pragma: no cover
