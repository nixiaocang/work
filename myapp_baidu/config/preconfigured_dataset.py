# KILL ME

PRECONFIGURED_DATASET = {
    'search_analytics': {
        'id': 'searchanalytics',
        'name': 'Search Analytics',
        'metrics': [
            {
                "id": "click",
                "name": "Clicks",
                "uiName": "Clicks",
                "fieldType": "METRIC",
                "dataType": "Number",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": "NUMBER",
                # "originExtra": "COUNT",
                "child": []
            },
            {
                "id": "impression",
                "name": "Impressions",
                "uiName": "Impressions",
                "fieldType": "METRIC",
                "dataType": "Number",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": "NUMBER",
                # "originExtra": "COUNT",
                "child": []
            },
            {
                "id": "ctr",
                "name": "CTR",
                "uiName": "CTR",
                "fieldType": "METRIC",
                "dataType": "PERCENT",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": "PERCENT",
                # "originExtra": "AVERAGE",
                "child": []
            },
            {
                "id": "position",
                "name": "Position",
                "uiName": "Position",
                "fieldType": "METRIC",
                "dataType": "Number",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": "NUMBER",
                # "originExtra": "COUNT",
                "child": []
            }
        ]
        , 'dimensions': [
            {
                "id": 'query',
                "name": "Queries",
                "uiName": "Queries",
                "fieldType": "DIMENSION",
                "dataType": "STRING",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": None,
                # "originExtra": None,
                "child": []
            },
            {
                "id": 'page',
                "name": "Pages",
                "uiName": "Pages",
                "fieldType": "DIMENSION",
                "dataType": "STRING",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": None,
                # "originExtra": None,
                "child": []
            },
            {
                "id": 'country',
                "name": "Countries",
                "uiName": "Countries",
                "fieldType": "DIMENSION",
                "dataType": "STRING",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": None,
                # "originExtra": None,
                "child": []
            },
            {
                "id": 'device',
                "name": "Devices",
                "uiName": "Devices",
                "fieldType": "DIMENSION",
                "dataType": "STRING",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": None,
                # "originExtra": None,
                "child": []
            },
            {
                "id": 'searchtype',
                "name": "Search Type",
                "uiName": "Search Type",
                "fieldType": "DIMENSION",
                "dataType": "STRING",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": None,
                # "originExtra": None,
                "child": []
            },
            {
                "id": 'date',
                "name": "Dates",
                "uiName": "Dates",
                "fieldType": "DIMENSION",
                "dataType": "STRING",
                "allowFilter": True,
                "fieldUnit": None,
                # "originDataType": None,
                # "originExtra": None,
                "child": []
            }
        ]
    }
    , 'rp:links_to_your_site': {
        'id': 'links_to_your_site',
        'name': 'Links To Your Site',
        'metrics': [],
        'dimensions': []
    }
    , 'internal_links': {
        'id': 'internal_links',
        'name': 'Internal Links',
        'metrics': [],
        'dimensions': []
    }
    , 'manual_actions': {
        'id': 'manual_actions',
        'name': 'Manual Actions',
        'metrics': [],
        'dimensions': []
    }
    , 'international_targeting': {
        'id': 'international_targeting',
        'name': 'International Targeting',
        'metrics': [],
        'dimensions': []
    }
    , 'mobile_usability': {
        'id': 'mobile_usability',
        'name': 'Mobile Usability',
        'metrics': [],
        'dimensions': []
    }
}