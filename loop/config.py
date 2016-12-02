header_dict = {'headers': [{'aggregator':{'columns': [ {
                                                    'label': 'S No',
                                                    'formula': None,
                                                    'total': False,
                                                    },
                                                    {
                                                     'label': 'Date',
                                                     'total': False, 
                                                     'formula': None,
                                                    },
                                                    {
                                                     'label': 'Market Value',
                                                     'total': False, 
                                                     'formula': None,
                                                    },
                                                    {
                                                     'label': 'Quantity [Q] (in Kg)',
                                                     'total': True, 
                                                     'formula': None,
                                                    },
                                                    {
                                                     'label': 'Farmers',
                                                     'total': False, 
                                                     'formula': None,
                                                    },
                                                    {'label': 'Aggregator Payment [AP] (in Rs) (0.25*Q)',
                                                     'total': True,
                                                     'formula': '0.25 * D',
                                                    },

                                                    {'label': 'Transport Cost [TC] (in Rs)',
                                                     'total': True,
                                                     'formula': None
                                                     
                                                    },
                                                    {'label': 'Farmers\''' Contribution [FC] (in Rs)',
                                                     'total': True,
                                                     'formula': None
                                                     
                                                    },
                                                    {'label': 'Commission Agent Contribution [CAC] (in Rs)',
                                                     'total': True,
                                                     'formula': None
                                                    },
                                                    {'label': 'Total Payment(in Rs) (AP + TC - FC - CAC)',
                                                     'total': True,
                                                     'formula': 'F + G - H - I'
                                                    }],
                                            'data': [[], []]
                                            }},

                        {'gaddidar':{'columns': [ {'label': 'Date',
                                                'total': False, 
                                                'formula': None,
                                                },
                                                {'label': 'Commission Agent',
                                                 'total': False, 
                                                 'formula': None,
                                                },
                                                { 'label': 'Market',
                                                  'total': False,  
                                                  'formula': None,
                                                },
                                                {'label': 'Quantity [Q] (in Kg)',
                                                 'total': True,
                                                 'formula': None,
                                                },
                                                {'label': 'Commission Agent Discount[CAD] (in Rs/Kg)',
                                                 'total': False, 
                                                 'formula': None,
                                                },
                                                {'label': 'Commission Agent Contribution[CAC] (in Rs) (Q*CAD)',
                                                 'total': True,
                                                 'formula': 'D * E'
                                                }],
                                   'data': [[], []]
                                    }
                        },
                        {'transporter':{'columns': [ {'label': 'Date',
                                                'total': False, 
                                                'formula': None,
                                                },
                                                {'label': 'Market',
                                                 'total': False, 
                                                 'formula': None,
                                                },
                                                {'label': 'Transporter',
                                                 'total': False, 
                                                 'formula': None,
                                                },
                                                {'label': 'Vehicle Type',
                                                 'total': False,
                                                 'formula': None,
                                                },
                                                {'label': 'Vehicle Number',
                                                 'total': False, 
                                                 'formula': None,
                                                },
                                                {'label': 'Tranport Cost in Rs',
                                                 'total': True,
                                                 'formula': None,
                                                }],
                                   'data': [[], []]
                                    }
                        }],

}



