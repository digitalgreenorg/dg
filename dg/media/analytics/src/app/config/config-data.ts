export const STAT: any = [
      {
        entity_name : 'No. of Trainings',
        overall : {
            placeHolder : 'overallBar',
            filter:null,
            show:true,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
 	        placeHolder: 'recentBar',
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
            placeHolder : 'overallBar',
            filter:null,
            show:true,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
 	        placeHolder: 'recentBar',
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
        entity_name : 'Pass Percentage',
        overall : {
            placeHolder : 'overallBar',
            filter:null,
            show:true,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
 	        placeHolder: 'recentBar',
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
        entity_name : 'Avg Score',
        overall : {
            placeHolder : 'overallBar',
            filter:null,
            show:true,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
 	        placeHolder: 'recentBar',
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
