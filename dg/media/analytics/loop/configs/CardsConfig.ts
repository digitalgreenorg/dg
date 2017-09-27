import { cardGraphConfig } from './GraphCardsConfig';
export const cardConfig = {
  'No_of_clusters': {
    text: '#Clusters',
    helpTip: 'Group of villages in close proximity served by one Loop aggregator.',
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
      text: 'Clusters',
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
    helpTip: 'Farmers who have used Loop service at least once.',
    overall: {
      text: 'No_of_farmers_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_Farmers,
      },
    },
    recent: {
      text: 'Farmers',
      borrowData: true,
      dateRange: 60, // In days
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },

  },
  'Volume': {
    text: 'Volume(Kg)',
    helpTip: 'Total weight of farmer produce in kg collected and sold at the market.',
    overall: {
      text: 'Volume_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.total_volume,
      },
    },
    recent: {
      text: 'Volume',
      borrowData: true,
      dateRange: 60, // In days
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },
  },

  'Total_payment': {
    text: 'Payments',
    helpTip: 'Total amount of payments made to farmers for their produce.',
    overall: {
      text: 'Payments_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.Total_payment,
      },
    },
    recent: {
      text: 'Amount',
      borrowData: true,
      dateRange: 60, // In days
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },
  },

  'Cost_per_kg': {
    text: 'Cost per Kg',
    helpTip: 'Total CPK of vegetables sold = Transport CPK + Aggregator CPK',
    overall: {
      text: 'Cost_per_kg_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.Cost_per_kg,
      },
    },
    recent: {
      text: 'Cpk',
      borrowData: true,
      dateRange: 60, // In days
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },
  },

  'Sustainability_perc': {
    text: 'Sustainability',
    helpTip: 'Operational cost covered by local players = Sustainability Per Kg (SPK) / CPK where SPK = Trader discount per kg on commision + Farmers transport contribution per kg',
    overall: {
      text: 'Sustainability_overall',
      borrowData: true,
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.Sustainability,
      },
    },
    recent: {
      text: 'Spk',
      borrowData: true,
      dateRange: 60, // In days
      filter: false,
      graph: {
        show: true,
        options: cardGraphConfig.No_of_clusters_spark,
      },
    },
  },


}
