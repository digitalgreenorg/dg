import { cardGraphConfig } from './GraphCardsConfig';
export const cardConfig = {

    'No_of_clusters':{    
                        text:'#Clusters',
                        overall : {
                            borrowData:false,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_clusters,
                            },
                        },
                        recent : {
                            borrowData:false,
                            dateRange:60, // In days
                            filter:true,
                            cards:true,
                        },
                   },

    'No_of_Farmers':{
                        text:'#Farmers',
                        overall : {
                            borrowData:true,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_Farmers,
                            },
                        },
                        recent : {
                            borrowData:true,
                            dateRange:60, // In days
                            filter:true,
                            cards:true,
                        },
                   
                    },
    'Volume':      {
                        text:'Volume()%',
                        overall : {
                            borrowData:true,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.total_volume,
                            },
                        },
                        recent : {
                            borrowData:true,
                            dateRange:60, // In days
                            filter:true,
                            cards:true,
                        },
                   },

    'Total_payment':   {    
                        text:'Payment',
                        overall : {
                            borrowData:true,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.Total_payment,
                            },
                        },
                        recent : {
                            borrowData:true,
                            dateRange:60, // In days
                            filter:true,
                            cards:true,
                        },
                  },
                  

}