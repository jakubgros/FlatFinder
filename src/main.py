from data_provider.gumtree_flat_provider import GumtreeFlatProvider


if __name__ == "__main__":
    import logging
    logging.root.setLevel(logging.NOTSET)

    args = {
        "price_low": 100,
        "price_high": 2000,
        "from": 'ownr'
    }

    provider = GumtreeFlatProvider(**args)
    flats = provider.fetch(5)
    pass
