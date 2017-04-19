export const STAT: any = [
      {
        entity_name : 'No. of Trainings',
        overall : {
            filter:null,
            show:true,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
            dataRange:60, // In days
            filter:{
                fromDate:'2017-01-01',
                toDate:'2017-03-31',
            },
            show: false,
        },
        graphs:{
            show:false
        }
      },
      {
        entity_name : 'No. of Trainings',
        overall : {
            filter:null,
            show:false,
            apiUrl:'http://localhost:8000/training/testmethod'
        },
        recent : {
            dataRange:60, // In days
            filter:{
                fromDate:'2017-01-01',
                toDate:'2017-03-31',
            },
            show: true,
        },
        graphs:{
            show:false
        }
      },
    ]
