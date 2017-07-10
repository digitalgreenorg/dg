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
                            graph : {
                                show : true,
                                options : cardGraphConfig.No_of_clusters_spark,
                            }
                        },
                   },

    'No_of_Farmers':{
                        text:'#Farmers',
                        overall : {
                            borrowData:true,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_clusters,
                            },
                        },
                        recent : {
                            borrowData:true,
                            dateRange:60, // In days
                            filter:true,
                            graph : {
                                show : true,
                                options : cardGraphConfig.No_of_clusters_spark,
                            },
                        },
                   
                    },
    'Volume':      {
                        text:'Volume',
                        overall : {
                            borrowData:true,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_clusters,
                            },
                        },
                        recent : {
                            borrowData:true,
                            dateRange:60, // In days
                            filter:true,
                            graph : {
                                show : true,
                                options : cardGraphConfig.No_of_clusters_spark,
                            },
                        },
                   },

    'Total_payment':   {    
                        text:'Payments',
                        overall : {
                            borrowData:true,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_clusters,
                            },
                        },
                        recent : {
                            borrowData:true,
                            dateRange:60, // In days
                            filter:true,
                            graph : {
                                show : true,
                                options : cardGraphConfig.No_of_clusters_spark,
                            },
                        },
                  },
    
    'Cost_per_kg':   {    
                        text:'Cost per Kg',
                        overall : {
                            borrowData:true,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_clusters,
                            },
                        },
                        recent : {
                            borrowData:true,
                            dateRange:60, // In days
                            filter:true,
                            graph : {
                                show : true,
                                options : cardGraphConfig.No_of_clusters_spark,
                            },
                        },
                  },

    'Sustainability_perc':   {    
                        text:'Sustainability',
                        overall : {
                            borrowData:true,
                            filter:false,
                            graph : {
                                show: true,
                                options : cardGraphConfig.No_of_clusters,
                            },
                        },
                        recent : {
                            borrowData:true,
                            dateRange:60, // In days
                            filter:true,
                            graph : {
                                show : true,
                                options : cardGraphConfig.No_of_clusters_spark,
                            },
                        },
                  },
                  

}