
import { chartsConfig, AddCommonOptions } from '../../loop/configs/GraphsConfig';
import { cardConfig } from '../../loop/configs/CardsConfig';
import { cardGraphConfig } from '../../loop/configs/GraphCardsConfig';
import { navsConfig } from '../../loop/configs/NavsConfig';
import { filtersConfig } from '../../loop/configs/FiltersConfig';
import { generalConfig } from '../../loop/configs/GeneralConfig';

export const environment = {
  production: true,
  // url: '/loop/',
  url: 'http://127.0.0.1:8000/loop/',
  chartsConfig: chartsConfig,
  cardsConfig: cardConfig,
  cardGraphConfig: cardGraphConfig,
  navsConfig: navsConfig,
  filtersConfig: filtersConfig,
  generalConfig: generalConfig,
  AddCommonOptions : AddCommonOptions
};
