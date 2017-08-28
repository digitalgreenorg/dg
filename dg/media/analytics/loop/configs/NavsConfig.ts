export const navsConfig = {
  'navs': {
    'Home': {
      'active': true,
      'filters': false,
      'import': {
        'overall': false,
        'recent': false,
      },
      'class': 'col-11',
      'addTab': true,
      'containers': {
        // 'addTab': true,
        'container1': {
          'Volume and Famers Cummulative Count': {
            'addDivs': ['cummulativeCount']
          },
        }
      }
    },
    'Analytics': {
      // 'active': true,
      'filters': true,
      'subNavs': {
        'Aggregators': {
          'active': true,
          'class': 'col-6',
          'addTab': true,
          'containers': {
            // 'addTab': true,
            'container1': {
              // 'addTab':true,
              'Volume': {
                'addDivs': ['aggrvol']
              },
              'Visits': {
                'addDivs': ['aggrvisit']
              }
            },
            'container2': {
              // 'addTab':true,
              'SPK/CPK': {
                'addDivs': ['aggrspkcpk']
              },
              'Recovered/Total': {
                'addDivs': ['aggrrecoveredtotal']
              }
            },
            'container3': {
              'Farmer Count': {
                'addDivs': ['aggrfarmercount']
              }
            }
          }
        },
        'Mandi': {
          'class': 'col-sm-6',
          'addTab': true,
          'containers': {
            // 'addTab': true,
            'container1': {
              'Volume': {
                'addDivs': ['mandivolume']
              },
              'Visits': {
                'addDivs': ['mandivisit']
              }
            },
            'container2': {
              'SPK/CPk': {
                'addDivs': ['mandispkcpk']
              },
              'Recovered/Total': {
                'addDivs': ['mandirecoveredtotal']
              }
            },
            'container3': {
              'Farmer Count': {
                'addDivs': ['mandifarmercount']
              }
            }
          }
        },
        'Crop': {
          'class': 'col-sm-6',
          'addTab': true,
          'containers': {
            // 'addTab': true,
            'container1': {
              'Volume': {
                'addDivs': ['cropvolume']
              },
            },
            'container2': {
              'Crop Prices': {
                'addDivs': ['cropprices']
              }
            },
            'container3': {
              'Farmer Count': {
                'addDivs': ['cropfarmercount']
              }
            }
          }
        },
      }
    },
    'Time Series': {
      // 'active': true,
      'filters': true,
      'class': 'col-sm-11',
      'addTab': false,
      'containers': {
        // 'addTab': false,
        'container1': {
          'Volume Farmer': {
            'addDivs': ['volFarmerTS', 'cpkSpkTS']
          },
        },
      }
    },
    'Payments': {
      'href': '/loop/dashboard/payment/'
    }
  },
}
