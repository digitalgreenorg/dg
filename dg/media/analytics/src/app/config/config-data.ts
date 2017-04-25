export const STAT: any = [
      {
        entity_name : 'No. of Mediators',
        overall : {
            filter:null,
            show:false,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
            dateRange:60, // In days
            filter:{
                fromDate:'2017-01-01',
                toDate:'2017-03-31',
            },
            show: true,
        },
        graphs:{
            show:true
        },
        apiUrl:'http://localhost:8000/training/testTrainingApi'
      },
      {
        entity_name : 'No. of Mediators',
        overall : {
            filter:null,
            show:false,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
            dateRange:60, // In days
            filter:{
                fromDate:'2017-01-01',
                toDate:'2017-03-31',
            },
            show: true,
        },
        graphs:{
            show:true
        },
        apiUrl:'http://localhost:8000/training/testMediatorsApi'
      },
      {
        entity_name : 'No. of Mediators',
        overall : {
            filter:null,
            show:false,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
            dateRange:60, // In days
            filter:{
                fromDate:'2017-01-01',
                toDate:'2017-03-31',
            },
            show: true,
        },
        graphs:{
            show:true
        },
        apiUrl:'http://localhost:8000/training/testPassPercentApi'
      },
      {
        entity_name : 'No. of Mediators',
        overall : {
            filter:null,
            show:false,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
            dateRange:60, // In days
            filter:{
                fromDate:'2017-01-01',
                toDate:'2017-03-31',
            },
            show: true,
        },
        graphs:{
            show:true
        },
        apiUrl:'http://localhost:8000/training/testAvgScoreApi'
      },
    ]
