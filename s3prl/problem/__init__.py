"""
Pre-defined python recipes with customizable methods
"""

from .asr.superb_asr import SuperbASR
from .asr.superb_pr import SuperbPR
from .asr.superb_sf import SuperbSF
from .asv.superb_asv import SuperbASV
from .common.superb_er import SuperbER
from .common.superb_ic import SuperbIC
from .common.superb_ks import SuperbKS
from .common.superb_sid import SuperbSID
from .diarization.superb_sd import SuperbSD
from .common.hear_fsd import HearFSD
from .common.hear_esc50 import HearESC50
from .common.hear_beijing_opera import HearBeijingOpera
from .common.hear_cremad import HearCremaD
from .common.hear_gsc5hr import HearGSC5hr

__all__ = [
    "SuperbASR",
    "SuperbPR",
    "SuperbSF",
    "SuperbASV",
    "SuperbER",
    "SuperbIC",
    "SuperbKS",
    "SuperbSID",
    "SuperbSD",
    "HearFSD",
    "HearESC50",
    "HearBeijingOpera",
    "HearCremaD",
    "HearGSC5hr",
]
