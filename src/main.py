from data_provider.gumtree_flat_provider import GumtreeFlatProvider



args = {
    "price_low": 100,
    "price_high": 2000,
    "from": 'ownr'
}

provider = GumtreeFlatProvider(**args)
provider.run()
