import { chartsConfig } from '../../loop/configs/GraphsConfig';
import { tabsConfig } from '../../loop/configs/TabsConfig';
import { cardConfig } from '../../loop/configs/CardsConfig';

export const environment = {
  production: true,
//   url: '/training/',
  url: 'http://127.0.0.1:8000/training/',
  chartsConfig: chartsConfig,
  tabsConfig : tabsConfig,
  cardsConfig : cardConfig
};
