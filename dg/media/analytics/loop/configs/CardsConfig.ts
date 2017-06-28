import { cardGraphConfig } from './GraphCardsConfig'
export const cardConfig = {

    'No_of_clusters':{    
                        text:'#Clusters',
                        overall : {
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_clusters,
                            },
                        },
                        recent : {
                            dateRange:60, // In days
                            filter:true,
                            cards:true,
                        },
                   },

    'No_of_Farmers':{
                        text:'#Farmers',
                        overall : {
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_Farmers,
                            },
                        },
                        recent : {
                            dateRange:60, // In days
                            filter:true,
                            cards:true,
                        },
                   
                    },
    'Volume':      {
                        text:'Volume()%',
                        overall : {
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.total_volume,
                            },
                        },
                        recent : {
                            dateRange:60, // In days
                            filter:true,
                            cards:true,
                        },
                   },

    'Total_payment':   {    
                        text:'Payment',
                        overall : {
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.Total_payment,
                            },
                        },
                        recent : {
                            dateRange:60, // In days
                            filter:true,
                            cards:true,
                        },
                  },
                  

}