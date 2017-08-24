import { cardGraphConfig } from './GraphCardsConfig';
export const cardConfig = {

  'No_of_clusters': {
    text: '#Clusters',
    overall: {
      text: 'No_of_clusters_overall',
      borrowData: false,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters,
      },
    },
    recent: {
      text: 'active_cluster',
      borrowData: false,
      dateRange: 60, // In days
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      }
    },
  },

  'No_of_Farmers': {
    text: '#Farmers',
    overall: {
      text: 'No_of_farmers_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters,
      },
    },
    recent: {
      text: 'distinct_farmer_count',
      borrowData: true,
      dateRange: 60, // In days
      filter: true,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },

  },
  'Volume': {
    text: 'Volume(Kg)',
    overall: {
      text: 'Volume_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters,
      },
    },
    recent: {
      text: 'quantity__sum',
      borrowData: true,
      dateRange: 60, // In days
      filter: true,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },
  },

  'Total_payment': {
    text: 'Payments',
    overall: {
      text: 'Payments_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters,
      },
    },
    recent: {
      text: 'amount__sum',
      borrowData: true,
      dateRange: 60, // In days
      filter: true,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },
  },

  'Cost_per_kg': {
    text: 'Cost per Kg',
    overall: {
      text: 'Cost_per_kg_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters,
      },
    },
    recent: {
      text: 'cpk',
      borrowData: true,
      dateRange: 60, // In days
      filter: true,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },
  },

  'Sustainability_perc': {
    text: 'Sustainability',
    overall: {
      text: 'Sustainability_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters,
      },
    },
    recent: {
      text: 'spk',
      borrowData: true,
      dateRange: 60, // In days
      filter: true,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },
  },


}
