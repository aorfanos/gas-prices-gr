def find_gas_station_company(icon_class):
    """Find the gas station company name."""
    match icon_class:
        case['gas_AVIN']:
            return 'AVIN'
        case['gas_CYCLON']:
            return 'CYCLON'
        case['gas_EKO']:
            return 'EKO'
        case['gas_SHELL']:
            return 'SHELL'
        case['gas_BP']:
            return 'BP'
        case['gas_AEGEAN']:
            return 'AEGEAN'
        case['gas_ELINOIL']:
            return 'ELINOIL'
        case['gas_SILKOIL']:
            return 'SILKOIL'
        case['gas_REVOIL']:
            return 'REVOIL'
        case['gas_ETEKA']:
            return 'ETEKA'
        case['gas_ANEXARTITO_PRATIRIO']:
            return 'INDEPENDENT'
        case _:
            return 'UNKNOWN'
