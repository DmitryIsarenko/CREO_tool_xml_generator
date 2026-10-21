list_of_feed_P = [
    1210,
    1160,
    1100,
    1240,
    1130,
    1010,
    830,
    750,
]

list_of_feed_M = [
    700,
    595,
    510,
    510,
    510,
    510,
    510,
    485,
    445,
    430,
]

cut_relation = {
    'iso_P': {
        'Vc': 120,
        'Vz': 0.05,
    },
    'iso_M': {
        'Vc': 80,
        'Vz': 0.045,
    },
    'iso_K': {
        'Vc': 100,
        'Vz': 0.05,
    },
    'iso_N': {
        'Vc': 180,
        'Vz': 0.06,
    },
    'iso_S': {
        'Vc': 60,
        'Vz': 0.045,
    },
    'iso_H': {
        'Vc': 70,
        'Vz': 0.04,
    },
}

iso_P = cut_relation['iso_P']
iso_M = cut_relation['iso_M']
iso_K = cut_relation['iso_K']
iso_N = cut_relation['iso_N']
iso_S = cut_relation['iso_S']
iso_H = cut_relation['iso_H']

multiplier_P_to_M = 0.5
multiplier_P_to_N = 2
multiplier_M_to_P = 2
multiplier_M_to_N = 4


def transform_feeds(
    list_of_feed: list[float],
    iso_from: dict[str, float],
    iso_to: dict[str, float],
    Vc_from: float,
    Vc_to: float,
) -> None:
    """Transform feeds."""
    mult_vc = iso_to['Vc'] / iso_from['Vc']
    mult_vz = iso_to['Vz'] / iso_from['Vz']
    mult_vc_mod = Vc_to / Vc_from

    new_feed_list = [
        round(f * mult_vz * mult_vc * mult_vc_mod, ndigits=0)
        for f in list_of_feed
    ]
    print()
    for feed in new_feed_list:
        print(feed)
    print()


if __name__ == '__main__':
    # transform_feeds(list_of_feed=list_of_feed_P,
    # multiplier=multiplier_P_to_M)
    # transform_feeds(list_of_feed=list_of_feed_P,
    # multiplier=multiplier_P_to_N)
    # transform_feeds(list_of_feed=list_of_feed_M,
    # multiplier=multiplier_M_to_P)
    # transform_feeds(list_of_feed=list_of_feed_M,
    # multiplier=multiplier_M_to_N)
    transform_feeds(
        list_of_feed=list_of_feed_M,
        iso_from=iso_M,
        iso_to=iso_P,
        Vc_from=80,
        Vc_to=80,
    )
