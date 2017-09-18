from pkg_resources import DistributionNotFound, get_distribution


def get_version()->str:
    try:
        return get_distribution('maxquant').version
    except DistributionNotFound:
        return '<unknown>'
