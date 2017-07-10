import { chartsConfig } from '../../loop/configs/GraphsConfig';
import { tabsConfig } from '../../loop/configs/TabsConfig';
import { cardConfig } from '../../loop/configs/CardsConfig';
import { navsConfig } from '../../loop/configs/NavsConfig';
import { filterConfig } from '../../loop/configs/FiltersConfig';

export const environment = {
  production: true,
//   url: '/training/',
  url: 'http://127.0.0.1:8000/loop/',
  chartsConfig: chartsConfig,
  tabsConfig : tabsConfig,
  cardsConfig : cardConfig,
  navsConfig : navsConfig,
  filtersConfig: filterConfig,
};
