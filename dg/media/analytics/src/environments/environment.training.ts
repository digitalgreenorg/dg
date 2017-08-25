import { chartsConfig } from '../../training/configs/GraphsConfig';
import { tabsConfig } from '../../training/configs/TabsConfig';
import { cardConfig } from '../../training/configs/CardsConfig';
import { filterConfig } from '../../training/configs/FiltersConfig';

export const environment = {
  production: true,
  url: '/training/',
  // url: 'http://127.0.0.1:8000/training/',
  chartsConfig: chartsConfig,
  tabsConfig: tabsConfig,
  cardsConfig: cardConfig,
  filtersConfig: filterConfig,
};
