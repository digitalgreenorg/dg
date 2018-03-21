/*
This file records the different payment models for Loop categorized by their geography and start date.

A) Each model has the following parameters:
  1. start_date - specifies the start date for implementation of the model
  2. geography - specifies the geography in which the model is to be implemented
               - it is defined as key-value pairs with key being a country and value being a list of states
  3. aggregator_data_set - specifies the parameters required for "payment summary" table
                            (i) data_table_properties - specifies all parameters of data table columns provided to DataTable constructor
                            (ii) col_const - constant used for the particular column in code for calculations
                            (iii) calc_function - it is defined as key-value pairs with key being the calculation function to be used to get values for the column and value being a list of dependencies (also calc functions) of the given func
                            (iv) default_val - specifies the default data value for the column
                            (v) total - a boolean specifying if the total value is to be displayed for the column
                         - it is a list of objects with each object specifying a column in the table
                         - all the visible columns must be listed before the invisible columns

  4. gaddidar_data_set - specifies the parameters required for "commision agent details" table
  5. transporter_data_set - specifies the parameters required for "transporter details" table
  6. net_quantity_const - specifies which quantity constant is to be used for calculation of aggregator incentive
                        - eg. QUANTITY, QUANTITY_POST_DEDUCTION
  7. header_dict - specifies excel parameters for downloaded payment sheet
  8. the first model is the default model; add new models at the end of list
*/

var models = [
  // default model
  {
    start_date: '',
    geography: {
    },
    aggregator_data_set: [
      {
        data_table_properties: {
          title: "S No",
          visible: true
        },
        col_const: "SNO",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q'] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Quantity Post Deduction[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY_POST_DEDUCTION",
        calc_function: {
          "quantity_post_deduction": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Payment[AP] (in Rs)",
          visible: true
        },
        col_const: "AGGREGATOR_INCENTIVE",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Transport Cost[TC] (in Rs)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Farmers' Contribution[FC] (in Rs)",
          visible: true
        },
        col_const: "FARMER_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in Rs)",
          visible: true
        },
        col_const: "GADDIDAR_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Total Payment(in Rs) (AP + TC - FC - CAC)",
          visible: true
        },
        col_const: "NET_PAYMENT",
        calc_function: {
          "net_payment": ["aggregator_data", "aggregator_incentive"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Comment",
          visible: true
        },
        col_const: "AGGREGATOR_COMMENT",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Farmer Comment",
          visible: true
        },
        col_const: "FARMER_COMMENT",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      }
    ],
    gaddidar_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent",
          visible: true
        },
        col_const: "GADDIDAR_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Discount[CAD] (in Rs/Kg)",
          visible: true
        },
        col_const: "GADDIDAR_DISCOUNT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in Rs) (Q*CAD)",
          visible: true
        },
        col_const: "GADDIDAR_COMMISSION",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "GADDIDAR_COMMENT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Gaddidar Id",
          visible: false
        },
        col_const: "GADDIDAR_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Amount",
          visible: false
        },
        col_const: "AMOUNT",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Discount Criteria",
          visible: false
        },
        col_const: "GADDIDAR_DISCOUNT_CRITERIA",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      }
    ],
    transporter_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transporter",
          visible: true
        },
        col_const: "TRANSPORTER_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Phone Number",
          visible: true
        },
        col_const: "TRANSPORTER_PHONE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Type",
          visible: true
        },
        col_const: "VEHICLE_TYPE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Number",
          visible: true
        },
        col_const: "VEHICLE_NUMBER",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transport Cost (in Rs)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "TRANSPORTER_COMMENT",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Transportation Vehicle Id",
          visible: false
        },
        col_const: "TRANSPORTATION_VEHICLE_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Timestamp",
          visible: false
        },
        col_const: "TIMESTAMP",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "RowId",
          visible: false
        },
        col_const: "ROW_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      }
    ],
    net_quantity_const: "QUANTITY_POST_DEDUCTION",
    header_dict: {
      'aggregator': [{
          'column_width': 2.45,
          'formula': null,
          'label': 'S No',
          'total': false
        },
        {
          'column_width': 8.8,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 8.18,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 7.8,
          'formula': null,
          'label': "Quantity [Q'] (in Kg)",
          'total': true
        },
        {
          'column_width': 7.8,
          'formula': null,
          'label': 'Quantity Post Deduction [Q] (in Kg)**',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Payment [AP] (in Rs)##',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Transport Cost [TC] (in Rs)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': "Farmers' Contribution [FC] (in Rs)",
          'total': true
        },
        {
          'column_width': 7.5,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in Rs)',
          'total': true
        },
        {
          'column_width': 8.73,
          'formula': 'F + G - H - I',
          'label': 'Total Payment (in Rs) (AP + TC - FC - CAC)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Comment',
          'total': false
        },
        {
          'column_width': 9,
          'formula': null,
          'label': 'Farmer Comment',
          'total': false
        }
      ],
      'gaddidar': [{
          'column_width': 9.4,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 18.3,
          'formula': null,
          'label': 'Commission Agent',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Quantity [Q] (in Kg)',
          'total': true
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Commission Agent Discount [CAD] (in Rs/Kg)',
          'total': false
        },
        {
          'column_width': 16,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in Rs) (Q*CAD)',
          'total': true
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ],
      'transporter': [{
          'column_width': 8.8,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 17.3,
          'formula': null,
          'label': 'Transporter',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Phone Number',
          'total': false
        },
        {
          'column_width': 9.4,
          'formula': null,
          'label': 'Vehicle',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Vehicle Number',
          'total': false
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Tranport Cost (in Rs)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ]
    }
  },
  // model for India from start of program
  {
    start_date: '2015-11-27',
    geography: {
      India: ['Bihar', 'Maharashtra']
    },
    aggregator_data_set: [
      {
        data_table_properties: {
          title: "S No",
          visible: true
        },
        col_const: "SNO",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Payment[AP] (in Rs)",
          visible: true
        },
        col_const: "AGGREGATOR_INCENTIVE",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Transport Cost[TC] (in Rs)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Farmers' Contribution[FC] (in Rs)",
          visible: true
        },
        col_const: "FARMER_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in Rs)",
          visible: true
        },
        col_const: "GADDIDAR_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Total Payment(in Rs) (AP + TC - FC - CAC)",
          visible: true
        },
        col_const: "NET_PAYMENT",
        calc_function: {
          "net_payment": ["aggregator_data", "aggregator_incentive"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Comment",
          visible: true
        },
        col_const: "AGGREGATOR_COMMENT",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Farmer Comment",
          visible: true
        },
        col_const: "FARMER_COMMENT",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      }
    ],
    gaddidar_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent",
          visible: true
        },
        col_const: "GADDIDAR_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Discount[CAD] (in Rs/Kg)",
          visible: true
        },
        col_const: "GADDIDAR_DISCOUNT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in Rs) (Q*CAD)",
          visible: true
        },
        col_const: "GADDIDAR_COMMISSION",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "GADDIDAR_COMMENT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Gaddidar Id",
          visible: false
        },
        col_const: "GADDIDAR_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Amount",
          visible: false
        },
        col_const: "AMOUNT",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Discount Criteria",
          visible: false
        },
        col_const: "GADDIDAR_DISCOUNT_CRITERIA",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      }
    ],
    transporter_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transporter",
          visible: true
        },
        col_const: "TRANSPORTER_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Phone Number",
          visible: true
        },
        col_const: "TRANSPORTER_PHONE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Type",
          visible: true
        },
        col_const: "VEHICLE_TYPE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Number",
          visible: true
        },
        col_const: "VEHICLE_NUMBER",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transport Cost (in Rs)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "TRANSPORTER_COMMENT",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Transportation Vehicle Id",
          visible: false
        },
        col_const: "TRANSPORTATION_VEHICLE_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Timestamp",
          visible: false
        },
        col_const: "TIMESTAMP",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "RowId",
          visible: false
        },
        col_const: "ROW_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      }
    ],
    net_quantity_const: "QUANTITY",
    header_dict: {
      'aggregator': [{
          'column_width': 2.47,
          'formula': null,
          'label': 'S No',
          'total': false
        },
        {
          'column_width': 8.8,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 8.18,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 7.8,
          'formula': null,
          'label': "Quantity [Q] (in Kg)",
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Payment [AP] (in Rs)##',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Transport Cost [TC] (in Rs)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': "Farmers' Contribution [FC] (in Rs)",
          'total': true
        },
        {
          'column_width': 7.5,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in Rs)',
          'total': true
        },
        {
          'column_width': 8.73,
          'formula': 'E + F - G - H',
          'label': 'Total Payment (in Rs) (AP + TC - FC - CAC)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Comment',
          'total': false
        },
        {
          'column_width': 9,
          'formula': null,
          'label': 'Farmer Comment',
          'total': false
        }
      ],
      'gaddidar': [{
          'column_width': 9.4,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 18.3,
          'formula': null,
          'label': 'Commission Agent',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Quantity [Q] (in Kg)',
          'total': true
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Commission Agent Discount [CAD] (in Rs/Kg)',
          'total': false
        },
        {
          'column_width': 16,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in Rs) (Q*CAD)',
          'total': true
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ],
      'transporter': [{
          'column_width': 8.8,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 17.3,
          'formula': null,
          'label': 'Transporter',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Phone Number',
          'total': false
        },
        {
          'column_width': 9.4,
          'formula': null,
          'label': 'Vehicle',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Vehicle Number',
          'total': false
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Tranport Cost (in Rs)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ]
    }
  },
  // model for Bihar from 16/11/2017
  {
    start_date: '2017-11-16',
    geography: {
      India: ['Bihar']
    },
    aggregator_data_set: [
      {
        data_table_properties: {
          title: "S No",
          visible: true
        },
        col_const: "SNO",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q'] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Quantity Post Deduction[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY_POST_DEDUCTION",
        calc_function: {
          "quantity_post_deduction": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Payment[AP] (in Rs)",
          visible: true
        },
        col_const: "AGGREGATOR_INCENTIVE",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Transport Cost[TC] (in Rs)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Farmers' Contribution[FC] (in Rs)",
          visible: true
        },
        col_const: "FARMER_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in Rs)",
          visible: true
        },
        col_const: "GADDIDAR_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Total Payment(in Rs) (AP + TC - FC - CAC)",
          visible: true
        },
        col_const: "NET_PAYMENT",
        calc_function: {
          "net_payment": ["aggregator_data", "aggregator_incentive"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Comment",
          visible: true
        },
        col_const: "AGGREGATOR_COMMENT",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Farmer Comment",
          visible: true
        },
        col_const: "FARMER_COMMENT",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      }
    ],
    gaddidar_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent",
          visible: true
        },
        col_const: "GADDIDAR_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Discount[CAD] (in Rs/Kg)",
          visible: true
        },
        col_const: "GADDIDAR_DISCOUNT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in Rs) (Q*CAD)",
          visible: true
        },
        col_const: "GADDIDAR_COMMISSION",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "GADDIDAR_COMMENT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Gaddidar Id",
          visible: false
        },
        col_const: "GADDIDAR_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Amount",
          visible: false
        },
        col_const: "AMOUNT",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Discount Criteria",
          visible: false
        },
        col_const: "GADDIDAR_DISCOUNT_CRITERIA",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      }
    ],
    transporter_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transporter",
          visible: true
        },
        col_const: "TRANSPORTER_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Phone Number",
          visible: true
        },
        col_const: "TRANSPORTER_PHONE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Type",
          visible: true
        },
        col_const: "VEHICLE_TYPE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Number",
          visible: true
        },
        col_const: "VEHICLE_NUMBER",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transport Cost (in Rs)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "TRANSPORTER_COMMENT",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Transportation Vehicle Id",
          visible: false
        },
        col_const: "TRANSPORTATION_VEHICLE_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Timestamp",
          visible: false
        },
        col_const: "TIMESTAMP",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "RowId",
          visible: false
        },
        col_const: "ROW_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      }
    ],
    net_quantity_const: "QUANTITY_POST_DEDUCTION",
    header_dict: {
      'aggregator': [{
          'column_width': 2.45,
          'formula': null,
          'label': 'S No',
          'total': false
        },
        {
          'column_width': 8.8,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 8.18,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 7.8,
          'formula': null,
          'label': "Quantity [Q'] (in Kg)",
          'total': true
        },
        {
          'column_width': 7.8,
          'formula': null,
          'label': 'Quantity Post Deduction [Q] (in Kg)**',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Payment [AP] (in Rs)##',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Transport Cost [TC] (in Rs)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': "Farmers' Contribution [FC] (in Rs)",
          'total': true
        },
        {
          'column_width': 7.5,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in Rs)',
          'total': true
        },
        {
          'column_width': 8.73,
          'formula': 'F + G - H - I',
          'label': 'Total Payment (in Rs) (AP + TC - FC - CAC)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Comment',
          'total': false
        },
        {
          'column_width': 9,
          'formula': null,
          'label': 'Farmer Comment',
          'total': false
        }
      ],
      'gaddidar': [{
          'column_width': 9.4,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 18.3,
          'formula': null,
          'label': 'Commission Agent',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Quantity [Q] (in Kg)',
          'total': true
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Commission Agent Discount [CAD] (in Rs/Kg)',
          'total': false
        },
        {
          'column_width': 16,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in Rs) (Q*CAD)',
          'total': true
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ],
      'transporter': [{
          'column_width': 8.8,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 17.3,
          'formula': null,
          'label': 'Transporter',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Phone Number',
          'total': false
        },
        {
          'column_width': 9.4,
          'formula': null,
          'label': 'Vehicle',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Vehicle Number',
          'total': false
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Tranport Cost (in Rs)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ]
    }
  },
  // model for Bangladesh from start of program
  {
    start_date: '2015-11-27',
    geography: {
      Bangladesh: ['Jessore', 'Jhenaidah', 'Narail', 'Magura', 'Khulna', 'Faridpur']
    },
    aggregator_data_set: [
      {
        data_table_properties: {
          title: "S No",
          visible: true
        },
        col_const: "SNO",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Payment[AP] (in ৳)",
          visible: true
        },
        col_const: "AGGREGATOR_INCENTIVE",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Farmer Contribution in Aggregator Payment (in ৳)",
          visible: true
        },
        col_const: "FARMER_SHARE_IN_AGGREGATOR_INCENTIVE",
        calc_function: {
          "farmer_share_in_aggregator_incentive_half": ["aggregator_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Transport Cost[TC] (in ৳)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Farmers' Contribution[FC] (in ৳)",
          visible: true
        },
        col_const: "FARMER_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in ৳)",
          visible: true
        },
        col_const: "GADDIDAR_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Total Payment(in ৳) (AP + TC - FC - CAC)",
          visible: true
        },
        col_const: "NET_PAYMENT",
        calc_function: {
          "net_payment": ["aggregator_data", "aggregator_incentive"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Comment",
          visible: true
        },
        col_const: "AGGREGATOR_COMMENT",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Farmer Comment",
          visible: true
        },
        col_const: "FARMER_COMMENT",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      }
    ],
    gaddidar_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent",
          visible: true
        },
        col_const: "GADDIDAR_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Discount[CAD] (in Rs/Kg)",
          visible: true
        },
        col_const: "GADDIDAR_DISCOUNT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in Rs) (Q*CAD)",
          visible: true
        },
        col_const: "GADDIDAR_COMMISSION",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "GADDIDAR_COMMENT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Gaddidar Id",
          visible: false
        },
        col_const: "GADDIDAR_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Amount",
          visible: false
        },
        col_const: "AMOUNT",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Discount Criteria",
          visible: false
        },
        col_const: "GADDIDAR_DISCOUNT_CRITERIA",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      }
    ],
    transporter_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transporter",
          visible: true
        },
        col_const: "TRANSPORTER_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Phone Number",
          visible: true
        },
        col_const: "TRANSPORTER_PHONE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Type",
          visible: true
        },
        col_const: "VEHICLE_TYPE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Number",
          visible: true
        },
        col_const: "VEHICLE_NUMBER",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transport Cost (in Rs)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "TRANSPORTER_COMMENT",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Transportation Vehicle Id",
          visible: false
        },
        col_const: "TRANSPORTATION_VEHICLE_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Timestamp",
          visible: false
        },
        col_const: "TIMESTAMP",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "RowId",
          visible: false
        },
        col_const: "ROW_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      }
    ],
    net_quantity_const: "QUANTITY",
    header_dict: {
      'aggregator': [{
          'column_width': 2.47,
          'formula': null,
          'label': 'S No',
          'total': false
        },
        {
          'column_width': 8.7,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 8.18,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 7.8,
          'formula': null,
          'label': "Quantity [Q] (in Kg)",
          'total': true
        },
        {
          'column_width': 7.9,
          'formula': null,
          'label': 'Aggregator Payment [AP] (in ৳)##',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Farmer Share in Aggregator Payment (in ৳)##',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Transport Cost [TC] (in ৳)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': "Farmers' Contribution [FC] (in ৳)",
          'total': true
        },
        {
          'column_width': 7.4,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in ৳)',
          'total': true
        },
        {
          'column_width': 8.73,
          'formula': 'E + G - H - I',
          'label': 'Total Payment (in ৳) (AP + TC - FC - CAC)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Comment',
          'total': false
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Farmer Comment',
          'total': false
        }
      ],
      'gaddidar': [{
          'column_width': 9.4,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 18.3,
          'formula': null,
          'label': 'Commission Agent',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Quantity [Q] (in Kg)',
          'total': true
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Commission Agent Discount [CAD] (in ৳/Kg)',
          'total': false
        },
        {
          'column_width': 16,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in ৳) (Q*CAD)',
          'total': true
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ],
      'transporter': [{
          'column_width': 8.8,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 17.3,
          'formula': null,
          'label': 'Transporter',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Phone Number',
          'total': false
        },
        {
          'column_width': 9.4,
          'formula': null,
          'label': 'Vehicle',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Vehicle Number',
          'total': false
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Tranport Cost (in ৳)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ]
    }
  },
  // model for Bangladesh from 16/12/2017
  {
    start_date: '2017-12-16',
    geography: {
      Bangladesh: ['Jessore', 'Jhenaidah', 'Narail', 'Magura', 'Khulna', 'Faridpur']
    },
    aggregator_data_set: [
      {
        data_table_properties: {
          title: "S No",
          visible: true
        },
        col_const: "SNO",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Payment[AP] (in ৳)",
          visible: true
        },
        col_const: "AGGREGATOR_INCENTIVE",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Farmer Contribution in Aggregator Payment (in ৳)",
          visible: true
        },
        col_const: "FARMER_SHARE_IN_AGGREGATOR_INCENTIVE",
        calc_function: {
          "farmer_share_in_aggregator_incentive_one_fourth": ["aggregator_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Transport Cost[TC] (in ৳)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Farmers' Contribution[FC] (in ৳)",
          visible: true
        },
        col_const: "FARMER_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in ৳)",
          visible: true
        },
        col_const: "GADDIDAR_SHARE",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Total Payment(in ৳) (AP + TC - FC - CAC)",
          visible: true
        },
        col_const: "NET_PAYMENT",
        calc_function: {
          "net_payment": ["aggregator_data", "aggregator_incentive"]
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Aggregator Comment",
          visible: true
        },
        col_const: "AGGREGATOR_COMMENT",
        calc_function: {
          "aggregator_incentive": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Farmer Comment",
          visible: true
        },
        col_const: "FARMER_COMMENT",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "aggregator_data": ["gaddidar_data", "gaddidar_amount", "transporter_data"]
        },
        default_val: " ",
        total: false
      }
    ],
    gaddidar_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent",
          visible: true
        },
        col_const: "GADDIDAR_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Quantity[Q] (in Kg)",
          visible: true
        },
        col_const: "QUANTITY",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Commission Agent Discount[CAD] (in Rs/Kg)",
          visible: true
        },
        col_const: "GADDIDAR_DISCOUNT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Commission Agent Contribution[CAC] (in Rs) (Q*CAD)",
          visible: true
        },
        col_const: "GADDIDAR_COMMISSION",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "GADDIDAR_COMMENT",
        calc_function: {
          "gaddidar_commission": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Gaddidar Id",
          visible: false
        },
        col_const: "GADDIDAR_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Aggregator Id",
          visible: false
        },
        col_const: "AGG_ID",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Amount",
          visible: false
        },
        col_const: "AMOUNT",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Discount Criteria",
          visible: false
        },
        col_const: "GADDIDAR_DISCOUNT_CRITERIA",
        calc_function: {
          "gaddidar_data": null
        },
        default_val: 0,
        total: false
      }
    ],
    transporter_data_set: [
      {
        data_table_properties: {
          title: "Date",
          visible: true
        },
        col_const: "DATE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Market",
          visible: true
        },
        col_const: "MANDI_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transporter",
          visible: true
        },
        col_const: "TRANSPORTER_NAME",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Phone Number",
          visible: true
        },
        col_const: "TRANSPORTER_PHONE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Type",
          visible: true
        },
        col_const: "VEHICLE_TYPE",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Vehicle Number",
          visible: true
        },
        col_const: "VEHICLE_NUMBER",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Transport Cost (in Rs)",
          visible: true
        },
        col_const: "TRANSPORT_COST",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: true
      },
      {
        data_table_properties: {
          title: "Comment",
          visible: true
        },
        col_const: "TRANSPORTER_COMMENT",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "Mandi Id",
          visible: false
        },
        col_const: "MANDI_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Transportation Vehicle Id",
          visible: false
        },
        col_const: "TRANSPORTATION_VEHICLE_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: 0,
        total: false
      },
      {
        data_table_properties: {
          title: "Timestamp",
          visible: false
        },
        col_const: "TIMESTAMP",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      },
      {
        data_table_properties: {
          title: "RowId",
          visible: false
        },
        col_const: "ROW_ID",
        calc_function: {
          "transporter_data": null
        },
        default_val: " ",
        total: false
      }
    ],
    net_quantity_const: "QUANTITY",
    header_dict: {
      'aggregator': [{
          'column_width': 2.47,
          'formula': null,
          'label': 'S No',
          'total': false
        },
        {
          'column_width': 8.5,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 8.18,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 7.8,
          'formula': null,
          'label': "Quantity [Q] (in Kg)",
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Payment [AP] (in ৳)##',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Farmer Share in Aggregator Payment (in ৳)##',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Transport Cost [TC] (in ৳)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': "Farmers' Contribution [FC] (in ৳)",
          'total': true
        },
        {
          'column_width': 7.5,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in ৳)',
          'total': true
        },
        {
          'column_width': 8.73,
          'formula': 'E + G - H - I',
          'label': 'Total Payment (in ৳) (AP + TC - FC - CAC)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Aggregator Comment',
          'total': false
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Farmer Comment',
          'total': false
        }
      ],
      'gaddidar': [{
          'column_width': 9.4,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 18.3,
          'formula': null,
          'label': 'Commission Agent',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Quantity [Q] (in Kg)',
          'total': true
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Commission Agent Discount [CAD] (in ৳/Kg)',
          'total': false
        },
        {
          'column_width': 16,
          'formula': null,
          'label': 'Commission Agent Contribution [CAC] (in ৳) (Q*CAD)',
          'total': true
        },
        {
          'column_width': 10,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ],
      'transporter': [{
          'column_width': 8.8,
          'formula': null,
          'label': 'Date',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Market',
          'total': false
        },
        {
          'column_width': 16.5,
          'formula': null,
          'label': 'Transporter',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Phone Number',
          'total': false
        },
        {
          'column_width': 9.4,
          'formula': null,
          'label': 'Vehicle',
          'total': false
        },
        {
          'column_width': 11,
          'formula': null,
          'label': 'Vehicle Number',
          'total': false
        },
        {
          'column_width': 13,
          'formula': null,
          'label': 'Tranport Cost (in ৳)',
          'total': true
        },
        {
          'column_width': 8,
          'formula': null,
          'label': 'Comment',
          'total': false
        }
      ]
    }
  },
];