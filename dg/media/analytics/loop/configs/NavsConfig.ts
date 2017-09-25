export const navsConfig = {
  'navs': {
    'Home': {
      'active': true,
      'filters': false,
      'import': {
        'overall': true,
        'recent': true,
      },
      // 'class': 'col-11',
      'classes': {
        'container1': 'col-md-11',
      },

      'addTab': true,
      'containers': {
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
          'classes': {
            'container1': 'col-md-5',
            'container2': 'col-md-5',
            'container3': 'col-md-5'
          },
          'addTab': true,
          'containers': {
            'container1': {
              'Volume': {
                'addDivs': ['aggrvol']
              },
              'Visits': {
                'addDivs': ['aggrvisit']
              }
            },
            'container2': {
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
          'classes': {
            'container1': 'col-md-5',
            'container2': 'col-md-5',
            'container3': 'col-md-5'
          },
          'addTab': true,
          'containers': {
            'container1': {
              'Volume': {
                'addDivs': ['mandivolume']
              },
              'Visits': {
                'addDivs': ['mandivisit']
              }
            },
            'container2': {
              'SPK/CPK': {
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
          'classes': {
            'container1': 'col-md-5',
            'container2': 'col-md-5',
            'container3': 'col-md-5'
          },
          'addTab': true,
          'containers': {
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
      'classes': {
        'container1': 'col-md-5',
        'container2': 'col-md-5',
        'container3': 'col-md-10',
      },
      'addTab': true,
      'containers': {
        'container1': {
          'Volume Farmer': {
            'addDivs': ['volFarmerTS']
          }
        },
        'container2': {
          'CPK / SPK': {
            'addDivs': ['cpkSpkTS']
          }
        },
        'container3': {
          'Crop Price Range': {
            'addDivs': ['crop_price_range_ts']
          }
        }
      }
    },
    'Payments': {
      'href': '/loop/analytics/payment/'
    }
  },
}
