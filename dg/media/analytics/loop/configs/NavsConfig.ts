export const navsConfig = {
    'navs':{
        'Home':{
            'active':true,
            'import':{
                'overall':false,
                'recent':false,
            },
            'containers':{
                'container1':{
                    'Volume and Famers Cummulative Count':{
                        'addDivs':['cummulativeCount']
                    },
                }
            } 
        },
        'Analytics':{
            'subNavs':{
                'Aggregators':{
                    'active':true,
                    'containers': {
                        'container1':{
                            'Volume':{},
                            'Visits':{}
                        },
                        'container2':{
                            'SPK/CPk':{},
                            'Recovered/Total':{}
                        },
                        'container3':{
                            'Farmer Count':{}
                        }
                    }
                },
                'Mandi':{
                    'containers':{
                        'container1':{
                            'Volume':{},
                            'Visits':{}
                        },
                        'container2':{
                            'SPK/CPk':{},
                            'Recovered/Total':{}
                        },
                        'container3':{
                            'Farmer Count':{}
                        }
                    }
                },
                'Crop':{
                    'containers':{
                        'container1':{
                            'Volume':{},
                            'Amount':{}
                        },
                        'container2':{
                            'Crop Prices':{}
                        },
                        'container3':{
                            'Farmer Count':{}
                        }
                    }
                },
            }
        },
        'Time Series': {
            'containers':{
                'container1':{
                    'test3':{},
                    'test4':{}
                }
            }   
        }
    },
}
