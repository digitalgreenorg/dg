# permission map for views and allowed user groups
PERMISSIONS_MAP = {
    'ScreeningAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'DefaultView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'VillageAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'BlockAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'DistrictAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'StateAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'CountryAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'FarmersJsonAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS', 'AWAAZDE_Group' ],
    'FarmersCsvAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'PartnerAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'ProjectAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
    'VideoAPIView': ['cocoadmin','COCOAPI_ALLOWED_USERS' ],
}