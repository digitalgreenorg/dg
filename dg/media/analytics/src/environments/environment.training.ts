import { chartsConfig, AddCommonOptions } from '../../training/configs/GraphsConfig';
import { cardConfig } from '../../training/configs/CardsConfig';
import { cardGraphConfig } from '../../training/configs/GraphCardsConfig';
import { navsConfig } from '../../training/configs/NavsConfig';
import { filtersConfig } from '../../training/configs/FiltersConfig';
import { generalConfig } from '../../training/configs/GeneralConfig';

export const environment = {
  production: true,
  // url: '/training/',
  url: 'http://127.0.0.1:8000/training/',
  chartsConfig: chartsConfig,
  cardsConfig: cardConfig,
  cardGraphConfig: cardGraphConfig,
  navsConfig: navsConfig,
  filtersConfig: filtersConfig,
  generalConfig: generalConfig,
  AddCommonOptions: AddCommonOptions
};
